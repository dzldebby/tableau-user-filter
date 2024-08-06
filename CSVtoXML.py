import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Step 1: Change the name of your user filter here e.g. [User-Filter-1]
filter_name = "[your-user-filter-name]"

# Step 2: Change this to your domain eg. external
your_domain = "your-server-name"

# Step 3: Change this to your variable name e.g. [City]
secondary_group_level = "[your-variable-name]"


primary_group_function = "intersection"
secondary_group_function = "level-members"

def create_iscurrentuser_expression(user):
    return f"ISCURRENTUSER('{your_domain}\\{user}')"


def csv_to_xml(csv_file_path, xml_file_path):
    # Define the namespace
    # Read CSV file
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        data = list(csvreader)
    # Create root element with namespace
    root = ET.Element('group', attrib={
        'name': filter_name,
        'name-style': 'unqualified',
        'ui-builder': 'identity-set'
    })
   
   
    # Create main structure
    groupfilter_c = ET.SubElement(root, 'groupfilter', attrib={'function': primary_group_function})
    ET.SubElement(groupfilter_c, 'groupfilter', attrib={'function': secondary_group_function, 'level': secondary_group_level})
    groupfilter_union = ET.SubElement(groupfilter_c, 'groupfilter', attrib={'function': 'union'})
    # Add false filter
    false_filter = ET.SubElement(groupfilter_union, 'groupfilter', attrib={'expression': 'false', 'function': 'filter'})
    ET.SubElement(false_filter, 'groupfilter', attrib={'function': 'level-members', 'level': secondary_group_level})
    # Process each row in CSV
    for row in data:
        member = row['Member']
        user_filter = ET.SubElement(groupfilter_union, 'groupfilter', attrib={
            'expression': create_iscurrentuser_expression(member),
            'function': 'filter'
        })
        set_values = [row[f'Set{i}'] for i in range(1, len(row)) if row.get(f'Set{i}')]
       
        if not set_values:
            ET.SubElement(user_filter, 'groupfilter', attrib={'function': 'empty-level', 'member': secondary_group_level})
        elif len(set_values) == 1:
            ET.SubElement(user_filter, 'groupfilter', attrib={
                'function': 'member',
                'level': secondary_group_level,
                'member': f'"{set_values[0]}"'
            })
        else:
            union_filter = ET.SubElement(user_filter, 'groupfilter', attrib={'function': 'union'})
            for value in set_values:
                ET.SubElement(union_filter, 'groupfilter', attrib={
                    'function': 'member',
                    'level': secondary_group_level,
                    'member': f'"{value}"'
                })
    # Convert to string
    xml_string = ET.tostring(root, encoding='unicode', method='xml')
    xml_string = xml_string.replace("ui-builder='identity-set", "user:ui-builder='identity-set'")
    # Parse and prettify
    parsed_xml = minidom.parseString(xml_string)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")
    # Replace escaped apostrophes in ISCURRENTUSER expressions
    pretty_xml = pretty_xml.replace("ISCURRENTUSER('","ISCURRENTUSER(&apos;")
    pretty_xml = pretty_xml.replace("')","&apos;)")
    # Remove the XML declaration
    pretty_xml = '\n'.join(pretty_xml.split('\n')[1:])
    # Add the user part back
    pretty_xml = str(pretty_xml)
    pretty_xml = pretty_xml.replace('ui-builder="identity-set"', 'user:ui-builder="identity-set"')
    # Write to file
    with open(xml_file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)
       
# File paths
csv_file_path = 'sample-user-access.csv'
xml_file_path = 'testaccess.xml'
# Run the converter
csv_to_xml(csv_file_path, xml_file_path)
print(f"Conversion complete. XML saved to {xml_file_path}")
