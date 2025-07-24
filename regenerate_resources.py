"""
Script to regenerate resources.py from icon.png
Run this script after changing icon.png to update the resources.py file
"""

import os

def create_resources_py():
    # Read the icon.png file
    icon_path = "icon.png"
    
    if not os.path.exists(icon_path):
        print(f"Error: {icon_path} not found!")
        return
    
    with open(icon_path, 'rb') as f:
        icon_data = f.read()
    
    # Convert to hex representation for Qt resources
    hex_data = icon_data.hex()
    
    # Format as Qt resource data (16 bytes per line)
    formatted_lines = []
    for i in range(0, len(hex_data), 32):  # 32 hex chars = 16 bytes
        chunk = hex_data[i:i+32]
        hex_bytes = []
        for j in range(0, len(chunk), 2):
            if j + 1 < len(chunk):
                hex_bytes.append(f"\\x{chunk[j:j+2]}")
        if hex_bytes:
            formatted_lines.append(''.join(hex_bytes))
    
    # Create the resources.py content with properly formatted data
    resources_content = f'''# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: Custom Python script for QcomboLayer plugin
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\\
\\x{hex_data[0:2]}\\
{chr(10).join([formatted_lines[i] + "\\" for i in range(len(formatted_lines))])}
"

qt_resource_name = b"\\
\\x00\\x07\\
\\x07\\x3b\\xe0\\xb3\\
\\x00\\x70\\
\\x00\\x6c\\x00\\x75\\x00\\x67\\x00\\x69\\x00\\x6e\\x00\\x73\\
\\x00\\x0b\\
\\x09\\xad\\xc3\\xa2\\
\\x00\\x51\\
\\x00\\x63\\x00\\x6f\\x00\\x6d\\x00\\x62\\x00\\x6f\\x00\\x4c\\x00\\x61\\x00\\x79\\x00\\x65\\x00\\x72\\
\\x00\\x08\\
\\x0a\\x61\\x5a\\xa7\\
\\x00\\x69\\
\\x00\\x63\\x00\\x6f\\x00\\x6e\\x00\\x2e\\x00\\x70\\x00\\x6e\\x00\\x67\\
"

qt_resource_struct_v1 = b"\\
\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\
\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02\\
\\x00\\x00\\x00\\x14\\x00\\x02\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x03\\
\\x00\\x00\\x00\\x30\\x00\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x00\\
"

qt_resource_struct_v2 = b"\\
\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\
\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\
\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02\\
\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\
\\x00\\x00\\x00\\x14\\x00\\x02\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x03\\
\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\
\\x00\\x00\\x00\\x30\\x00\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x00\\
\\x00\\x00\\x01\\x97\\xf8\\xf5\\x94\\x78\\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
'''

    # Write to resources.py
    with open("resources.py", 'w', encoding='utf-8') as f:
        f.write(resources_content)
    
    print("resources.py has been regenerated successfully!")
    print(f"Icon size: {len(icon_data)} bytes")

if __name__ == "__main__":
    create_resources_py()
