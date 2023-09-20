import re
import sys
import nltk
import os
import pandas as pd
from docx import Document
import requests
from bs4 import BeautifulSoup
from google_translate import translate_with_google_translate

import pandas as pd
import difflib
import datefinder
from pypinyin import lazy_pinyin

copyright_text = "Bản quyền © 2023 Minghui.org. Mọi quyền được bảo lưu."
from concurrent.futures import ThreadPoolExecutor

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


csv_filename = resource_path("data\link_eng_vn_gct.csv")
csv_filename_dic = resource_path("data\dic_eng_vn_data.csv")
kv_data = resource_path("data\KV_data.csv")


def find_vietnamese_link_1(english_link):
    # Đọc dữ liệu từ file CSV
    vietnamese_link = ""
    df = pd.read_csv(csv_filename)
    match = ""
    if re.match(r'https?://', english_link):
        match = re.search(r'(en\..*?\.html)', english_link)
    if match:
        english_link_1 = match.group(1)
    else:
        english_link_1 = english_link
    # Tìm link tiếng Anh trong cột 1 sử dụng biểu thức chính quy

    list1 = df.iloc[:, 0].tolist()
        # Lấy cột 1 và gán vào list2
    list2 = df.iloc[:, 1].tolist()
    for i in range(len(list1)):
        if english_link_1 in list1[i]:
            vietnamese_link = list2[i]
            break
    if vietnamese_link:
        if not vietnamese_link.startswith("http://") and not vietnamese_link.startswith("https://"):
            vietnamese_link = "https:" + vietnamese_link  # Thêm schema "https:" nếu cần
        return vietnamese_link
    else:
        return "Can not find Vietnamese Link"
def get_related_link(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_contents_1 = soup.find('div', class_='article-body-content')
        article_contents_2 = soup.find('div', class_='articleZhengwen geo cBBlack')
        if article_contents_1:
            article_contents = article_contents_1
        else:
            article_contents = article_contents_2
        if article_contents:
            paragraphs = article_contents.find_all(['p', 'h3'])
            valid_paragraphs = []
            start_collecting = False
            related_links = []
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)

                if "Related article" in text or "Related Article" in text or "Related Report" in text or "Related report" in text:
                    start_collecting = True

                if start_collecting:
                    if 'splitted' in paragraph.get("class", []):
                        span_sections = paragraph.find_all('span', class_='section')
                        for span in span_sections:
                            text_1 = span.get_text(strip=True)
                            valid_paragraphs.append(text_1)
                            for link in paragraph.find_all('a', href=True):
                                related_links.append(link['href'])
                    else:
                        valid_paragraphs.append(text)
                        for link in paragraph.find_all('a', href=True):
                            related_links.append(link['href'])

            if valid_paragraphs:
                article_content = "\n".join(valid_paragraphs)
                return valid_paragraphs, related_links
            else:
                return [], related_links
        else:
            return [], []
    else:
        return [], []


def find_vietnamese_link(english_link):
    first_text = "Bài liên quan:"
    all_link = []
    result_link = []
    result_link.append(first_text)
    # Đọc dữ liệu từ file CSV
    related_content, related_link = get_related_link(english_link)
    if related_content:
        for link in related_link:
            all_link.append(link)
        for link in all_link:
            result_link.append(find_vietnamese_link_1(link))
        return related_content, result_link, all_link
    else:
        return []

def find_vietnamese_sentence_1(english_sentence):
    result_list = []  # Danh sách chứa cột 1 (tiếng Anh)
    try:
        # Đọc dữ liệu từ file CSV vào một DataFrame
        df = pd.read_csv(csv_filename_dic)
        # Lấy cột 0 và gán vào list1
        list1 = df.iloc[:, 0].tolist()

        # Lấy cột 1 và gán vào list2
        list2 = df.iloc[:, 1].tolist()
        for i in range(len(list1)):
            if english_sentence in list1[i]:
                result_list.append((list2[i]))
                break
        if result_list:
            return result_list
        else:
            return []
    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")
        return e


