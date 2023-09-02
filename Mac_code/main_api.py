import sys
import subprocess

if len(sys.argv) != 3:
    print("Sử dụng: python your_program.py arg1 arg2")
else:
    arg1_value = sys.argv[1]
    arg2_value = sys.argv[2]
    result = f"Kết quả: {arg1_value} và {arg2_value}"
    utf8_result = result.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    print(utf8_result)
