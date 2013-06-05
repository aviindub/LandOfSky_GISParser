from os.path import split, join, isfile, splitext, walk
from metadata_analyzer import analyze_metadata, STATUS_COMPLETE, STATUS_INCOMPLETE
import csv

DATA_ROOT = 'data\\'
METADATA_EXTENSIONS = ['.shp.xml']
ALL_EXTENSIONS = set(['.dbf', '.shx', '.sbx', '.shp','.shp.xml', '.sbn', '.prj'])

def catalog_files(cat_ext, dirname, names):
    catalog, all_extensions = cat_ext
    basenames = [n for n in names if isfile(join(dirname, n))]
    if len(basenames) == 0:
        return
    dir_catalog = dict()
    for filename in get_unique_filenames(names):
        fileset_catalog = dict()
        for ext in all_extensions:
            basename = filename + ext
            fileset_catalog[ext] = basename if basename in basenames else None
            if ext in METADATA_EXTENSIONS and fileset_catalog[ext] is not None:
                full_path = join(dirname, basename)
                fileset_catalog['metadata_analysis'], fileset_catalog['metadata_status'] = analyze_metadata(full_path)
        dir_catalog[filename] = fileset_catalog
    catalog[dirname] = dir_catalog


def get_unique_filenames(names):
    return set([strip_multiple_extensions(name) for name in names])


def strip_multiple_extensions(filename):
    filename, ext = splitext(filename)
    if ext is None or ext is '':
        return filename
    return strip_multiple_extensions(filename)


def get_extensions(extensions, dirname, names):
    for name in names:
        basename, ext = splitext(name)
        if ext == '.xml':
            ext = '.shp.xml'
            basename, _extra_ext = splitext(name)
        if ext not in extensions and isfile(join(dirname, name)):
            extensions.add(ext)


def get_all_extensions(root_path, use_predefined=False):
    if use_predefined:
        return ALL_EXTENSIONS
    extensions = set()
    walk(root_path, get_extensions, extensions)
    return extensions


def output_missing_files_report(catalog):
    missing_files_rows = list()
    for dirname, directory in catalog.iteritems():
        for filename, fileset in directory.iteritems():
            if has_missing_files(fileset):
                row = dict()
                row['file_name'] = join(dirname, filename)
                for ext, full_filename in fileset.iteritems():
                    if ext is not 'metadata_analysis':
                        if full_filename is None:
                            row[ext] = 'X'
                        else:
                            row[ext] = ''
                missing_files_rows.append(row)
    field_names = ALL_EXTENSIONS.copy()
    field_names.add('file_name')
    with csv.DictWriter('missing_files_report.csv', field_names) as writer:
        for row in missing_files_rows:
            writer.writerow(row)


def output_incomplete_metadata_report(catalog):
    metadata_rows = list()
    for dirname, directory in catalog.iteritems():
        for filename, fileset in directory.iteritems():
            metadata_report = fileset['metadata_report']
            if len(metadata_report) > 0:
                metadata_rows.append(join(dirname, filename))
                for r in metadata_report:
                    metadata_rows.append([''] + list(r))
    with csv.writer('incomplete_metadata_report') as writer:
        writer.writerow(['file', 'XML element', 'text'])
        for row in metadata_rows:
            writer.writerow(row)


def output_complete_metadata_report(catalog):
    metadata_rows = list()
    for dirname, directory in catalog.iteritems():
        for filename, fileset in directory.iteritems():
            metadata_report = fileset['metadata_report']
            if len(metadata_report) is 0 and fileset['.shp.xml'] is not None:
                pass
                # TODO: write catalog of usable data 


def has_missing_files(fileset):
    for ext, full_filename in fileset.iteritems():
        if ext is not 'metadata_analysis' and full_filename is None:
            return true


def output_csv(catalog):
    ONE_CELL_ROW = '\"{}\"\n'
    TWO_CELL_ROW = '\"{}\",\"{}\"\n'

    csv_string = ''
    for dirname, directory in catalog.iteritems():
        for filename, fileset in directory.iteritems():
            csv_string += '\n' + TWO_CELL_ROW.format('Directory:', 'Filename:')
            csv_string += TWO_CELL_ROW.format(dirname, filename)
            missing_files = 'Missing Files:'
            for ext, full_filename in fileset.iteritems():
                if ext is not 'metadata_analysis' and full_filename is None:
                    missing_files += ' {},'.format(ext)
            if missing_files is 'Missing Files:':
                missing_files = 'Missing Files: None'
            csv_string += ONE_CELL_ROW.format(missing_files)
            csv_string += '\n' + ONE_CELL_ROW.format('Missing Metadata Elements:')
            csv_string += TWO_CELL_ROW.format('Tag:', 'Text:')
            if 'metadata_analysis' in fileset:
                for tag, text in fileset['metadata_analysis']:
                    csv_string += TWO_CELL_ROW.format(tag, text)
            else:
                csv_string += ONE_CELL_ROW.format("missing metadata file")

    with open('missing_data_report.csv', 'w') as outfile:
        outfile.write(csv_string)


def main():
    # print 'starting'
    catalog = dict()
    all_extensions = get_all_extensions(DATA_ROOT)
    # print all_extensions
    walk(DATA_ROOT, catalog_files, (catalog, all_extensions))
    output_csv(catalog)
    # print catalog
    # catalog[directory_path][filename][extension]
    # catalog[directory_path][filename]['metadata_analysis']
    # catalog[directory_path][filename]['metadata_status']
    # return catalog


if __name__ == "__main__":
    main()