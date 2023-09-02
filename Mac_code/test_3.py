import platform

# Lấy tên hệ điều hành
os_name = platform.system()

# Kiểm tra xem chương trình đang chạy trong Git Bash hay không
if os_name.lower() == "windows":
    print("Chương trình đang chạy trong terminal mặc định của Windows.")
else:
    print("Chương trình đang chạy trong Git Bash hoặc một terminal khác trên hệ điều hành khác.")
