
"""
Data set title
Abstract
Supplemental information/description/summary
keywords/tags
credits/originators
use limitations
extent, projection, and scale??
status and time period/publication date/currency date

<resTitle Sync="TRUE">BuncombeCo_TransitLikelyDestinations_RetailEmpHospitalMultiFam</resTitle>
<abstract>Buncombe County community facilities, retail and multi-family housing destinations which might be of particular interest to transit riders</abstract>
<purpose>This file was created for transportation planning and verifying demographic data purposes at Land-of-Sky Regional Council</purpose>
<supplinf>Facilities listed based on Land-of-Sky Housing Directory, City of Asheville website search and Google search; geocoded using bullkgeocoder.com</supplinf>
<themekey>grocery stores, health care, hospitals, employment training, multi-family residential, mixed use developments</themekey>
<placekey>Buncombe County, Asheville, Weaverville, Black Mountain, Swannanoa, Biltmore Forest</placekey>
<datacred>Land-of-Sky Regional Council December 2012; geocoded using www.BulkGeocoder.com</datacred>
<origin>REQUIRED: The name of an organization or individual that developed the data set.</origin>
<pubdate>REQUIRED: The date when the data set is published or otherwise made available for release.</pubdate>
<accconst>Open use.  There might be accuracy issues with the dataset (not all facilities listed, some potential errors in geocoding and numbers of residential units)</accconst>
<useconst>Open use.  There might be accuracy issues with the dataset (not all facilities listed, some potential errors in geocoding and numbers of residential units)</useconst>
<westbc Sync="TRUE">-82.838249</westbc>
<eastbc Sync="TRUE">-82.320895</eastbc>
<northbc Sync="TRUE">35.704068</northbc>
<southbc Sync="TRUE">-82.643538</southbc>
<leftbc Sync="TRUE">-82.838249</leftbc>
<rightbc Sync="TRUE">-82.320895</rightbc>
<bottombc Sync="TRUE">-82.643538</bottombc>
<topbc Sync="TRUE">35.704068</topbc>
<progress>To be updated as needed, preferably once every five years prior to LRTP update</progress>
<update>At start of FBRMPO LRTP update, every five years</update>
<current>ground condition</current>
<begdate>19990402</begdate>
<begtime>09000000</begtime>
<enddate>19990413</enddate>
<endtime>15000000</endtime>            
<pubdate>REQUIRED: The date when the data set is published or otherwise made available for release.</pubdate>
<CreaDate>20100819</CreaDate>
<SyncDate>20120530</SyncDate>

Data set title
    resTitle

Abstract
    abstract

Supplemental information/description/summary
    purpose
    supplinf

keywords/tags
    themekey
    placekey

credits/originators
    datacred
    origin

use limitations
    accconst
    useconst

extent
    westbc
    eastbc
    northbc
    southbc

projection
    leftbc
    rightbc
    bottombc
    topbc

scale??

status
    progress
    update

time period
    current
    begdate
    begtime
    enddate
    endtime

publication date
    pubdate
    CreaDate

currency date
    SyncDate

"""

import xml.etree.ElementTree as ET
from xml.sax.handler import ContentHandler
from xml.sax import make_parser as make_validator_parser

INCOMPLETE_TARGET_STRINGS = ['REQUIRED']
COMPLETE_TARGET_ELEMENTS = ['resTitle', 'abstract', 'purpose', 'supplinf', 
    'themekey', 'placekey', 'datacred', 'origin', 'accconst', 'useconst',
    'westbc', 'eastbc', 'northbc', 'southbc', 'leftbc', 'rightbc',
    'bottombc', 'topbc', 'progress', 'update', 'current', 'begdate',
    'begtime', 'enddate', 'endtime', 'pubdate', 'CreaDate', 'SyncDate']
STATUS_INCOMPLETE = 'no'
STATUS_COMPLETE = 'yes'

def analyze_metadata(file_path):
    if not valid_xml(file_path):
        return None
    xml_tree = ET.parse(file_path)
    #incomplete_catalog = catalog_validated_elements(xml_tree, INCOMPLETE_TARGET_STRINGS)
    incomplete_catalog = [e for e in xml_tree.iter() if is_required_incomplete(e)]
    if any(incomplete_catalog):
        return incomplete_catalog, STATUS_INCOMPLETE
    else:
        #return catalog_validated_elements(xml_tree, COMPLETE_TARGET_ELEMENTS)
        complete_catalog = [e for e in xml_tree.iter() if is_target(e)]
        return complete_catalog, STATUS_COMPLETE


def is_required_incomplete(element):
    if element.text is not None:
        for target in INCOMPLETE_TARGET_STRINGS:
            if target in element.text:
                return True
    return False


def is_target(element):
    if element.text is not None:
        for target in COMPLETE_TARGET_ELEMENTS:
            if element.tag is target:
                return True
    return False


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
