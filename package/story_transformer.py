import os
import re
import csv
import glob
import string
from pyvi import ViTokenizer, ViPosTagger
# https://realpython.com/python-encodings-guide/
# List các ký tự hợp lệ trong tiếng Việt
whitespace = ' '
digits = '0123456789'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
intab_l = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ"
accept_strings =  intab_l + ascii_lowercase + digits + punctuation + whitespace

r = re.compile('^[' + accept_strings + ']+$')


# Một câu sẽ được coi là hợp lệ nếu có các ký tự nằm trong accept_strings
def _check_tieng_viet(seq):
  if re.match(r, seq.lower()):
    return True
  else:
    return False

def extract_content4(directory, out_dir):
    file_paths = glob.glob(os.path.join(directory, '*'))
    for file_path in file_paths:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # print("FileName: ", file_name)
        output_file = os.path.join(out_dir, file_name + '.story')
        # print("OutputFile: ", output_file)
        with open(file_path, 'r', encoding="utf-8") as infile, open(output_file, 'w', encoding="utf-8") as outfile:
            lines = infile.read()
            contents = lines.strip().split('<<space>>')
            if len(contents) >= 4:
                outfile.write(clean_document(contents[3]) + '\n@highlight\n' +  clean_document(contents[2]) + '\n')


def extract_csv(directory, out_file_csv):
    file_paths = glob.glob(os.path.join(directory, '*'))
    with open(out_file_csv, mode='w', newline='', encoding='utf-8') as file:
      writer = csv.writer(file)
      writer.writerow(["source", "target"])

      for file_path in file_paths:
          file_name = os.path.splitext(os.path.basename(file_path))[0]
          #print("FileName: ", file_name)
          with open(file_path, 'r', encoding="utf-8") as infile:
              lines = infile.read()
              contents = lines.strip().split('<<space>>')
              if len(contents) >= 4:
                  writer.writerow((clean_document(contents[3]), clean_document(contents[2])))


def clean_document(content):
    contents_parsed = content.lower()
    contents_parsed = contents_parsed.replace('\n', '. ').replace("browser not support iframe ", "").replace("\xa0", "")
    contents_parsed = contents_parsed.strip()
    doc = ViTokenizer.tokenize(contents_parsed) #Pyvi Vitokenizer library
    doc = doc.lower() #Lower
    tokens = doc.split() #Split in_to words
    table = str.maketrans('', '', string.punctuation.replace("_", "")) #Remove all punctuation
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]
    return " ".join(tokens)

def count_rows_in_csv(file_path):
  import pandas as pd
  try:
    df = pd.read_csv(file_path, header=None)
    # Đếm số dòng dữ liệu trong DataFrame
    row_count = len(df)
    return row_count
  except FileNotFoundError:
    return 0

extract_content4(r'C:\Users\maxco\Desktop\BRIO_DATA\ex_1', r'C:\Users\maxco\Desktop\BRIO_RENEW\package\source\data_root')
#extract_csv(r'C:\Users\maxco\Desktop\BRIO_DATA\ex_1\ex', r'C:\Users\maxco\Desktop\BRIO_RENEW\package\source\csv_root\data_1.csv')

row_count = count_rows_in_csv(r'C:\Users\maxco\Desktop\BRIO_RENEW\package\source\csv_root\data_1.csv')
print("Số dòng dữ liệu trong tệp CSV là:", row_count)