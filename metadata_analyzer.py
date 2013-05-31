import xml.etree.ElementTree as ET
from xml.sax.handler import ContentHandler
from xml.sax import make_parser as make_validator_parser

INCOMPLETE_TARGET_STRINGS = ['REQUIRED']
COMPLETE_TARGET_ELEMENTS = ['title', 'abstract', ]


def analyze_metadata(file_path):
    if not valid_xml(file_path):
        return None
    xml_tree = ET.parse(file_path)
    incomplete_catalog = catalog_missing_elements(xml_tree)
    if any(incomplete_catalog):
        return incomplete_catalog
    else:
        return catalog_complete_elements(xml_tree)


def valid_xml(file_path):
    try:
        parse_file_for_validation(file_path)
    except Exception, e:
        print e
        return False
    return True


def parse_file_for_validation(file_path):
    parser = make_validator_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file_path)


def catalog_validated_elements(xml_tree, target_strings):
    '''catalogs elements that contain a string in target_strings'''
    
    catalog = list()
    for element in xml_tree.iter():
        if element.text is not None and check_element_text(element.text, target_strings):
            catalog.append((element.tag, element.text))
    return catalog


def check_element_text(element_text, target_strings):
    for target in target_strings:
        if target in element_text:
            return True
    return False    


def catalog_missing_elements(xml_tree):
    return catalog_validated_elements(xml_tree, INCOMPLETE_TARGET_STRINGS)


def catalog_complete_elements(xml_tree):
    return catalog_validated_elements(xml_tree, COMPLETE_TARGET_STRINGS)


def csv_string(catalog):
    csv_output = ''
    for row in catalog:
        csv_output += '\"{}\",\"{}\"\n'.format(row[0],row[1])
    return csv_output


if __name__ == '__main__':
    '''for testing only'''

    import csv
    TEST_FILE = 'data/CountyData/buncosde_BUNCOSDE_property.shp.xml'
    # TEST_FILE = 'data/CountyData/BuncombeCo_bridges.shp.xml'
    # TEST_FILE = 'data/CountyData/parcels_2002.shp.xml'
    catalog = analyze_metadata(TEST_FILE)
    if catalog is None:
        print 'validation falied'
    else:
        with open('incomplete_metadata_report.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for row in catalog: writer.writerow(row)
            print 'wrote analysis file incomplete_metadata_report.csv'
