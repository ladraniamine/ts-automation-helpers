import os
import re

# Define the directory where your JavaScript/JSX files are located
root_dir = "src"

# Regular expression pattern to match import statements with destructuring from Ant Design icons
import_pattern = re.compile(r'^import\s*{\s*(.*?)\s*}\s*from\s*["\']@ant-design/icons["\']\s*;?\s*$', re.MULTILINE)

# Function to generate import statements for individual icons
def generate_imports(icon_list):
    imports = []
    for icon in icon_list:
        imports.append(f"import {icon} from \"@ant-design/icons/{icon}\";")
    return "\n".join(imports)

# Function to replace import statements in a file
def replace_imports_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Search for import statements and replace them
    def replace_import(match):
        icons = match.group(1).split(',')
        icon_list = [icon.strip() for icon in icons]
        individual_imports = generate_imports(icon_list)
        return individual_imports

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
        if filename.endswith(('.js', '.jsx', '.ts', '.tsx')):
            file_path = os.path.join(dirpath, filename)
            replace_imports_in_file(file_path)
