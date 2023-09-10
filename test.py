import spacy
import re

def extract_proper_nouns(text):
    # Tải mô hình ngôn ngữ tiếng Anh
    nlp = spacy.load("en_core_web_sm")

    # Sử dụng spaCy để phân tích văn bản
    doc = nlp(text)

    # Tách các tên riêng theo địa danh và tên người
    proper_nouns = []
    current_proper_noun = ""
    for token in doc:
        if token.ent_type_ in ["GPE", "PERSON"]:
            current_proper_noun += token.text + " "
        elif token.text in ["Mr.", "Ms."]:
            current_proper_noun += token.text
        else:
            if current_proper_noun:
                # Loại bỏ các từ không cần thiết khỏi current_proper_noun
                current_proper_noun = re.sub(r'\b(?:Face|Trial|Sent|Sentenced|Arrested|Detained|Harassed|Submitted|Framed|Home|Ransacked)\b', '', current_proper_noun)
                proper_nouns.append(current_proper_noun.strip())
                current_proper_noun = ""

    # Kiểm tra xem còn tên riêng cuối cùng không được thêm vào danh sách
    if current_proper_noun:
        # Loại bỏ các từ không cần thiết khỏi current_proper_noun
        current_proper_noun = re.sub(r'\b(?:Face|Trial|Sent|Sentenced|Arrested|Detained|Harassed|Submitted|Framed|Home|Ransacked)\b', '', current_proper_noun)
        proper_nouns.append(current_proper_noun.strip())

    return proper_nouns

# Sử dụng hàm để tách các tên riêng từ văn bản
text_to_tokenize = "4. [Xianning City, Hubei Province] Ms. Yang Dongxiang and Mr. Zhou Hongda Face Indictment"
result = extract_proper_nouns(text_to_tokenize)

# In danh sách các tên riêng
print(result)
