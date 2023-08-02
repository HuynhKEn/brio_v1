
import os
import glob
import shutil
import random
import threading
import random_get_files
import concurrent.futures
import transform_datafiles
from path import UtilsRoot

def copy_files(file_list):
    for file in file_list:
        source_path, destination_dir = file
        shutil.copy(source_path, destination_dir)

class Preprocess:
    def __init__(self, lang, kind):
        
        print("Call")

        self.lang = lang
        self.type = kind
        if kind == "parent":
            self.part1_dir = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'original_root', 'train')
            self.part2_dir = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'original_root', 'val')
            self.part3_dir = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'original_root', 'test')
        elif kind == "sub":
            self.part1_dir = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'random_data', 'train')
            self.part2_dir = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'random_data', 'val')
            self.part3_dir = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'random_data', 'test')

        self.path_source_target = os.path.join(UtilsRoot.get_root_path(),'package', 'cnndm', 'source_target')

    def random_dataset(self, number_random, train_ratio=0.7, val_ratio=0.2):
        part_dir_random = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'original_root', 'train')
        part_dir_out_random = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'random_data')

        random_get_files.run(part_dir_random, part_dir_out_random, number_random, train_ratio, val_ratio)



    def split_dataset(self, dir_src, train_ratio=0.7, val_ratio=0.2):
        """
            This function splits total raw data into train, val, and test sets.
            Warning: used for the original dataset.
            Parameters:
            dir_src (str): Source root directory.
            train_ratio (float): Train ratio.
            val_ratio: (float): Validation ratio.
            test_ratio: (float): Automatically calculated.
            
            Returns: Void -> Splits to directories /package/source/{train/val/test/}
        """

        file_list = glob.glob(os.path.join(dir_src, "*"))
        random.shuffle(file_list)
        total_files = len(file_list)
        part1_count = int(total_files * train_ratio)
        part2_count = int(total_files * val_ratio)
        part3_count = total_files - part1_count - part2_count

        os.makedirs(self.part1_dir, exist_ok=True)
        os.makedirs(self.part2_dir, exist_ok=True)
        os.makedirs(self.part3_dir, exist_ok=True)

        part1_files = []
        part2_files = []
        part3_files = []
        for i, file_name in enumerate(file_list):
            source_path = os.path.join(dir_src, file_name)
            if i < part1_count:
                part1_files.append((source_path, self.part1_dir))
            elif i < part1_count + part2_count:
                part2_files.append((source_path, self.part2_dir))
            else:
                part3_files.append((source_path, self.part3_dir))
        thread1 = threading.Thread(target=copy_files, args=(part1_files,))
        thread2 = threading.Thread(target=copy_files, args=(part2_files,))
        thread3 = threading.Thread(target=copy_files, args=(part3_files,))

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()


    def split_directory(self, num_parts, type_document):
        """
            This function split data to multiple part
            
            Parameters:
            num_parts (int): Ratio train.
            type: train, val, test
            
            Returns: Void -> Split to directory /package/source/part_data/{train/val/test/}
            
        """

        part1_dir_out = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'sub_source_data', 'train')
        part2_dir_out = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'sub_source_data', 'val')
        part3_dir_out = os.path.join(UtilsRoot.get_root_path(), 'package', 'source', 'sub_source_data', 'test')

        if type_document == 'train':
            input_directory = self.part1_dir
            output_parent_dir = part1_dir_out
        elif type_document == 'val':
            input_directory = self.part2_dir
            output_parent_dir = part2_dir_out
        else:
            type_document = "test"
            input_directory = self.part3_dir
            output_parent_dir = part3_dir_out


        # Create output directories
        os.makedirs(output_parent_dir, exist_ok=True)
        output_dirs = [os.path.join(output_parent_dir, f'{type_document}_{i+1}') for i in range(num_parts)]

        for output_dir in output_dirs:
            os.makedirs(output_dir, exist_ok=True)

        # Get the list of files in the input directory
        files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]

        # Determine the number of files in each part
        files_per_part = len(files) // num_parts

        # Copy files to the respective output directories
        for i, output_dir in enumerate(output_dirs):
            start_index = i * files_per_part
            end_index = start_index + files_per_part
            if i == num_parts - 1:
                end_index = len(files)
            files_to_copy = files[start_index:end_index]
            for file_to_copy in files_to_copy:
                src = os.path.join(input_directory, file_to_copy)
                dst = os.path.join(output_dir, file_to_copy)
                shutil.copy(src, dst)

    def radom_get_num_file(self, src, des ,number):
        random_get_files.get_number_radom_file(src, des ,number)

    def create_source_target(self, type_document, isAll=True, isSplit=False, idx_is_split=1):
        """
        This function creates source and target files for different data types.
        
        Parameters:
        type_document (str): The type of document (e.g., 'train', 'test', 'val').
        isAll (bool): Flag to indicate if all data types should be processed.
        isSplit (bool): Flag to indicate if splitting is required.
        idx_is_split (int): Index for splitting.
        """

        print("Call create_source_target fnc")

        def transform_data(type_document_local):
            src_path = ""
            if type_document_local == 'train':
                src_path = self.part1_dir
            elif type_document_local == 'val':
                src_path = self.part2_dir
            elif type_document_local == 'test':
                src_path = self.part3_dir   
            
            print("Create source, target for dir: ", src_path, self.path_source_target)

            transform_datafiles.run(type_document_local, src_path, self.path_source_target)

        if isAll:
            data_types = ['train', 'test', 'val']
        else:
            data_types = [type_document]

        threads = []
        for data_type in data_types:
            thread = threading.Thread(target=transform_data, args=(data_type,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()