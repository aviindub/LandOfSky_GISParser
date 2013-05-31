import xml.etree.ElementTree as ET
from xml.sax.handler import ContentHandler
from xml.sax import make_parser as make_validator_parser

INCOMPLETE_TARGET_STRINGS = ['REQUIRED']
COMPLETE_TARGET_ELEMENTS = ['title', 'abstract', ]


def analyze_metadata(file_path):
    if not valid_xml(file_path):
        return 0
    xml_tree = ET.parse(file_path)
    incomplete_catalog = catalog_missing_elements(xml_tree)
    if len(incomplete_catalog) > 0:
        return incomplete_catalog
    else:
        return catalog_complete_metadata(xml_tree)


def valid_xml(file_path):
    try:
        parse_file(file_path)
    except Exception, e:
        print e
        return False
    return True


def parse_file(file_path):
    parser = make_validator_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file_path)


def catalog_missing_elements(xml_tree):
    catalog = list()
    for element in xml_tree.iter():
        if element.text is not None and element_is_incomplete(element):
            catalog.append((element.tag, element.text))
    return catalog


def catalog_complete_metadata(xml_tree):
    pass


def element_is_incomplete(element):
    for target in INCOMPLETE_TARGET_STRINGS:
        if target in element.text:
            return True
    return False


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
    if catalog is 0:
        print 'validation falied'
    else:
        with open('incomplete_metadata_report.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for row in catalog: writer.writerow(row)
            print 'wrote analysis file incomplete_metadata_report.csv'
