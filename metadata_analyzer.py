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


if __name__ == '__main__':
    print analyze_metadata('data/CountyData/buncosde_BUNCOSDE_property.shp.xml')