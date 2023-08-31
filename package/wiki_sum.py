import os
import re
import csv
import glob
import string

source_dir = 'G:/NLP/ViWikiSum/source'
summary_dir = 'G:/NLP/ViWikiSum/summary'

source_subdirectories = os.listdir(source_dir)
summary_subdirectories = os.listdir(summary_dir)

def clean_document(content):
    contents_parsed = content
    contents_parsed = contents_parsed.replace('\n', '. ').replace("browser not support iframe ", "").replace("\xa0", "")
    contents_parsed = contents_parsed.strip()

    # Thay thế nhiều spaces bằng 1 space
    contents_parsed = re.sub(r"\s+", r" ", contents_parsed).strip()
    # Chuẩn hóa email về một thực thể duy nhất

    email_pattern = r'\S+@\S+\.\S+'
    contents_parsed = re.sub(email_pattern, '__EMAIL__', contents_parsed)
    return contents_parsed

for subdir in source_subdirectories:
        if subdir in summary_subdirectories:
            source_subdir_path = os.path.join(source_dir, subdir)
            summary_subdir_path = os.path.join(summary_dir, subdir)
            source_files = [f for f in os.listdir(source_subdir_path) if f.endswith('.txt')]
            summary_files = [f for f in os.listdir(summary_subdir_path) if f.endswith('.txt')]
            if source_files and summary_files:
                source_file_path = os.path.join(source_subdir_path, source_files[0])
                summary_file_path = os.path.join(summary_subdir_path, summary_files[0])
                output_file_path = "G:/NLP/brio_v1/wiki_source/wiki_sum_" + subdir + '.story'
                with open(source_file_path, 'r', encoding='utf-8') as source_file, open(summary_file_path, 'r', encoding='utf-8') as summary_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
                    content_source = ""
                    content_summary = ""

                    text_source = source_file.read()
                    content_src_start = text_source.find("content:")
                    text_summary = summary_file.read()
                    content_sm_start = text_summary.find("content:")
                    
                    # Lấy nội dung sau phần "content:"
                    if content_src_start != -1:
                        content_source = text_source[content_src_start + len("content:"):]

                    if content_sm_start != -1:
                        content_summary = text_summary[content_sm_start + len("content:"):]
                    
                    if content_source != "" and content_summary != "":
                        output_file.write(clean_document(content_source.strip()) + '\n@highlight\n' +  clean_document(content_summary.strip()) + '\n')

