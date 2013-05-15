from os.path import split, join, isfile, splitext, walk
from metadata_analyzer import analyze_metadata

DATA_ROOT = 'data/'
METADATA_EXTENSIONS = ['.shp.xml']

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
                fileset_catalog['metadata_analysis'] = analyze_metadata(full_path)
        dir_catalog[filename] = fileset_catalog
    catalog[dirname] = dir_catalog


def get_unique_filenames(names):
    return set([filename for filename, _ext in
        [splitext(filename) for filename, _ext in 
        [splitext(n) for n in names]]])


def get_extensions(extensions, dirname, names):
    for name in names:
        basename, ext = splitext(name)
        if ext == '.xml':
            ext = '.shp.xml'
            basename, _extra_ext = splitext(name)
        if ext not in extensions and isfile(join(dirname, name)):
            extensions.add(ext)


def get_all_extensions(root_path):
    extensions = set()
    walk(root_path, get_extensions, extensions)
    return extensions


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
            csv_string += TWO_CELL_ROW.format('Tag', 'Text')
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
    # return catalog


if __name__ == "__main__":
    main()