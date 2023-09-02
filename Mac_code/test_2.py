import subprocess
import base64

# Lệnh để thực thi tệp .exe và truyền đối số "hello" và "world"
command = 'Searching_Tool_api.exe "hello" "world"'

# Thực thi lệnh và chấp nhận đầu ra
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Đọc đầu ra và lỗi từ quá trình
stdout, stderr = process.communicate()

# Kiểm tra mã trả về của quá trình
if process.returncode == 0:
    # Chuyển đổi stdout thành Base64
    utf8_result = stdout.encode('utf-8', errors='ignore')
    base64_result = base64.b64encode(utf8_result).decode('utf-8', errors='ignore')

    # In kết quả ở dạng Base64
    print("Kết quả (Base64):")
    print(base64_result)
else:
    # In lỗi từ stderr nếu có lỗi
    print(f"Lỗi: {stderr.strip()}")
