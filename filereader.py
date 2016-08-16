import codecs
import os
from helper import Helper


class FileReader:
    def __init__(self, parser, src_dir, dest_dir):
        self.parser = parser
        self.src_dir = src_dir
        self.dest_dir = dest_dir

        self.unique_items = 0
        assert self.parser.extension

    def get_file_paths(self, from_path):
        print('PRINTING FILE TREE FROM PATH {0}'.format(from_path))

        file_paths = []
        for root, dirs, files in os.walk(from_path):
            level = root.replace(from_path, '').count(os.sep)
            indent = ' ' * 4 * level
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))
                if f.endswith(self.parser.extension):
                    file_paths.append(os.path.join(root, f))

        print('------------------------------------------------')
        print('FOUND {0} FILES WITH MATCHING EXTENSION(S): {1}'.format(len(file_paths), self.parser.extension))
        print('------------------------------------------------')

        return file_paths

    def collect_and_print_lines(self, file_paths):
        self.collect_lines(file_paths)
        self.parser.print_all()

    def collect_lines(self, file_paths):
        self.unique_items = 0
        for file_path in file_paths:
            print('Processing file: {0}'.format(file_path))

            last_read_line_count = 0
            with open(file_path, "r", encoding='utf-8', errors='ignore') as file:
                for line_idx, line in enumerate(file):
                    # line_idx is starting from 0
                    line_number = line_idx + 1
                    self.parser.process_line(line, file_path, line_number)
                    last_read_line_count = line_number

            print("Found {0} elements in file {1}".format(str(last_read_line_count), file_path))

            unique_items_length_old = self.unique_items
            self.unique_items += last_read_line_count
            print('Changed count of unique items (sum of all files): {0} --> {1}'.format(unique_items_length_old,
                                                                                         self.unique_items))
        print('Found {0} unique elements in ALL FILES'.format(str(self.unique_items)))

    def delete_lines_from(self, delete_from_files):

        if not os.path.exists(self.dest_dir):
            print('Creating not existing destination directory: {0}'.format(self.dest_dir))
            os.makedirs(self.dest_dir)
        for old_file_path in delete_from_files.keys():
            line_numbers_to_delete = delete_from_files[old_file_path]
            print('------------------------------------------------')
            print('------------------------------------------------')
            print('Processing duplicate skipping from file: {0}'.format(old_file_path))
            print("Will skip {0} lines from file {1}".format(len(line_numbers_to_delete), old_file_path))
            print('------------------------------------------------')
            print('------------------------------------------------')

            new_file_path = old_file_path.replace(self.src_dir, self.dest_dir)
            Helper.make_dirs(os.path.dirname(new_file_path))

            with open(old_file_path, "r", encoding='utf-8', errors='ignore') as old_file, \
                    open(new_file_path, "w", encoding='utf-8', errors='ignore') as new_file:
                for line_idx, line in enumerate(old_file):
                    line_number = line_idx + 1
                    if not line_number in line_numbers_to_delete:
                        new_file.write(line)
                    else:
                        print('Skipping line {0} from {1}'.format(line_number, new_file_path))

            print('------------------------------------------------')
            print('------------------------------------------------')

    def get_all_files_from_paths(self, processable_paths):
        file_paths = set()

        for path in processable_paths:
            if os.path.isdir(path):
                for dirname, dirnames, filenames in os.walk(path):
                    for subdirname in dirnames:
                        #nothing to do now
                        pass

                    for filename in filenames:
                        file_paths.add(os.path.join(dirname, filename))
            else:
                file_paths.add(path)

        return file_paths
