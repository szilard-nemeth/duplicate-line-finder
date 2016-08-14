import codecs
import os


class FileReader:
    def __init__(self, parser, src_dir, dest_dir):
        self.parser = parser
        self.src_dir = src_dir
        self.dest_dir = dest_dir

        self.unique_items = 0
        assert self.parser.extension

    def collect_and_print_lines(self):
        self.collect_lines()
        self.parser.print_all()

    def collect_lines(self):
        self.unique_items = 0
        for file_name in os.listdir(self.src_dir):
            if file_name.endswith(self.parser.extension):
                file_path = os.path.join(self.src_dir, file_name)
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
        for file_name in delete_from_files.keys():
            file_name = os.path.join(self.src_dir, file_name)

            line_numbers_to_delete = delete_from_files[file_name]
            print("Will remove {0} lines from file {1}".format(len(line_numbers_to_delete), file_name))

            with open(file_name, "r", encoding='utf-8', errors='ignore') as old_file, \
                    open(file_name + "_updated", "w", encoding='utf-8', errors='ignore') as new_file:
                for line_idx, line in enumerate(old_file):
                    line_number = line_idx + 1
                    if not line_number in line_numbers_to_delete:
                        new_file.write(line)
                    else:
                        print('Removing line {0} from {1}'.format(line_number, file_name))