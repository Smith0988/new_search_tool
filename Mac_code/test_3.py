import pandas as pd

# Đọc tệp CSV gốc vào DataFrame
df = pd.read_csv('link_eng_vn_gct.csv')

# Tạo một hàm để trích xuất số từ URL
def extract_number(url):
    parts = url.split('/')
    for part in parts:
        if '-' in part:
            number_part = part.split('-')[0]
            if number_part.isdigit():
                return int(number_part)
    return 0  # Trả về 0 nếu không tìm thấy số trong URL

# Sử dụng chỉ số cột thay vì tên cột (ví dụ: cột 1 là df.iloc[:, 1])
df['Number'] = df.iloc[:, 1].apply(extract_number)

# Sắp xếp DataFrame theo số từ lớn đến bé
df_sorted = df.sort_values(by='Number', ascending=False)

# Xóa cột số (đã không cần thiết sau khi đã sắp xếp)
df_sorted.drop('Number', axis=1, inplace=True)

# Lưu DataFrame đã sắp xếp thành tệp CSV mới
df_sorted.to_csv('link_eng_vn_gct_sorted.csv', index=False)
