import csv

# Tên tệp CSV đầu vào
input_file = 'dic_name_data.csv'

# Tạo hai tên tệp CSV đầu ra cho các hàng bị trùng nhau và các giá trị duy nhất
duplicate_file = 'duplicate_rows.csv'
unique_file = 'unique_rows.csv'

# Mở tệp đầu vào và đọc nội dung
with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)

    # Tạo danh sách để lưu trữ các hàng bị trùng nhau và các giá trị duy nhất
    duplicate_rows = []
    unique_rows = []
    unique_values = set()

    # Duyệt qua từng hàng trong tệp CSV đầu vào
    for row in reader:
        # Lấy giá trị trong cột thứ nhất của hàng
        value = row[0]
        # Kiểm tra xem giá trị này đã xuất hiện trước đó hay chưa
        if value in unique_values:
            # Nếu đã xuất hiện, thêm hàng này vào danh sách các hàng bị trùng nhau
            duplicate_rows.append(row)
        else:
            # Nếu chưa xuất hiện, thêm giá trị vào danh sách các giá trị duy nhất
            unique_values.add(value)
            # Thêm cả hàng vào danh sách các hàng duy nhất
            unique_rows.append(row)

# Ghi dữ liệu các hàng bị trùng nhau vào tệp CSV
with open(duplicate_file, 'w', newline='', encoding='utf-8') as duplicate_csvfile:
    writer = csv.writer(duplicate_csvfile)
    writer.writerows(duplicate_rows)

# Ghi dữ liệu các hàng duy nhất vào tệp CSV
with open(unique_file, 'w', newline='', encoding='utf-8') as unique_csvfile:
    writer = csv.writer(unique_csvfile)
    writer.writerows(unique_rows)

print(f"Đã ghi dữ liệu vào {duplicate_file} và {unique_file}.")
