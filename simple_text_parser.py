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
            occurences_of_line = len(value.filenames)
            line_found_in_more_than_one_files = occurences_of_line > 1
            # Check first that more than 1 filename contains the particular line
            if not line_found_in_more_than_one_files:
                continue

            # check if all found filenames for a line is part of the deletable file paths
            if all((fn in paths for fn in value.filenames)):
                marked_deleted_count = 0

                filtered_paths = {fn: paths[fn] for fn in value.filenames}
                #sort the dictionary by the file_props.defined_as_file property
                #True valued defined_as_file comes first,
                #this means that the items defined as separate files takes precedence in the marking process
                sorted_paths = sorted(filtered_paths, key=lambda x: filtered_paths[x].defined_as_file, reverse=True)
                for file_name in sorted_paths:
                    filenames_and_line_numbers[file_name] = value.filenames[file_name]
                    marked_deleted_count += 1

                    #SHOULD ALWAYS KEEP ONE OCCURENCE AT LEAST IN ALL FILES!
                    #In other words: the line should be mark for deletion at a maximum of (occurences_of_line - 1) times
                    #In other words2: mark items specified as part of a folder as long we have only 1 occurence remaining
                    if marked_deleted_count == (occurences_of_line - 1):
                        break

            else:
                # filenames the lines should be deleted from
                for path, file_props in paths.items():
                    # store the path if path is part of the filenames list
                    if path in value.filenames:
                        # value[path] contains the line numbers for the matched file
                        if path in filenames_and_line_numbers:
                            filenames_and_line_numbers[path].extend(value.filenames[path])
                        else:
                            filenames_and_line_numbers[path] = value.filenames[path]

        return filenames_and_line_numbers
