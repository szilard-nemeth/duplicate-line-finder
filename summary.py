from pprint import pprint


class Summary:

    def store_unique_items_count(self, unique_items_count):
        self.unique_items_count = unique_items_count
        #print('Found {0} unique elements in ALL FILES'.format(str(self.unique_items)))

    def store_all_files_checked(self, all_files_checked):
        self.all_files_checked = all_files_checked

    def store_info_processed_hashed_lines(self, hashed_lines):
        self.affected_file_count = len(hashed_lines)

        self.count_of_lines_to_delete = 0
        for line_numbers in hashed_lines.values():
            self.count_of_lines_to_delete += len(line_numbers)


    def process_lines_dict(self, lines_dict):
        self.duplicate_lines = 0
        self.duplicate_line_occurences = 0
        for i, line in enumerate(lines_dict):
            line_occurences = len(lines_dict[line].filenames)
            if line_occurences > 1:
                self.duplicate_line_occurences += line_occurences
                self.duplicate_lines += 1
                print('Found line {0} in multiple files: {1}'.format(lines_dict[line].content,
                                                                     lines_dict[line].filenames))

    def print_warning_message(self):
        print('WARNING!! '
              'Based on the provided paths, '
              '{0} files will be affected by duplicate line deletion and '
              '{1} lines will be deleted'
              .format(self.affected_file_count, self.count_of_lines_to_delete))


    def print(self):
        print('------------------------------------------------')
        print('------------------------------------------------')
        print('-------------------SUMMARY----------------------')
        print('--------------ALL FILES CHECKED-----------------')
        pprint(self.all_files_checked)
        print('------------------------------------------------')
        print('------------------------------------------------')
        print('Number of unique lines found in total: {0}'.format(self.unique_items_count))
        print('Number of all duplicate line occurences found in all files {0}'.format(self.duplicate_line_occurences))
        print('Number of duplicate distinct lines found in total {0}'.format(self.duplicate_lines))
        print('Number of affected files: {0}'.format(self.affected_file_count))
        print('Number of lines to delete: {0}'.format(self.count_of_lines_to_delete))
        print('------------------------------------------------')
        print('------------------------------------------------')
