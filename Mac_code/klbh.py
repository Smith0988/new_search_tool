import re

# Câu mẫu
target_english_sentence = "This is an Example sentence with some lowercased words and sentenced 10 10.5 year."

# Sử dụng biểu thức chính quy để tìm các từ viết thường
lowercase_words = re.findall(r'\b[a-z]+\b', target_english_sentence.lower())

# In danh sách các từ viết thường
print(lowercase_words)
