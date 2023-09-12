import re

text = "2. [Longkou City, Shandong Province] The Cases Against Four Practitioners Submitted to the Court"

# Loại bỏ các ký số dạng "1." hoặc "2." hoặc "3." khỏi văn bản
text_without_numbers = re.sub(r'\d+\.\s*', '', text)

# Tách đoạn văn bản đã loại bỏ ký số thành các phần tử
pattern = r'\[|,|;|\]|and '
elements = re.split(pattern, text_without_numbers)

# Loại bỏ khoảng trắng thừa ở đầu và cuối mỗi phần tử (nếu có)
elements = [element.strip() for element in elements if element.strip()]


# In ra các phần tử đã xử lý
print(elements)

