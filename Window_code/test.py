import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # Kiểm tra xem chương trình có đang chạy trong môi trường phát triển hay không
        if getattr(sys, 'frozen', False):
            # Nếu đang chạy từ tệp thực thi đã xây dựng bởi PyInstaller
            base_path = sys._MEIPASS
        else:
            # Nếu đang chạy trong môi trường phát triển
            base_path = os.path.abspath(".")

        # Đường dẫn đến thư mục searching_tool trên Desktop
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        searching_tool_path = os.path.join(desktop_path, "Searching_Tool")

        # Tạo thư mục searching_tool nếu nó chưa tồn tại
        if not os.path.exists(searching_tool_path):
            os.makedirs(searching_tool_path)

        # Đường dẫn tới tài nguyên trong thư mục searching_tool
        resource_path = os.path.join(searching_tool_path, relative_path)

        return resource_path
    except Exception as e:
        print(f"Error in resource_path: {str(e)}")
        return None

# Sử dụng resource_path để lấy đường dẫn tới một tài nguyên trong thư mục searching_tool
file_path = resource_path("sample.docx")
print(f"Đường dẫn tới tệp Word: {file_path}")
