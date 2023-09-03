import sys
import subprocess

if len(sys.argv) != 3:
    print("Sử dụng: python your_program.py arg1 arg2")
else:
    arg1_value = sys.argv[1]
    arg2_value = sys.argv[2]
    result = arg1_value + arg2_value  + "Thành công rồi"
    # Ghi kết quả vào tệp văn bản
    with open("output.txt", "w", encoding="utf-8") as output_file:
        output_file.write(result)

    #print(f"Kết quả đã được ghi vào tệp output.txt")
