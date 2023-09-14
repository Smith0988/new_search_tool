def tokenize_sentence(sentence):
    # Tách câu thành các từ
    words = sentence.split()
    return words

# Sử dụng hàm để tách câu
english_sentence = "Ms. Wang’s three-year-old granddaughter cried all night and developed a fever that lingered for several days"
tokens = tokenize_sentence(english_sentence)

# In các từ trong câu
for word in tokens:
    print(word)
