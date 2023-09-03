import subprocess

# Đường dẫn đến tệp .exe và đối số
app_path = r'C:\Users\Cong Dinh\Documents\GitHub\New_Search_Tool\new_search_tool\Mac_code\dist\main_api.exe'
arguments = "hello world"  # Đối số được nối với dấu cách

# Tạo danh sách lệnh bao gồm đường dẫn đến tệp .exe và các đối số
command = [app_path] + arguments.split()  # Tách đối số thành danh sách các từ và nối vào danh sách lệnh

# Thực thi lệnh và chấp nhận đầu ra
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Đọc đầu ra và lỗi từ quá trình
stdout, stderr = process.communicate()

# Kiểm tra mã trả về của quá trình
if process.returncode == 0:
    # In đầu ra từ chương trình .exe
    print("Kết quả:")
    print(stdout.decode('utf-8'))
else:
    # In lỗi từ stderr nếu có lỗi
    print(f"Lỗi: {stderr.decode('utf-8')}")
