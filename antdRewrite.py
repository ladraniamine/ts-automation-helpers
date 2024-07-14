import os
import re

# Define the directory where your JavaScript/JSX files are located
root_dir = "src"

# Regular expression pattern to match import statements with destructuring
import_pattern = re.compile(r'^import\s*{\s*(.*?)\s*}\s*from\s*["\']antd["\']\s*;?\s*$', re.MULTILINE)

# Function to determine the import path for each component
def get_component_path(component_name):
    return f"antd/es/{component_name.lower()}"

# Function to replace import statements in a file
def replace_imports_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Search for import statements and replace them
    def replace_import(match):
        imports = match.group(1).split(',')
        replaced_imports = []
        for imp in imports:
            imp = imp.strip()
            component_name = imp.split(' as ')[-1].strip() if ' as ' in imp else imp
            path = get_component_path(component_name)
            replaced_imports.append(f"import {imp} from \"{path}\";")
            replaced_imports.append(f"import \"{path}/style/css\";")
        return '\n'.join(replaced_imports)

    # Perform replacements in the content
    new_content = import_pattern.sub(replace_import, content)

    # Write back to the file if changes were made
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
            print(f"Updated imports in {file_path}")

# Traverse all JavaScript/JSX files in the directory and its subdirectories
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(('.js', '.tsx','.ts')):
            file_path = os.path.join(dirpath, filename)
            replace_imports_in_file(file_path)
