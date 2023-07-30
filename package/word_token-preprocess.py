import os
import argparse
import concurrent.futures
from path import UtilsRoot
from os.path import abspath
from underthesea import word_tokenize

if __name__ == '__main__':

    """
    This function creates tokenize for different data types.
    """

    print("Call create token fnc")

    def transform_data(type_document_local, type_token = "source"):
        count = 1
        file_in = ""
        file_out = ""

        path_tokenize_target = os.path.join(UtilsRoot.get_root_path(), 'package', 'cnndm', 'preprocess_final')
        path_source_target = os.path.join(UtilsRoot.get_root_path(), 'package', 'cnndm', 'preprocess_final')

        print(path_tokenize_target, path_source_target)
        if  type_token == "source":
            if type_document_local == 'train':
                file_in = os.path.join(path_source_target, "train.source")
                file_out = os.path.join(path_tokenize_target, "train.source.tokenized")
            elif type_document_local == 'val':
                file_in = os.path.join(path_source_target, "val.source")
                file_out = os.path.join(path_tokenize_target, "val.source.tokenized")
            elif type_document_local == 'test':
                file_in = os.path.join(path_source_target, "test.source")
                file_out = os.path.join(path_tokenize_target, "test.source.tokenized")
        elif type_token == "target":
            if type_document_local == 'train':
                file_in = os.path.join(path_source_target, "train.target")
                file_out = os.path.join(path_tokenize_target, "train.target.tokenized")
            elif type_document_local == 'val':
                file_in = os.path.join(path_source_target, "val.target")
                file_out = os.path.join(path_tokenize_target, "val.target.tokenized")
            elif type_document_local == 'test':
                file_in = os.path.join(path_source_target, "test.target")
                file_out = os.path.join(path_tokenize_target, "test.target.tokenized")
        elif type_token == "out":
            if type_document_local == 'train':
                file_in = os.path.join(path_source_target, "train.out")
                file_out = os.path.join(path_tokenize_target, "train.out.tokenized")
            elif type_document_local == 'val':
                file_in = os.path.join(path_source_target, "val.out")
                file_out = os.path.join(path_tokenize_target, "val.out.tokenized")

        f = open(file_out, "a",encoding="utf-8")
        
        for text in open(file_in, encoding="utf-8"):
            if count % 100 == 0:
                print(count)

            count +=1; text = text.strip()

            dumb_characters = ['\u200b','. - .',' . - - - .','-','vov . vn',' . vn',' .']

            for character in dumb_characters:
                text = text.replace(character, '')

            try: 
                output = word_tokenize(text, format="text") + "\n"; 
                if output is not None:
                    f.write(output)
            except:
                print("error")
                f.write(text + "\n")


    data_types = ['train', 'val', 'test']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for data_type in data_types:
            futures.append(executor.submit(transform_data, data_type, "out"))

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

# python word_token-preprocess.py --fin ./cnndm/source_target/train.source --fout ./cnndm/tokenized/train.source.tokenized
