import re

text = "21. [Thành phố Bao Đầu, Nội Mông] Hồ sơ vụ án của ba học viên được trình lên viện kiểm sát"

# Loại bỏ các ký số dạng "1." hoặc "2." hoặc "3." khỏi văn bản
text_without_numbers = re.sub(r'\d+\.\s*', '', text)

# Tách đoạn văn bản đã loại bỏ ký số thành các phần tử
pattern = r'\[|,|;|\]|và'
elements = re.split(pattern, text_without_numbers)

# Loại bỏ khoảng trắng thừa ở đầu và cuối mỗi phần tử (nếu có)
elements = [element.strip() for element in elements if element.strip()]

# Danh sách các từ đặc biệt cần giữ lại
special_words = ["ông", "bà", "anh", "cô", "chị", "thành", "phố", "huyện", "quận", "khu", "tỉnh", "thị trấn", "thị xã"]

# Duyệt qua từng phần tử và xử lý
result = []
for element in elements:
    # Tách thành các từ
    words = element.split()
    # Lưu trữ các từ thỏa mãn điều kiện
    valid_words = []
    for word in words:
        # Kiểm tra xem từ có chữ cái đầu tiên viết hoa hoặc thuộc danh sách từ đặc biệt không
        if word[0].isupper() or word.lower() in special_words:
            valid_words.append(word)
    # Tạo lại đoạn văn bản từ các từ thỏa mãn điều kiện
    valid_element = ' '.join(valid_words)
    if valid_element:
        result.append(valid_element)
result = [item for item in result if len(item.split()) > 1]
# In ra các phần tử đã xử lý
print(result)

