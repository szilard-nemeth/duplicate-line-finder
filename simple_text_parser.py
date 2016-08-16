import hashlib
import sys
import os

scriptpath = "../collector.py"
sys.path.append(os.path.abspath(scriptpath))


class Entry():
    def __init__(self, filename, content, line_number):
        self.content = content
        self.filenames = {filename: [line_number]}

    def add_file(self, filename, line_number):
        if filename in self.filenames:
            self.filenames[filename].append(line_number)
        else:
            self.filenames[filename] = [line_number]


class SimpleTextParser():
    extension = '.txt'

    def __init__(self):
        self.hashed_lines = dict()

    def process_line(self, content, file_name, line_number):
        hashed_line = hashlib.md5(content.encode('utf-8')).hexdigest()

        if hashed_line in self.hashed_lines:
            self.hashed_lines[hashed_line].add_file(file_name, line_number)
        else:
            self.hashed_lines[hashed_line] = Entry(file_name, content, line_number)

    def print_all(self):
        duplicate_count = 0
        for i, hashed_line in enumerate(self.hashed_lines):
            if len(self.hashed_lines[hashed_line].filenames) > 1:
                duplicate_count += 1
                print('Found line {0} in multiple files: {1}'.format(self.hashed_lines[hashed_line].content,
                                                                     self.hashed_lines[hashed_line].filenames))
        print('------------------------------------------------')
        print('Summary: ')
        print('Number of duplicates found in all files {0}'.format(duplicate_count))
        print('------------------------------------------------')

    @staticmethod
    def get_deletable_line_numbers(paths, hashed_lines):
        print('Preparing making of "delete line index data" for paths: {0}'.format(paths))
        filenames_and_line_numbers = dict()

        # key: hash,
        # value: Entry
        for key, value in hashed_lines.items():
            # filenames the lines should be deleted from
            for path in paths:
                # store the path if and only if path is part of the filenames list
                # and more than 1 filename belongs to the particular hashed line
                if path in value.filenames and len(value.filenames) > 1:
                    # value[path] contains the line numbers for the matched file
                    if path in filenames_and_line_numbers:
                        filenames_and_line_numbers[path].extend(value.filenames[path])
                    else:
                        filenames_and_line_numbers[path] = value.filenames[path]

        return filenames_and_line_numbers
