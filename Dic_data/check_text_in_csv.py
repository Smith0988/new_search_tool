import pandas as pd

# Đọc tệp CSV vào một DataFrame
df = pd.read_csv('link_eng_vn_gct.csv', header=None)

# Lọc các hàng mà phần tử ở cột thứ nhất (index 0) chứa từ "By"
#filtered_df = df[df.iloc[:, 0].str.contains('By', case=False, na=False)]

# Lọc các hàng mà phần tử ở cột thứ hai (index 1) chứa chuỗi 'tin-tuc' hoặc 'bo-sung'
filtered_df = df[df.iloc[:, 1].str.contains('tin-tuc|bo-sung', case=False, na=False)]


# Ghi DataFrame đã lọc vào một tệp CSV mới
filtered_df.to_csv('filtered_line_en_vn.csv', index=False, header=False)
