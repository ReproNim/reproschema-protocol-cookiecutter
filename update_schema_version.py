import os
import re

latest_release = os.environ['LATEST_RELEASE']

def update_file(file_path, version):
    with open(file_path, 'r') as file:
        content = file.read()

    content = re.sub(r'"@context": "https://raw\.githubusercontent\.com/ReproNim/reproschema/.+?/contexts/generic"',
                     f'"@context": "https://raw.githubusercontent.com/ReproNim/reproschema/{version}/contexts/generic"',
                     content)
    content = re.sub(r'"schemaVersion": ".+?"', f'"schemaVersion": "{version}"', content)

    with open(file_path, 'w') as file:
        file.write(content)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('_schema') or file.endswith('_item') or '_item_' in file:
            update_file(os.path.join(root, file), latest_release)
