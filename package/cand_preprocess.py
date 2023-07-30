def process_line(line):
    # Xử lý dữ liệu tại đây, ví dụ: thêm dấu chấm cuối dòng
    line = line.replace("vov . vn - ", "").replace("( vov ) ", "").replace("vov vn ", "").replace("browser not support iframe", "").strip()
    return line

input_file =  r'C:\Users\maxco\Desktop\BRIO_RENEW\package\cnndm\out_merge\val.out'
output_file = r'C:\Users\maxco\Desktop\BRIO_RENEW\package\cnndm\preprocess_final\val.out'

try:
    # Đọc từng dòng từ tệp gốc
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    # Xử lý từng dòng và lưu vào tệp mới
    with open(output_file, "w", encoding="utf-8") as outfile:
        for line in lines:
            processed_line = process_line(line)
            outfile.write(processed_line + "\n")

    print("Xử lý và lưu thành công!")
except FileNotFoundError:
    print(f"Tệp '{input_file}' không tồn tại.")
except Exception as e:
    print(f"Có lỗi xảy ra: {e}")