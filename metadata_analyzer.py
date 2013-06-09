
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
# COMPLETE_TARGET_ELEMENTS = [u'resTitle', u'abstract', u'purpose', u'supplinf', 
#     u'themekey', u'placekey', u'datacred', u'origin', u'accconst', u'useconst',
#     u'westbc', u'eastbc', u'northbc', u'southbc', u'leftbc', u'rightbc',
#     u'bottombc', u'topbc', u'progress', u'update', u'current', u'begdate',
#     u'begtime', u'enddate', u'endtime', u'pubdate', u'CreaDate', u'SyncDate']
COMPLETE_TARGET_ELEMENTS = ['resTitle', 'abstract', 'purpose', 'supplinf', 
    'themekey', 'placekey', 'datacred', 'origin', 'accconst', 'useconst',
    'westbc', 'eastbc', 'northbc', 'southbc', 'leftbc', 'rightbc',
    'bottombc', 'topbc', 'progress', 'update', 'current', 'begdate',
    'begtime', 'enddate', 'endtime', 'pubdate', 'CreaDate', 'SyncDate']
STATUS_INCOMPLETE = 'incomplete metadata'
STATUS_COMPLETE = 'complete metadata'
STATUS_VALIDATION_FAILURE = 'validation failure'

def analyze_metadata(file_path):
    print 'analyzing ' + file_path
    if not valid_xml(file_path):
        print '**XML validation failure: ' + file_path
        return None, STATUS_VALIDATION_FAILURE
    xml_tree = ET.parse(file_path)
    incomplete_catalog = [e for e in xml_tree.iter() if is_required_incomplete(e)]
    # print incomplete_catalog
    if len(incomplete_catalog) > 0:
        print 'INCOMPLETE'
        # print incomplete_catalog, STATUS_INCOMPLETE
        return incomplete_catalog, STATUS_INCOMPLETE
    else:
        complete_catalog = [e for e in xml_tree.iter() if is_target(e)]
        print 'COMPLETE'
        # print complete_catalog, STATUS_COMPLETE
        return complete_catalog, STATUS_COMPLETE

def is_required_incomplete(element):
    if element.text is not None:
        for target in INCOMPLETE_TARGET_STRINGS:
            # print target +' '+ element.text
            # print '{} {}'.format(type(target), type(element.text))
            if str(target) in str(element.text):
                return True
    return False


def is_target(element):
    if element.text is not None:
        for target in COMPLETE_TARGET_ELEMENTS:
            # if target == u'abstract': print 'target: {} tag: {}'.format(target, element.tag)
            if element.tag == target:
                return True
    return False


def valid_xml(file_path):
    parser = make_validator_parser()
    parser.setContentHandler(ContentHandler())
    try:
        parser.parse(file_path)
    except Exception, e:
        print e
        return False
    return True


if __name__ == '__main__':
    '''for testing only'''

    import csv
    TEST_FILE = 'data/CountyData/buncosde_BUNCOSDE_property.shp.xml'
    # TEST_FILE = 'data/CountyData/BuncombeCo_bridges.shp.xml'
    # TEST_FILE = 'data/CountyData/parcels_2002.shp.xml'
    catalog, status = analyze_metadata(TEST_FILE)
    if catalog is None:
        print 'validation falied'
    else:
        print status
        print catalog
        with open('incomplete_metadata_report.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for row in catalog: writer.writerow(row)
            print 'wrote analysis file incomplete_metadata_report.csv'
