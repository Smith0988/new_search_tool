import pandas as pd

# Đọc dữ liệu từ tệp CSV vào DataFrame
df = pd.read_csv('dic_eng_vn_data_sorted.csv')

# Tính độ dài (số từ) của mỗi phần tử trong cột 2 và thêm một cột mới vào DataFrame
df['Word_Count_Column2'] = df.iloc[:, 1].str.split().apply(len)

# Sắp xếp DataFrame theo cột 'Word_Count_Column2' (số từ của cột 2) từ ít đến nhiều
df_sorted = df.sort_values(by='Word_Count_Column2')

# Ghi DataFrame đã sắp xếp ra tệp CSV mới
df_sorted.to_csv('dic_eng_vn_data_sorted_by_column2.csv', index=False)
