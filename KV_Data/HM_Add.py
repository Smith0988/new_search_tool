# Đọc nội dung từ file Vietnam.txt và loại bỏ các dòng trống
with open('Vietnam.txt', 'r', encoding='utf-8') as vietnam_file:
    vietnam_data = [line.strip() for line in vietnam_file if line.strip()]

# Ghi nội dung đã xử lý vào file HN_data.txt (chế độ ghi bổ sung - append)
with open('HN_data.txt', 'a', encoding='utf-8') as hn_file:
    if vietnam_data:  # Kiểm tra xem có dữ liệu từ Vietnam.txt không
        if hn_file.tell() != 0:  # Kiểm tra xem file HN_data.txt đã chứa dữ liệu trước đó không
            hn_file.write('\n')  # Xuống dòng trước khi nối với dữ liệu trước đó
        hn_file.write('\n'.join(vietnam_data))

print("Đã sao chép dữ liệu từ Vietnam.txt sang HN_data.txt và loại bỏ các dòng trống.")
