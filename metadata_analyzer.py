import xml.etree.ElementTree as ET

TARGET_STRINGS = ['REQUIRED']


def analyze_metadata(file_path):
    tree = ET.parse(file_path)
    return catalog_missing_elements(tree)


def catalog_missing_elements(tree):
    catalog = list()
    for element in tree.iter():
        if element.text is not None:
            for target in TARGET_STRINGS:
                if target in element.text:
                    catalog.append((element.tag, element.text))
    return catalog


def csv_string(catalog):
    csv_output = ''
    for row in catalog:
        csv_output += '\"{}\",\"{}\"\n'.format(row[0],row[1])
    return csv_output


if __name__ == '__main__':
    catalog = analyze_metadata('data/CountyData/buncosde_BUNCOSDE_property.shp.xml')
    with open('analysis_test.csv', 'w') as outfile:
        outfile.write('\"tag\",\"text\"\n')
        outfile.write(csv_string(catalog))
