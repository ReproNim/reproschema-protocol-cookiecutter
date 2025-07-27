#!/usr/bin/env python
"""
Test script to verify the cookiecutter works correctly.
Run this script from the cookiecutter root directory.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def test_cookiecutter_generation():
    """Test that the cookiecutter generates a valid project."""
    print("Testing reproschema-protocol-cookiecutter...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Working in temporary directory: {tmpdir}")
        
        # Test parameters
        test_configs = [
            {"name": "Test1", "activities": 1},
            {"name": "Test3", "activities": 3},
            {"name": "Test5", "activities": 5},
        ]
        
        for config in test_configs:
            print(f"\n{'='*60}")
            print(f"Testing with {config['activities']} activities...")
            
            # Generate project using cookiecutter
            project_name = f"Test Protocol {config['name']}"
            cmd = [
                sys.executable, "-m", "cookiecutter",
                ".", "--no-input",
                f"protocol_name={project_name}",
                f"number_of_activities={config['activities']}",
                "--output-dir", tmpdir
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"✗ Cookiecutter failed: {result.stderr}")
                    return False
                print("✓ Cookiecutter executed successfully")
            except Exception as e:
                print(f"✗ Failed to run cookiecutter: {e}")
                return False
            
            # Verify the generated project
            project_dir = Path(tmpdir) / project_name
            if not project_dir.exists():
                print(f"✗ Project directory not created: {project_dir}")
                return False
            
            # Check essential files
            essential_files = [
                "README.md",
                "Makefile",
                "LICENSE",
                "config.env",
                "activities",
                "test_protocol_test1/test_protocol_test1_schema" if config['name'] == "Test1" else None,
                "test_protocol_test3/test_protocol_test3_schema" if config['name'] == "Test3" else None,
                "test_protocol_test5/test_protocol_test5_schema" if config['name'] == "Test5" else None,
            ]
            
            for file_path in essential_files:
                if file_path and not (project_dir / file_path).exists():
                    print(f"✗ Missing essential file: {file_path}")
                    return False
            print("✓ All essential files present")
            
            # Count activities
            activities_dir = project_dir / "activities"
            activity_count = len([d for d in activities_dir.iterdir() if d.is_dir()])
            if activity_count != config['activities']:
                print(f"✗ Expected {config['activities']} activities but found {activity_count}")
                return False
            print(f"✓ Correct number of activities: {activity_count}")
            
            # Validate protocol schema
            protocol_slug = f"test_protocol_{config['name'].lower()}"
            schema_path = project_dir / protocol_slug / f"{protocol_slug}_schema"
            
            try:
                with open(schema_path) as f:
                    schema = json.load(f)
                
                # Check schema structure
                if schema.get("@type") != "reproschema:Protocol":
                    print("✗ Invalid protocol type")
                    return False
                
                if schema.get("schemaVersion") != "1.0.0":
                    print(f"✗ Wrong schema version: {schema.get('schemaVersion')}")
                    return False
                
                # Check activities in schema
                activities_in_schema = len(schema.get("ui", {}).get("addProperties", []))
                if activities_in_schema != config['activities']:
                    print(f"✗ Schema has {activities_in_schema} activities, expected {config['activities']}")
                    return False
                
                print("✓ Protocol schema is valid")
                
            except json.JSONDecodeError as e:
                print(f"✗ Invalid JSON in protocol schema: {e}")
                return False
            except Exception as e:
                print(f"✗ Error reading protocol schema: {e}")
                return False
            
            # Check for Activity4 references (should not exist)
            for file_path in project_dir.rglob("*_schema"):
                with open(file_path) as f:
                    content = f.read()
                if "Activity4" in content:
                    print(f"✗ Found Activity4 reference in {file_path}")
                    return False
            print("✓ No invalid activity references")
            
            # Validate all JSON files
            invalid_json = []
            for json_file in project_dir.rglob("*_schema"):
                try:
                    with open(json_file) as f:
                        json.load(f)
                except json.JSONDecodeError:
                    invalid_json.append(json_file)
            
            for json_file in project_dir.rglob("*_item"):
                try:
                    with open(json_file) as f:
                        json.load(f)
                except json.JSONDecodeError:
                    invalid_json.append(json_file)
            
            if invalid_json:
                print(f"✗ Found {len(invalid_json)} invalid JSON files:")
                for f in invalid_json:
                    print(f"  - {f}")
                return False
            print("✓ All JSON files are valid")
            
            print(f"\n✅ Test with {config['activities']} activities PASSED")
    
    print(f"\n{'='*60}")
    print("✅ All tests PASSED! The cookiecutter is working correctly.")
    return True


if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("cookiecutter.json").exists():
        print("Error: cookiecutter.json not found. Run this script from the cookiecutter root directory.")
        sys.exit(1)
    
    # Run tests
    success = test_cookiecutter_generation()
    sys.exit(0 if success else 1)