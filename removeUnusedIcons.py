import os
import re

# Define the paths
icons_path = 'src/assets/icons'
src_path = 'src'

# Get list of icon component filenames (without extension)
icons = [f.replace('.tsx', '') for f in os.listdir(icons_path) if f.endswith('.tsx')]

# Function to check if an icon is used
def is_icon_used(icon_name, src_path, icons_path):
    pattern = re.compile(rf'\b{icon_name}\b')
    for root, _, files in os.walk(src_path):
        # Skip the icons_path directory
        if os.path.abspath(root).startswith(os.path.abspath(icons_path)):
            continue
        for file in files:
            if file.endswith('.tsx') or file.endswith('.ts'):
                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    content = f.read()
                    # Check for import statement or usage of the icon
                    if pattern.search(content):
                        print(f"Icon '{icon_name}' found in {os.path.join(root, file)}")
                        return True
    return False

# Check each icon and remove if unused
unused_icons = []
for icon in icons:
    print(f"Checking if icon '{icon}' is used...")
    if not is_icon_used(icon, src_path, icons_path):
        print(f"Removing unused icon: {icon}.tsx")
        os.remove(os.path.join(icons_path, f'{icon}.tsx'))
        unused_icons.append(icon)
    else:
        print(f"Icon '{icon}' is used.")

print(f'Removed unused icons: {unused_icons}')
