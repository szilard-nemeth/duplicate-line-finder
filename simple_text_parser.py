import codecs
import hashlib
import sys
import os

scriptpath = "../collector.py"
sys.path.append(os.path.abspath(scriptpath))
import filereader


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
        self.last_read_line_count = 0

    def parse(self, file_name):
        self.last_read_line_count = 0
        with codecs.open(file_name, "r", encoding='utf-8', errors='ignore') as file:
            for line_idx, line in enumerate(file):
                # line_idx is starting from 0
                line_number = line_idx + 1
                self.last_read_line_count = line_number
                hashed_line = hashlib.md5(line.encode('utf-8')).hexdigest()

                line_number = line_idx + 1
                if hashed_line in self.hashed_lines:
                    self.hashed_lines[hashed_line].add_file(file_name, line_number)
                else:
                    self.hashed_lines[hashed_line] = Entry(file_name, line, line_number)

    def get_element_count(self):
        return self.last_read_line_count

    def print_all(self):
        for i, hashed_line in enumerate(self.hashed_lines):
            if len(self.hashed_lines[hashed_line].filenames) > 1:
                print('Found line {0} in multiple files: {1}'.format(self.hashed_lines[hashed_line].content,
                                                                     self.hashed_lines[hashed_line].filenames))

    @staticmethod
    def get_deletable_line_numbers(processable_file_names, hashed_lines):
        print('Preparing making of "delete line index data" for files: {0}'.format(processable_file_names))
        filenames_and_line_numbers = dict()

        # key: hash, value: Entry
        for key, value in hashed_lines.items():
            #filenames the lines should be deleted from
            for file_name in processable_file_names:
                #processable_file_name is part of filenames list and there is more than 1 filename for the particular hash
                if file_name in value.filenames and len(value.filenames) > 1:
                    ##value[file_name] contains the line numbers for the matched file
                    if file_name in filenames_and_line_numbers:
                        filenames_and_line_numbers[file_name].extend(value.filenames[file_name])
                    else:
                        filenames_and_line_numbers[file_name] = value.filenames[file_name]

        return filenames_and_line_numbers


if __name__ == "__main__":
    arg_parser = filereader.FileReader.setup_parser(SimpleTextParser.extension)
    argsDict = filereader.FileReader.create_args_dict(arg_parser)
    reader = filereader.FileReader(SimpleTextParser(), argsDict['srcdir'], argsDict['destdir'])
    reader.collect_and_print_lines()

    if 'delete_duplicate_lines_from' in argsDict:
        processable_file_names = argsDict['delete_duplicate_lines_from']
        filenames_to_line_numbers_mapping = SimpleTextParser.get_deletable_line_numbers(processable_file_names,
                                                                                        reader.parser.hashed_lines)
        reader.delete_lines_from(filenames_to_line_numbers_mapping)
