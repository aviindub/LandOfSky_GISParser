from os.path import split, join, isfile, splitext, walk

DATA_ROOT = 'data/'

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
            if basename in basenames:
                fileset_catalog[ext] = basename
            else:
                fileset_catalog[ext] = None
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


def main():
    # print 'starting'
    catalog = dict()
    all_extensions = get_all_extensions(DATA_ROOT)
    # print all_extensions
    walk(DATA_ROOT, catalog_files, (catalog, all_extensions))
    print catalog


if __name__ == "__main__":
    main()