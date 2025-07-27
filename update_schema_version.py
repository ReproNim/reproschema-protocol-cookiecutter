import os
import re
import sys
import json

# Get version from environment variable or use default
latest_release = os.environ.get("LATEST_RELEASE", "1.0.0")


def update_file(file_path, version):
    """Update schema version in a file, handling both string and array contexts."""
    try:
        with open(file_path, "r") as file:
            content = file.read()
        
        # Determine context path based on version
        if version == "1.0.0":
            context_path = "reproschema"
        else:
            context_path = "generic"
        
        # Update simple string @context
        content = re.sub(
            r'"@context": "https://raw\.githubusercontent\.com/ReproNim/reproschema/[^/]+/contexts/(generic|reproschema)"',
            f'"@context": "https://raw.githubusercontent.com/ReproNim/reproschema/{version}/contexts/{context_path}"',
            content,
        )
        
        # Update @context when it's in an array (handles multi-line)
        content = re.sub(
            r'"https://raw\.githubusercontent\.com/ReproNim/reproschema/[^/]+/contexts/(generic|reproschema)"',
            f'"https://raw.githubusercontent.com/ReproNim/reproschema/{version}/contexts/{context_path}"',
            content,
        )
        
        # Update schemaVersion
        content = re.sub(
            r'"schemaVersion": "[^"]+"', 
            f'"schemaVersion": "{version}"', 
            content
        )
        
        # Validate JSON syntax before writing
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Warning: {file_path} may have invalid JSON after update: {e}")
        
        with open(file_path, "w") as file:
            file.write(content)
            
        print(f"Updated: {file_path}")
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}", file=sys.stderr)
        return False
    
    return True


def main():
    """Main function to update all schema files."""
    updated_count = 0
    error_count = 0
    
    print(f"Updating schema files to version: {latest_release}")
    
    for root, dirs, files in os.walk("."):
        # Skip hidden directories and common non-schema directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith("_schema") or file.endswith("_item") or "_item_" in file or "_item" in file:
                file_path = os.path.join(root, file)
                if update_file(file_path, latest_release):
                    updated_count += 1
                else:
                    error_count += 1
    
    print(f"\nSummary: Updated {updated_count} files, {error_count} errors")
    
    # Exit with error code if there were errors
    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
