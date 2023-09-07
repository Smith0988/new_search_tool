import pandas as pd

# Đọc dữ liệu từ tệp CSV
df = pd.read_csv('link_eng_vn_gct.csv', header=None)

# Tạo một mảng boolean để kiểm tra xem text trong cột 1 (cột có chỉ số 0) có chứa "Can not" hay không
contains_can_not = df.iloc[:, 0].str.contains("Can not")

# Tạo hai tệp CSV mới dựa trên điều kiện
text_with_can_not_df = df[contains_can_not]
text_without_can_not_df = df[~contains_can_not]

# Lưu hai tệp CSV mới
text_with_can_not_df.to_csv('link_eng_vn_gct_3.csv', index=False, header=False)
text_without_can_not_df.to_csv('link_eng_vn_gct_4.csv', index=False, header=False)
