#!/usr/bin/env python3
"""
Test script to generate sample PDF report with mock insights data.

This demonstrates the enhanced inline insights formatting by creating
sample buildings with various health scores and insights.
"""
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_collector import BuildingMetrics
from pdf_generator import PDFReportGenerator


def create_sample_data():
    """Create sample building metrics with realistic insights."""
    
    sample_metrics = []
    
    # Building 1: Admin - Has issues on 5 GHz and 6 GHz
    admin_24 = BuildingMetrics(
        building_id="sample-001",
        building_name="Admin Building",
        building_hierarchy="Global/Australia/Sydney/Admin Building",
        profile_name="CatC-Production",
        frequency_band=2,
        frequency_label="2.4 GHz",
        ap_count=12,
        client_count=45,
        rrm_health_score=85.5,
        rrm_changes=23,
        insights=[],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    admin_5 = BuildingMetrics(
        building_id="sample-001",
        building_name="Admin Building",
        building_hierarchy="Global/Australia/Sydney/Admin Building",
        profile_name="CatC-Production",
        frequency_band=5,
        frequency_label="5 GHz",
        ap_count=12,
        client_count=128,
        rrm_health_score=65.2,
        rrm_changes=87,
        insights=[
            {
                'insightType': 'High Co-Channel Interference',
                'insightValue': 45.2,
                'description': 'Multiple APs detected on overlapping channels causing interference',
                'reason': 'Automatic channel assignment optimization recommended. Consider enabling DCA (Dynamic Channel Assignment).'
            },
            {
                'insightType': 'Channel Utilization Warning',
                'insightValue': 78.5,
                'description': 'Channel utilization exceeds recommended threshold on channels 36, 40, and 44',
                'reason': 'High client density detected. Additional APs may be required in high-traffic areas.'
            }
        ],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    admin_6 = BuildingMetrics(
        building_id="sample-001",
        building_name="Admin Building",
        building_hierarchy="Global/Australia/Sydney/Admin Building",
        profile_name="CatC-Production",
        frequency_band=6,
        frequency_label="6 GHz",
        ap_count=8,
        client_count=34,
        rrm_health_score=72.8,
        rrm_changes=156,
        insights=[
            {
                'insightType': 'Excessive RRM Changes',
                'insightValue': 156,
                'description': 'RRM has made 156 optimization changes in the last 24 hours',
                'reason': 'Unstable RF environment detected. Review AP placement and external interference sources.'
            }
        ],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    # Building 2: Lab - Good health, no issues
    lab_24 = BuildingMetrics(
        building_id="sample-002",
        building_name="Lab Building",
        building_hierarchy="Global/Australia/Sydney/Lab Building",
        profile_name="CatC-Production",
        frequency_band=2,
        frequency_label="2.4 GHz",
        ap_count=8,
        client_count=22,
        rrm_health_score=92.3,
        rrm_changes=12,
        insights=[],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    lab_5 = BuildingMetrics(
        building_id="sample-002",
        building_name="Lab Building",
        building_hierarchy="Global/Australia/Sydney/Lab Building",
        profile_name="CatC-Production",
        frequency_band=5,
        frequency_label="5 GHz",
        ap_count=8,
        client_count=67,
        rrm_health_score=88.7,
        rrm_changes=18,
        insights=[],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    lab_6 = BuildingMetrics(
        building_id="sample-002",
        building_name="Lab Building",
        building_hierarchy="Global/Australia/Sydney/Lab Building",
        profile_name="CatC-Production",
        frequency_band=6,
        frequency_label="6 GHz",
        ap_count=6,
        client_count=15,
        rrm_health_score=94.1,
        rrm_changes=8,
        insights=[],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    # Building 3: Conference Center - Multiple issues
    conf_24 = BuildingMetrics(
        building_id="sample-003",
        building_name="Conference Center",
        building_hierarchy="Global/Australia/Sydney/Conference Center",
        profile_name="CatC-Production",
        frequency_band=2,
        frequency_label="2.4 GHz",
        ap_count=15,
        client_count=156,
        rrm_health_score=58.4,
        rrm_changes=203,
        insights=[
            {
                'insightType': 'Poor Coverage Quality',
                'insightValue': 58.4,
                'description': 'Coverage gaps detected in east wing and main hall areas',
                'reason': 'AP density insufficient for current client load. Consider adding 3-4 APs in identified coverage gaps.'
            },
            {
                'insightType': 'Client Distribution Imbalance',
                'insightValue': 35.2,
                'description': 'Uneven client distribution with some APs serving 20+ clients',
                'reason': 'Load balancing optimization needed. Enable client band steering and AP load balancing features.'
            }
        ],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    conf_5 = BuildingMetrics(
        building_id="sample-003",
        building_name="Conference Center",
        building_hierarchy="Global/Australia/Sydney/Conference Center",
        profile_name="CatC-Production",
        frequency_band=5,
        frequency_label="5 GHz",
        ap_count=15,
        client_count=289,
        rrm_health_score=62.1,
        rrm_changes=178,
        insights=[
            {
                'insightType': 'DFS Channel Interference',
                'insightValue': 42.8,
                'description': 'Radar detection events forcing channel changes on DFS channels',
                'reason': 'High radar activity in area. Consider using non-DFS channels or relocating affected APs.'
            }
        ],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    conf_6 = BuildingMetrics(
        building_id="sample-003",
        building_name="Conference Center",
        building_hierarchy="Global/Australia/Sydney/Conference Center",
        profile_name="CatC-Production",
        frequency_band=6,
        frequency_label="6 GHz",
        ap_count=12,
        client_count=78,
        rrm_health_score=81.5,
        rrm_changes=34,
        insights=[],
        timestamp="2026-02-03T10:00:00Z"
    )
    
    # Add all metrics
    sample_metrics.extend([
        admin_24, admin_5, admin_6,
        lab_24, lab_5, lab_6,
        conf_24, conf_5, conf_6
    ])
    
    # Calculate issue status for each
    for metric in sample_metrics:
        metric.calculate_issue_status()
    
    return sample_metrics


def create_summary_stats(metrics):
    """Generate summary statistics from sample data."""
    
    total_buildings = len(set(m.building_id for m in metrics))
    buildings_with_issues = len(set(m.building_id for m in metrics if m.has_issues))
    total_aps = sum(m.ap_count for m in metrics)
    total_clients = sum(m.client_count for m in metrics)
    total_insights = sum(len(m.insights) for m in metrics)
    avg_health = sum(m.rrm_health_score for m in metrics) / len(metrics)
    
    return {
        'total_buildings': total_buildings,
        'buildings_with_issues': buildings_with_issues,
        'total_aps': total_aps,
        'total_clients': total_clients,
        'total_insights': total_insights,
        'average_health_score': round(avg_health, 2),
        'collection_timestamp': datetime.now().isoformat()
    }


def main():
    """Generate sample PDF report."""
    
    print("=== AI-RRM Sample Report Generator ===")
    print()
    print("Generating sample data with insights...")
    
    # Create sample data
    metrics = create_sample_data()
    summary_stats = create_summary_stats(metrics)
    
    print(f"✓ Created {len(metrics)} metric entries")
    print(f"✓ {summary_stats['total_buildings']} buildings")
    print(f"✓ {summary_stats['buildings_with_issues']} with issues")
    print(f"✓ {summary_stats['total_insights']} total insights")
    print()
    
    # Generate PDF
    output_path = "output/sample_report.pdf"
    os.makedirs("output", exist_ok=True)
    
    print(f"Generating PDF: {output_path}")
    generator = PDFReportGenerator(output_path)
    generator.generate_report(metrics, summary_stats)
    
    print(f"✓ Report generated successfully!")
    print()
    print("Sample Data Summary:")
    print(f"  - Admin Building: 2 issues (5 GHz has 2 insights, 6 GHz has 1 insight)")
    print(f"  - Lab Building: No issues (all frequencies healthy)")
    print(f"  - Conference Center: 2 issues (2.4 GHz has 2 insights, 5 GHz has 1 insight)")
    print()
    print(f"Open: {output_path}")


if __name__ == '__main__':
    main()
