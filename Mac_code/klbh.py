import pandas as pd

# Đọc dữ liệu từ tệp CSV vào DataFrame
df = pd.read_csv('dic_eng_vn_data.csv')

# Tính độ dài (số từ) của mỗi phần tử trong cột 1 và thêm một cột mới vào DataFrame
df['Word_Count'] = df.iloc[:, 0].str.split().apply(len)

# Sắp xếp DataFrame theo cột 'Word_Count' (số từ) từ ít đến nhiều
df_sorted = df.sort_values(by='Word_Count')

# Ghi DataFrame đã sắp xếp ra tệp CSV mới
df_sorted.to_csv('dic_eng_vn_data_sorted.csv', index=False)
