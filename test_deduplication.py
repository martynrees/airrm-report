#!/usr/bin/env python3
"""
Test building-level deduplication logic.

This script simulates the API response with floor-level data
and verifies that the deduplication groups floors by building name.
"""

def test_building_deduplication():
    """Test that floor-level sites are deduplicated by building name."""
    
    # Simulate API response with multiple floors per building
    mock_response = {
        'response': [
            {
                'aiRfProfileName': 'AI-RF-Profile',
                'associatedBuildings': [
                    {
                        'name': 'Wing B',
                        'instanceUUID': 'floor1-uuid',
                        'groupNameHierarchy': 'Global/India/CDC-5/Tower-S9/Wing B/Floor 1'
                    },
                    {
                        'name': 'Wing B',
                        'instanceUUID': 'floor2-uuid',
                        'groupNameHierarchy': 'Global/India/CDC-5/Tower-S9/Wing B/Floor 2'
                    },
                    {
                        'name': 'Wing B',
                        'instanceUUID': 'floor3-uuid',
                        'groupNameHierarchy': 'Global/India/CDC-5/Tower-S9/Wing B/Floor 3'
                    },
                    {
                        'name': 'Wing A',
                        'instanceUUID': 'winga-floor1-uuid',
                        'groupNameHierarchy': 'Global/India/CDC-5/Tower-S8/Wing A/Floor 1'
                    },
                    {
                        'name': 'Wing A',
                        'instanceUUID': 'winga-floor2-uuid',
                        'groupNameHierarchy': 'Global/India/CDC-5/Tower-S8/Wing A/Floor 2'
                    }
                ]
            }
        ]
    }
    
    # Simulate the deduplication logic
    building_map = {}
    floor_count = 0
    
    for profile in mock_response['response']:
        profile_name = profile.get('aiRfProfileName', 'Unknown')
        for site in profile.get('associatedBuildings', []):
            floor_count += 1
            building_name = site.get('name', '')
            
            # Group by building name - keep first occurrence
            if building_name and building_name not in building_map:
                site['aiRfProfileName'] = profile_name
                building_map[building_name] = site
    
    buildings = list(building_map.values())
    
    # Verify results
    print("=== Building Deduplication Test ===\n")
    print(f"Input: {floor_count} floor-level sites")
    print(f"Output: {len(buildings)} building-level entries\n")
    
    assert len(buildings) == 2, f"Expected 2 buildings, got {len(buildings)}"
    assert floor_count == 5, f"Expected 5 floors, got {floor_count}"
    
    building_names = {b['name'] for b in buildings}
    assert building_names == {'Wing A', 'Wing B'}, f"Unexpected building names: {building_names}"
    
    print("✓ Deduplication working correctly!")
    print(f"✓ Reduced {floor_count} floors to {len(buildings)} buildings")
    
    # Show the deduplicated buildings
    print("\nDeduplicated Buildings:")
    for building in buildings:
        print(f"  - {building['name']} (UUID: {building['instanceUUID']})")
    
    print("\n✅ All tests passed!")


if __name__ == '__main__':
    test_building_deduplication()
