import pandas as pd

# Đọc dữ liệu từ file CSV vào DataFrame
df = pd.read_csv('dic_eng_vn_data.csv')

# Hàm để đếm số lượng từ có chữ cái đầu in hoa trong một câu
def count_capitalized_words(sentence):
    words = sentence.split()
    capitalized_words = [word for word in words if word.istitle()]
    return len(capitalized_words)

# Chuyển đổi cột thứ 2 (cột số 3 theo chỉ số) thành kiểu số nguyên
df.iloc[:, 2] = df.iloc[:, 2].astype(int)

# Áp dụng hàm count_capitalized_words vào cột thứ 0 (cột English) và tạo cột mới Capitalized_Words_Count
df['Capitalized_Words_Count'] = df.iloc[:, 0].apply(count_capitalized_words)

# Hàm để kiểm tra và ghi giá trị vào cột 4
def check_and_write(row):
    if row[3] > row[2] / 2:
        return 1
    return 0

# Áp dụng hàm check_and_write vào DataFrame và tạo cột mới Is_More_Capitalized
df['Is_More_Capitalized'] = df.apply(check_and_write, axis=1)

# Giữ lại cột thứ 0 (cột English), thứ 1 (cột Vietnamese), thứ 2 (cột Number_of_Words), và thứ 4 (cột Is_More_Capitalized)
result_df = df.iloc[:, [0, 1, 2, 4]]

# In ra 10 hàng đầu tiên của DataFrame
print(result_df.head(10))

# Lưu kết quả vào file CSV mới (nếu bạn muốn)
result_df.to_csv('dic_eng_vn_data_updated.csv', index=False)
