"""
PDF Report generation module
"""
import logging
from typing import List, Dict, Any
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from data_collector import BuildingMetrics

logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """Generates PDF reports for AI-RRM metrics"""
    
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(output_path, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Custom styles
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
    
    def generate_report(self, metrics: List[BuildingMetrics], summary_stats: Dict[str, Any]):
        """
        Generate complete PDF report
        
        Args:
            metrics: List of BuildingMetrics objects
            summary_stats: Summary statistics dictionary
        """
        logger.info(f"Generating PDF report: {self.output_path}")
        
        # Title
        self._add_title()
        
        # Executive Summary
        self._add_executive_summary(summary_stats)
        
        # Buildings with Issues (highlighted)
        buildings_with_issues = [m for m in metrics if m.has_issues]
        if buildings_with_issues:
            self._add_issues_section(buildings_with_issues)
        
        # All Buildings Summary Table
        self._add_all_buildings_table(metrics)
        
        # Detailed Insights Section
        self._add_insights_section(metrics)
        
        # Build PDF
        self.doc.build(self.story)
        logger.info(f"Report generated successfully: {self.output_path}")
    
    def _add_title(self):
        """Add report title"""
        title = Paragraph("AI-RRM Performance Report", self.title_style)
        self.story.append(title)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subtitle = Paragraph(f"Generated: {timestamp}", self.styles['Normal'])
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_executive_summary(self, stats: Dict[str, Any]):
        """Add executive summary section"""
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
    
    def _add_issues_section(self, buildings_with_issues: List[BuildingMetrics]):
        """Add section for buildings with issues"""
        self.story.append(Paragraph("Buildings Requiring Attention", self.heading_style))
        
        # Group by building
        building_dict = {}
        for metric in buildings_with_issues:
            if metric.building_name not in building_dict:
                building_dict[metric.building_name] = []
            building_dict[metric.building_name].append(metric)
        
        for building_name, building_metrics in building_dict.items():
            # Building name as subheading
            building_para = Paragraph(f"<b>{building_name}</b>", self.styles['Normal'])
            self.story.append(building_para)
            
            # Table for this building's frequencies
            data = [['Frequency', 'Health Score', 'RRM Changes', 'Insights', 'APs', 'Clients']]
            
            for m in building_metrics:
                insight_count = len(m.insights)
                health_color = 'red' if m.rrm_health_score < 70 else 'black'
                
                data.append([
                    m.frequency_label,
                    f"{m.rrm_health_score:.1f}",
                    str(m.rrm_changes),
                    str(insight_count),
                    str(m.ap_count),
                    str(m.client_count)
                ])
            
            table = Table(data, colWidths=[1.2*inch, 1*inch, 1*inch, 0.8*inch, 0.7*inch, 0.7*inch])
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
            self.story.append(Spacer(1, 0.2*inch))
        
        self.story.append(Spacer(1, 0.2*inch))
    
    def _add_all_buildings_table(self, metrics: List[BuildingMetrics]):
        """Add comprehensive table of all buildings"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("All Buildings - Detailed Metrics", self.heading_style))
        
        # Create table data
        data = [['Building', 'Frequency', 'Health', 'Changes', 'Insights', 'APs', 'Clients']]
        
        for m in sorted(metrics, key=lambda x: (x.building_name, x.frequency_band)):
            data.append([
                m.building_name,
                m.frequency_label,
                f"{m.rrm_health_score:.1f}",
                str(m.rrm_changes),
                str(len(m.insights)),
                str(m.ap_count),
                str(m.client_count)
            ])
        
        table = Table(data, colWidths=[1.8*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.7*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_insights_section(self, metrics: List[BuildingMetrics]):
        """Add detailed insights section"""
        # Collect all insights
        insights_data = []
        for m in metrics:
            for insight in m.insights:
                insights_data.append({
                    'building': m.building_name,
                    'frequency': m.frequency_label,
                    'type': insight.get('insightType', 'N/A'),
                    'description': insight.get('description', 'N/A'),
                    'reason': insight.get('reason', 'N/A')
                })
        
        if not insights_data:
            return
        
        self.story.append(PageBreak())
        self.story.append(Paragraph("Detailed Insights", self.heading_style))
        
        for insight in insights_data:
            # Building and frequency
            header = f"<b>{insight['building']} - {insight['frequency']}</b>"
            self.story.append(Paragraph(header, self.styles['Normal']))
            
            # Insight details
            details = f"Type: {insight['type']}<br/>Description: {insight['description']}<br/>Reason: {insight['reason']}"
            self.story.append(Paragraph(details, self.styles['Normal']))
            self.story.append(Spacer(1, 0.15*inch))
