import xml.etree.ElementTree as ET
import csv
from collections import OrderedDict
import re
def parse_xml_to_csv(xml_file_path, output_file):
    # Read XML content from file
    with open(xml_file_path, 'r') as file:
        xml_string = file.read()
    # Remove namespace prefixes
    xml_string = re.sub(r'\sxmlns:.?=[""].?[""]', '', xml_string, flags=re.MULTILINE)
    xml_string = re.sub(r'\w+:', '', xml_string)
   
    root = ET.fromstring(xml_string)
   
    data = OrderedDict()
    data['Member'] = []
   
    for groupfilter in root.findall(".//groupfilter[@expression]"):
        expression = groupfilter.get('expression')
        if expression and expression.startswith('ISCURRENTUSER'):
            user = expression.split("'")[1].split('\\')[1]
            data['Member'].append(user)
           
            set_values = []
            for member_filter in groupfilter.findall(".//groupfilter[@function='member']"):
                member = member_filter.get('member')
                if member:
                    set_value = member.strip('"')
                    set_values.append(set_value)
           
            for i, value in enumerate(set_values, 1):
                if f'Set{i}' not in data:
                    data[f'Set{i}'] = [''] * (len(data['Member']) - 1)
                data[f'Set{i}'].append(value)
           
            # Fill in empty values for sets that don't have a value for this user
            for key in data:
                if key != 'Member' and len(data[key]) < len(data['Member']):
                    data[key].append('')
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))
# File paths
xml_file_path = 'access.xml'
csv_output_path = 'output.csv'
# Run the parser
parse_xml_to_csv(xml_file_path, csv_output_path)
print(f"Parsing complete. Output saved to {csv_output_path}")