def find_vietnamese_sentence(english_sentence):
    result_list = ""  # Danh sách chứa cột 1 (tiếng Anh)
    try:
        # Đọc dữ liệu từ file CSV vào một DataFrame
        df = pd.read_csv(csv_filename_dic)

        # Lấy giá trị của cột số 3 và chuyển thành kiểu int
        column3_values = df.iloc[:, 2].astype(int)

        # Độ dài của english_sentence
        english_length = len(english_sentence.split())
        if english_length > 61:
            return []

        filtered_df = df[column3_values == english_length]
        # Lấy danh sách các phần tử trong cột 1 và cột 2 tương ứng
        list1 = filtered_df.iloc[:, 0].tolist()
        list2 = filtered_df.iloc[:, 1].tolist()
        temp_ratio = 0.95
        for i in range(len(list1)):
            # Tính toán tỷ lệ tương đồng
            similarity_ratio = difflib.SequenceMatcher(None, english_sentence, list1[i]).ratio()
            if similarity_ratio > temp_ratio:  # Điều kiện để thêm kết quả vào danh sách
                temp_ratio = similarity_ratio
                result_list = list2[i]
        if result_list:
            return result_list
        else:
            return []
    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")
        return e

def find_vietnamese_sentence_4(english_sentence):
    result_list = ""  # Danh sách chứa cột 1 (tiếng Anh)
    try:

        words = english_sentence.split()
        #print(words)
        english_length = len(words)
        capitalized_words = [word for word in words if word.istitle()]
        your_uppercase_count = len(capitalized_words)
        #print(capitalized_words)
        if your_uppercase_count > english_length / 2:
            your_uppercase_count =1
        else:
            your_uppercase_count =0

        lowercase_words = re.findall(r'\b[a-z]+\b', english_sentence)
        #print(lowercase_words)
        # Đọc dữ liệu từ file CSV vào một DataFrame
        df = pd.read_csv("dic_eng_vn_data_updated.csv")

        # Lấy giá trị của cột số 3 và chuyển thành kiểu int
        column3_values = df.iloc[:, 2].astype(int)

        # Số từ viết hoa của câu tiếng Anh
        uppercase_count = df.iloc[:, 3].astype(int)

        if english_length > 61:
            return []

        if english_length < 5 or english_length == 61:
            filtered_df = df[(column3_values == english_length) & (uppercase_count == your_uppercase_count)]
        else:
            # Lọc ra các hàng có độ dài trùng với độ dài của english_sentence hoặc +- 1
            filtered_df = df[((column3_values == english_length) |
                              (column3_values == english_length - 1) |
                              (column3_values == english_length - 2) |
                              (column3_values == english_length + 2) |
                              (column3_values == english_length + 1)) &
                              (uppercase_count == your_uppercase_count)]

        # Lấy danh sách các phần tử trong cột 1 và cột 2 tương ứng
        list1 = filtered_df.iloc[:, 0].tolist()
        list2 = filtered_df.iloc[:, 1].tolist()
        result_list = []
        temp_ratio = 0.8

        if english_length <= 9 or your_uppercase_count:
            for i in range(len(list1)):
                similarity_ratio = difflib.SequenceMatcher(None, english_sentence, list1[i]).ratio()
                if similarity_ratio > temp_ratio:  # Điều kiện để thêm kết quả vào danh sách
                    temp_ratio = similarity_ratio
                    result_list = list2[i]
        else:
            j=0
            for i in range(len(list1)):
                for word in lowercase_words:
                    if word in list1[i]:
                        j = j+1
                if j == len(lowercase_words):
                    result_list = list2[i]
                    return result_list


        if result_list:
            return result_list
        else:
            return []

    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")
        return e


# Điều kiện mẫu để tìm kiếm
target_english_sentence = "Ms. Jin BL, a Changchun City resident, is being held in Cell 311 of the 8th Ward."
input_file_path = "dic_eng_vn_data_updated.csv"  # Thay đổi đường dẫn đến file CSV đầu vào

print(find_vietnamese_sentence(target_english_sentence))

