"""
Quick test script to verify modules can be imported and basic structure works
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from auth import DNACenterAuth
        print("✓ auth.py imported successfully")
    except Exception as e:
        print(f"✗ auth.py import failed: {e}")
        return False
    
    try:
        from api_client import DNACenterClient
        print("✓ api_client.py imported successfully")
    except Exception as e:
        print(f"✗ api_client.py import failed: {e}")
        return False
    
    try:
        from data_collector import DataCollector, BuildingMetrics
        print("✓ data_collector.py imported successfully")
    except Exception as e:
        print(f"✗ data_collector.py import failed: {e}")
        return False
    
    try:
        from pdf_generator import PDFReportGenerator
        print("✓ pdf_generator.py imported successfully")
    except Exception as e:
        print(f"✗ pdf_generator.py import failed: {e}")
        return False
    
    return True


def test_data_structures():
    """Test basic data structure creation"""
    print("\nTesting data structures...")
    
    try:
        from data_collector import BuildingMetrics
        
        metrics = BuildingMetrics(
            building_id="test-123",
            building_name="Test Building",
            building_hierarchy="Global/Test/Building",
            profile_name="TestProfile",
            frequency_band=5,
            frequency_label="5 GHz",
            ap_count=10,
            client_count=50,
            rrm_health_score=85.5,
            rrm_changes=5
        )
        
        metrics.calculate_issue_status()
        print(f"✓ Created BuildingMetrics: {metrics.building_name}")
        print(f"  - Health Score: {metrics.rrm_health_score}")
        print(f"  - Has Issues: {metrics.has_issues}")
        
        return True
    except Exception as e:
        print(f"✗ Data structure test failed: {e}")
        return False


if __name__ == '__main__':
    print("=== AI-RRM Report Generator - Module Test ===\n")
    
    success = True
    success = test_imports() and success
    success = test_data_structures() and success
    
    if success:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed")
        sys.exit(1)
