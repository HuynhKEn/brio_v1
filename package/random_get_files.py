import os
import random
import shutil

def get_random_files(source_dir,  destination_dir, num_files, train_ratio, val_ratio):
    # Lấy danh sách tất cả các tệp trong thư mục nguồn
    all_files = os.listdir(source_dir)

    # Lấy ngẫu nhiên num_files tệp từ danh sách tệp
    random_files = random.sample(all_files, num_files)

    total_files = len(random_files)
    part1_count = int(total_files * train_ratio)
    part2_count = int(total_files * val_ratio)
    part3_count = total_files - part1_count - part2_count

    os.makedirs(os.path.join(destination_dir, "train"), exist_ok=True)
    os.makedirs(os.path.join(destination_dir, "val"), exist_ok=True)
    os.makedirs(os.path.join(destination_dir, "test"), exist_ok=True)

    for i, file_name in enumerate(random_files):
        source_path = os.path.join(source_dir, file_name)
        print("copy file name:", source_path)
        if i < part1_count:
            destination_dir_copy = os.path.join(destination_dir, "train")
        elif i < part1_count + part2_count:
            destination_dir_copy = os.path.join(destination_dir, "val")
        else:
            destination_dir_copy = os.path.join(destination_dir, "test")

        shutil.copy(source_path, destination_dir_copy)

def get_number_radom_file(source_directory, destination_directory, number_file):
    # Ensure the destination directory exists, if not, create it
    os.makedirs(destination_directory, exist_ok=True)

    # Get a list of all files in the source directory
    all_files = os.listdir(source_directory)

    # Shuffle the list of files to randomly select 70,000 files
    random.shuffle(all_files)
    selected_files = all_files[:number_file]

    # Copy the selected files to the destination directory
    for file_name in selected_files:
        source_file_path = os.path.join(source_directory, file_name)
        destination_file_path = os.path.join(destination_directory, file_name)
        shutil.copy2(source_file_path, destination_file_path)

    print("Successfully copied 70,000 files to the destination directory.")


def run(src_dir, des_path_dir, number_random, train_ratio, val_ratio):
    # Đường dẫn tới thư mục nguồn
    source_directory = src_dir

    # Đường dẫn tới thư mục đích
    destination_directory = des_path_dir

    # Số lượng tệp cần lấy ngẫu nhiên
    num_files = number_random

    # Lấy ngẫu nhiên các tệp và sao chép chúng vào thư mục đích
    get_random_files(source_directory, destination_directory, num_files, train_ratio, val_ratio)

#get_number_radom_file("C:/Users/Admin/Desktop/brio_v1/package/source/original_root/train","C:/Users/Admin/Desktop/brio_v1/package/source/original_root/val", 3000)
