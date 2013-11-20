from os.path import split, join, isfile, splitext, walk
import metadata_analyzer
import csv

DATA_ROOT = 'data\\'
METADATA_EXTENSIONS = ['.shp.xml']
ALL_EXTENSIONS = set(['.dbf', '.shx', '.sbx', '.shp','.shp.xml', '.sbn', '.prj'])
STATUS_MISSING = 'missing metadata file'


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
            if ext in METADATA_EXTENSIONS:
                if fileset_catalog[ext] is not None:
                    full_path = join(dirname, basename)
                    fileset_catalog['metadata_analysis'], fileset_catalog['metadata_status'] = metadata_analyzer.analyze_metadata(full_path)
                    # print fileset_catalog['metadata_analysis']
                    # print fileset_catalog['metadata_status']
                else:
                    # print 'hit else'
                    fileset_catalog['metadata_analysis'] = None
                    fileset_catalog['metadata_status'] = STATUS_MISSING
        dir_catalog[filename] = fileset_catalog
    catalog[dirname] = dir_catalog


def get_unique_filenames(names):
    return set([strip_multiple_extensions(name) for name in names
        if name.endswith(tuple(ALL_EXTENSIONS))])


def strip_multiple_extensions(filename):
    filename, ext = splitext(filename)
    if ext is None or ext == '':
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


def output_missing_files_report(catalog):
    missing_files_rows = list()
    for dirname, directory in catalog.iteritems():
        for filename, fileset in directory.iteritems():
            if has_missing_files(fileset):
                row = dict()
                row['file_name'] = join(dirname, filename)
                for ext, full_filename in fileset.iteritems():
                    if ext != 'metadata_analysis' and ext != 'metadata_status':
                        if full_filename is None:
                            row[ext] = 'X'
                        else:
                            row[ext] = ''
                missing_files_rows.append(row)
    field_names = ['file_name']
    field_names.extend(ALL_EXTENSIONS)
    with open('missing_files_report.csv', 'w') as out_file:
        writer = csv.DictWriter(out_file, field_names)
        writer.writeheader()
        for row in missing_files_rows:
            writer.writerow(row)


def output_incomplete_metadata_report(catalog):
    metadata_rows = list()
    for dirname, directory in catalog.iteritems():
        for filename, fileset in directory.iteritems():
            metadata_report = fileset['metadata_analysis']
            if metadata_report is not None and len(metadata_report) > 0 \
              and fileset['metadata_status'] == metadata_analyzer.STATUS_INCOMPLETE:
                full_filename = join(dirname, filename)
                row = [full_filename]
                for element in metadata_report:
                    row.append(element.tag)
                metadata_rows.append(row)
    with open('incomplete_metadata_report.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for row in metadata_rows:
            writer.writerow(row)


def output_complete_metadata_report(catalog):
    with open('complete_metadata_report.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for dirname, directory in catalog.iteritems():
            for filename, fileset in directory.iteritems():
                metadata_report = fileset['metadata_analysis']
                if fileset['metadata_status'] == metadata_analyzer.STATUS_COMPLETE \
                  and len(metadata_report) > 0 and fileset['.shp.xml'] is not None:
                    for element in metadata_report:
                        writer.writerow([filename, element.tag, element.text])


def has_missing_files(fileset):
    for ext, full_filename in fileset.iteritems():
        if ext != 'metadata_analysis' and full_filename is None:
            return True


def main():
    print 'starting'
    catalog = dict()
    walk(DATA_ROOT, catalog_files, (catalog, ALL_EXTENSIONS))
    output_missing_files_report(catalog)
    output_incomplete_metadata_report(catalog)
    output_complete_metadata_report(catalog)
    # catalog[directory_path][filename][extension]
    # catalog[directory_path][filename]['metadata_analysis']
    # catalog[directory_path][filename]['metadata_status']


if __name__ == "__main__":
    main()