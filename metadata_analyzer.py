import xml.etree.ElementTree as ET

def analyze_metadata(file_path):
    tree = ET.parse(file_path)
    return catalog_missing_elements(tree)


def catalog_missing_elements():
    root = tree.getroot()


if __name__ = '__main__':
    print analyze_metadata('data/CountyData/buncosde_BUNCOSDE_property.shp.xml')