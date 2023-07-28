def gop_file(file1, file2, output_file):
    with open(file1, 'r', encoding="utf-8") as f1:
        content1 = f1.read()
    
    with open(file2, 'r', encoding="utf-8") as f2:
        content2 = f2.read()
    
    with open(output_file, 'w', encoding="utf-8") as output:
        output.write(content1 + content2)
    
    print("Đã gộp thành công nội dung của hai file vào file mới: ", output_file)

# Thực hiện gộp nội dung của file1.txt và file2.txt vào file output.txt
gop_file(r'C:\Users\maxco\Desktop\BRIO_RENEW\package\train_1.out', r'C:\Users\maxco\Desktop\BRIO_RENEW\package\train_2.out', r'C:\Users\maxco\Desktop\BRIO_RENEW\package\cnndm\source_target\train.out')
