"""
PDF Report generation module.

This module generates professional PDF reports for AI-RRM metrics with
enhanced formatting for insights and detailed building information.
"""
import logging
from datetime import datetime
from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from data_collector import BuildingMetrics

logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """
    Generates professional PDF reports for AI-RRM metrics.

    Creates multi-section reports with executive summary, building
    details, and comprehensive insights with improved formatting.
    """

    def __init__(self, output_path: str) -> None:
        """
        Initialize PDF report generator.

        Parameters:
            output_path (str): Path where PDF will be saved

        Returns:
            None
        """
        self.output_path: str = output_path
        self.doc = SimpleDocTemplate(output_path, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.story: List[Any] = []

        # Custom styles for better formatting
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=12,
            spaceBefore=12
        )

        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#2c5f8d'),
            spaceAfter=6,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        )

        self.insight_style = ParagraphStyle(
            'InsightText',
            parent=self.styles['Normal'],
            fontSize=9,
            leftIndent=20,
            spaceAfter=4,
            textColor=colors.HexColor('#333333')
        )

    def generate_report(
        self,
        metrics: List[BuildingMetrics],
        summary_stats: Dict[str, Any]
    ) -> None:
        """
        Generate complete PDF report with enhanced insights formatting.

        Parameters:
            metrics (List[BuildingMetrics]): List of collected metrics
            summary_stats (Dict[str, Any]): Summary statistics

        Returns:
            None
        """
        logger.info(f"Generating PDF report: {self.output_path}")

        # Title page
        self._add_title()

        # Executive Summary
        self._add_executive_summary(summary_stats)

        # Buildings with Issues (with inline insights)
        buildings_with_issues = [m for m in metrics if m.has_issues]
        if buildings_with_issues:
            self._add_issues_section(buildings_with_issues)

        # All Buildings Summary Table
        self._add_all_buildings_table(metrics)

        # Build PDF
        self.doc.build(self.story)
        logger.info(f"Report generated successfully: {self.output_path}")

    def _add_title(self) -> None:
        """Add report title and generation timestamp."""
        title = Paragraph("AI-RRM Performance Report", self.title_style)
        self.story.append(title)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subtitle = Paragraph(
            f"Generated: {timestamp}",
            self.styles['Normal']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.3*inch))

    def _add_executive_summary(self, stats: Dict[str, Any]) -> None:
        """Add executive summary section with key metrics."""
        self.story.append(Paragraph("Executive Summary", self.heading_style))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Buildings', str(stats.get('total_buildings', 0))],
            ['Buildings with Issues', str(stats.get('buildings_with_issues', 0))],
            ['Total Access Points', str(stats.get('total_aps', 0))],
            ['Total Clients', str(stats.get('total_clients', 0))],
            ['Total Insights', str(stats.get('total_insights', 0))],
            ['Average Health Score', f"{stats.get('average_health_score', 0):.1f}"],
        ]
        
        table = Table(summary_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))

    def _add_issues_section(
        self,
        buildings_with_issues: List[BuildingMetrics]
    ) -> None:
        """
        Add section for buildings requiring attention with insights.

        Shows each building with its metrics and lists all insights
        inline for immediate visibility.

        Parameters:
            buildings_with_issues (List[BuildingMetrics]): Buildings
                flagged as having issues

        Returns:
            None
        """
        self.story.append(
            Paragraph(
                "Buildings Requiring Attention",
                self.heading_style
            )
        )

        # Group by building
        building_dict: Dict[str, List[BuildingMetrics]] = {}
        for metric in buildings_with_issues:
            if metric.building_name not in building_dict:
                building_dict[metric.building_name] = []
            building_dict[metric.building_name].append(metric)

        for building_name, building_metrics in building_dict.items():
            # Building name as subheading
            building_para = Paragraph(
                f"<b>{building_name}</b>",
                self.subheading_style
            )
            self.story.append(building_para)

            # Hierarchy info
            hierarchy = building_metrics[0].building_hierarchy
            hierarchy_para = Paragraph(
                f"<i>{hierarchy}</i>",
                self.styles['Normal']
            )
            self.story.append(hierarchy_para)
            self.story.append(Spacer(1, 0.1*inch))

            # Metrics table for this building
            data = [[
                'Frequency',
                'Health',
                'RRM Changes',
                'APs',
                'Clients'
            ]]

            for m in sorted(
                building_metrics,
                key=lambda x: x.frequency_band
            ):
                data.append([
                    m.frequency_label,
                    f"{m.rrm_health_score:.1f}",
                    str(m.rrm_changes),
                    str(m.ap_count),
                    str(m.client_count)
                ])

            table = Table(
                data,
                colWidths=[1.2*inch, 1*inch, 1.2*inch, 0.8*inch, 0.8*inch]
            )
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d9534f')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            self.story.append(table)
            self.story.append(Spacer(1, 0.15*inch))

            # Show insights for this building (all frequencies)
            has_insights = any(len(m.insights) > 0 for m in building_metrics)

            if has_insights:
                insights_header = Paragraph(
                    "<b>Active Insights:</b>",
                    self.styles['Normal']
                )
                self.story.append(insights_header)

                for m in sorted(
                    building_metrics,
                    key=lambda x: x.frequency_band
                ):
                    if m.insights:
                        freq_label = Paragraph(
                            f"<b>{m.frequency_label}</b>",
                            self.insight_style
                        )
                        self.story.append(freq_label)

                        for idx, insight in enumerate(m.insights, 1):
                            insight_text = (
                                f"{idx}. <b>{insight.get('insightType', 'N/A')}</b><br/>"
                                f"   Description: {insight.get('description', 'N/A')}<br/>"
                                f"   Reason: {insight.get('reason', 'N/A')}"
                            )
                            insight_para = Paragraph(
                                insight_text,
                                self.insight_style
                            )
                            self.story.append(insight_para)
                            self.story.append(Spacer(1, 0.05*inch))

                self.story.append(Spacer(1, 0.1*inch))
            else:
                # No insights but flagged due to low health/high changes
                reason_text = "No insights currently. "
                if any(m.rrm_health_score < 70 for m in building_metrics):
                    reason_text += "Flagged due to low health score. "
                if any(m.rrm_changes > 100 for m in building_metrics):
                    reason_text += "Flagged due to high RRM changes."

                reason_para = Paragraph(
                    f"<i>{reason_text}</i>",
                    self.insight_style
                )
                self.story.append(reason_para)
                self.story.append(Spacer(1, 0.1*inch))

            self.story.append(Spacer(1, 0.2*inch))

        self.story.append(Spacer(1, 0.2*inch))

    def _add_all_buildings_table(
        self,
        metrics: List[BuildingMetrics]
    ) -> None:
        """
        Add comprehensive table of all buildings with summary.

        Parameters:
            metrics (List[BuildingMetrics]): All collected metrics

        Returns:
            None
        """
        self.story.append(PageBreak())
        self.story.append(
            Paragraph(
                "All Buildings - Complete Summary",
                self.heading_style
            )
        )

        # Create table data
        data = [[
            'Building',
            'Frequency',
            'Health',
            'Changes',
            'APs',
            'Clients',
            'Insights'
        ]]

        for m in sorted(
            metrics,
            key=lambda x: (x.building_name, x.frequency_band)
        ):
            # Format insights count with indicator
            insight_count = len(m.insights)
            insights_display = str(insight_count)
            if insight_count > 0:
                insights_display = f"⚠ {insight_count}"

            data.append([
                m.building_name,
                m.frequency_label,
                f"{m.rrm_health_score:.1f}",
                str(m.rrm_changes),
                str(m.ap_count),
                str(m.client_count),
                insights_display
            ])

        table = Table(
            data,
            colWidths=[
                1.6*inch,
                0.9*inch,
                0.7*inch,
                0.8*inch,
                0.6*inch,
                0.7*inch,
                0.7*inch
            ]
        )
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            (
                'ROWBACKGROUNDS',
                (0, 1),
                (-1, -1),
                [colors.white, colors.lightgrey]
            ),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))

        self.story.append(table)

        # Add legend for insights column
        legend = Paragraph(
            "<i>⚠ indicates active insights present</i>",
            self.styles['Normal']
        )
        self.story.append(Spacer(1, 0.1*inch))
        self.story.append(legend)
        self.story.append(Spacer(1, 0.3*inch))
