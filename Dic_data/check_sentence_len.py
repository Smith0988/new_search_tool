import pandas as pd

# Đọc tệp CSV vào một DataFrame
df = pd.read_csv('dic_eng_vn_data_new.csv', header=None)

# Định nghĩa hàm để tính số lượng từ trong câu tiếng Anh và ghi vào cột số 3
def count_words(sentence):
    words = sentence.split()
    return len(words)

df[2] = df[0].apply(count_words)  # Thêm cột mới với số lượng từ

# Sắp xếp thứ tự tăng dần theo số lượng từ ở cột số 3
df = df.sort_values(by=2, ascending=True)

# Lưu kết quả vào tệp CSV mới
df.to_csv('dic_eng_vn_data_new_sorted.csv', index=False, header=None)


