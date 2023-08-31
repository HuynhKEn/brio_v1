from transformers import pipeline # for using model in huggingface

corrector = pipeline("text2text-generation", model="bmd1905/vietnamese-correction")

source_file_path = 'G:/NLP/brio_v1/package/cnndm/source_target/train.target'  # Đặt đường dẫn tới tệp nguồn của bạn

with open(source_file_path, 'r') as source_file:
    # Đọc từng dòng trong tệp nguồn
    lines = source_file.readlines()

# Mở tệp đích để ghi
target_file_path = 'G:/NLP/brio_v1/package/cnndm/source_target/spell/train.target'  # Đặt đường dẫn tới tệp đích bạn muốn tạo
pipeline("text2text-generation", model="bmd1905/vietnamese-correction")
with open(target_file_path, 'w') as target_file:
    # Ghi từng dòng vào tệp đích
    for line in lines:
        correctorx = corrector(line, max_length=len(line) + 2, , num_return_sequences=1)
        target_file.write(correctorx)

print("File processing completed.")