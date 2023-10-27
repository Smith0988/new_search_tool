import pandas as pd
import numpy as np

# Đọc tệp CSV vào một DataFrame
df = pd.read_csv('dic_eng_vn_data_new.csv', header=None)

# Định nghĩa hàm để tính số lượng từ trong câu tiếng Anh và ghi vào cột số 3
def count_words(sentence):
    if isinstance(sentence, str):
        words = sentence.split()
        return len(words)
    return 0

# Sử dụng hàm numpy.vectorize để áp dụng count_words cho mỗi giá trị trong cột 0
df[2] = np.vectorize(count_words)(df[0])

# Sắp xếp thứ tự tăng dần theo số lượng từ ở cột số 3
df = df.sort_values(by=2, ascending=True)

# Lưu kết quả vào tệp CSV mới
df.to_csv('dic_eng_vn_data_new_sorted.csv', index=False, header=None)
