import pandas as pd

# Đọc dữ liệu từ tệp CSV vào DataFrame
df = pd.read_csv('dic_eng_vn_data.csv')

# Tính độ dài (số lượng từ) của mỗi phần tử trong cột 1 và thêm một cột mới vào DataFrame
df['Length'] = df.iloc[:, 0].str.split().str.len()

# Sắp xếp DataFrame theo cột 'Length' (số lượng từ) từ ít đến nhiều
df_sorted = df.sort_values(by=df.columns[2])  # Sử dụng chỉ số cột 2 (cột 'Length')

# Hoặc nếu bạn muốn lưu kết quả vào một tệp CSV mới
df_sorted.to_csv('sorted_data.csv', index=False)
