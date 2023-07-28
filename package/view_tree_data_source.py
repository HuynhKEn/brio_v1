import os
from path import UtilsRoot

def get_directory_info(directory):
    num_files = 0
    total_size = 0
    num_subdirectories = 0
    files_in_each_directory = {}

    for entry in os.scandir(directory):
        if entry.is_file():
            num_files += 1
            total_size += entry.stat().st_size
        elif entry.is_dir():
            subdir = os.path.join(directory, entry.name)
            sub_num_files, sub_total_size, sub_num_subdirectories, sub_files_in_each_directory = get_directory_info(subdir)
            num_files += sub_num_files
            total_size += sub_total_size
            num_subdirectories += sub_num_subdirectories + 1
            files_in_each_directory[entry.name] = sub_num_files + len(sub_files_in_each_directory)

    return num_files, total_size, num_subdirectories, files_in_each_directory

def display_file_info(file_path):
    line_count = 0
    longest_line = ''
    shortest_line = None

    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            line_count += 1

            line = line.rstrip('\n')

            if shortest_line is None or len(line) < len(shortest_line):
                shortest_line = line

            if len(line) > len(longest_line):
                longest_line = line

    print(f"Number of lines: {line_count}")
    # print(f"Longest line: {longest_line}")
    # print(f"Shortest line: {shortest_line}")

def display_directory_info(directory):
    num_files, total_size, num_subdirectories, files_in_each_directory = get_directory_info(directory)
    print(f"Number of files: {num_files}")
    print(f"Total size: {total_size} bytes")
    print(f"Number of subdirectories: {num_subdirectories}")
    print(f"Number file of subdirectories: {files_in_each_directory}")


directory_path = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'random_data')
file_path_source = os.path.join(UtilsRoot.get_root_path(), 'package', 'cnndm', 'source_target', 'train.source')

#display_file_info(file_path_source)
display_directory_info(directory_path)

