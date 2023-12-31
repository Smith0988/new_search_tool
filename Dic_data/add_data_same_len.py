import csv
import nltk
import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy
import re
from update_link import *

nltk.download('punkt')  # Download data for sentence tokenizer
from nltk.tokenize import sent_tokenize


def read_number_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            number = int(file.read())
            return number
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except ValueError:
        print(f"Invalid content in '{file_path}'. It should contain a valid number.")
        return None


def write_number_to_file(file_path, number):
    try:
        with open(file_path, 'w') as file:
            file.write(str(number))
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_use_link_to_csv(text1, text2):
    # Tạo DataFrame với hai cột "English" và "Vietnamese"
    df = pd.DataFrame({'English': [text1], 'Vietnamese': [text2]})

    # Ghi vào file CSV, mode='a' để ghi tiếp dữ liệu nếu file đã tồn tại
    df.to_csv('all_link_use.csv', mode='a', header=False, index=False)


def write_not_use_link_to_csv(text1, text2):
    # Tạo DataFrame với hai cột "English" và "Vietnamese"
    df = pd.DataFrame({'English': [text1], 'Vietnamese': [text2]})

    # Ghi vào file CSV, mode='a' để ghi tiếp dữ liệu nếu file đã tồn tại
    df.to_csv('link_not_use_complete.csv', mode='a', header=False, index=False)


def write_to_text(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)


def write_list_to_txt(filename, lst):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in lst:
            file.write(item + '\n')


def get_en_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        article_contents = []
        soup = BeautifulSoup(response.content, 'html.parser')
        article_contents_1 = soup.find('div', class_='article-body-content')
        article_contents_2 = soup.find('div', class_='articleZhengwen geo cBBlack')
        article_contents_3 = soup.find('div', class_='articleZhengwen geo')
        if article_contents_1:
            article_contents = article_contents_1
        if article_contents_2:
            article_contents = article_contents_2
        if article_contents_3:
            article_contents = article_contents_3

        if article_contents:
            # Tìm các phần tử con của 'articleBody'
            paragraphs = article_contents.find_all(['p', 'h3'])

            valid_paragraphs = []
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)
                match = re.match(r'^\d+\.\s*(.*)', text)
                if match:
                    valid_paragraphs.append(match.group(1))
                else:
                    valid_paragraphs.append(text)

            # Ghi nội dung các đoạn văn bản hợp lệ vào biến article_content
            article_content = "\n".join(valid_paragraphs)
            return article_content
        else:
            return []
    else:
        return []


def get_en_article_title(url):
    try:
        # Tải nội dung của trang web
        response = requests.get(url)

        # Kiểm tra nếu yêu cầu thành công (status code 200)
        if response.status_code == 200:
            # Sử dụng BeautifulSoup để phân tích cú pháp trang web
            soup = BeautifulSoup(response.content, 'html.parser')

            # Tìm thẻ div có class là 'article-title'
            article_title_tag = soup.find('div', class_='article-title')
            
            if not article_title_tag:
                article_title_tag = soup.find('h2', class_='articleTitle cABlue')

            if not article_title_tag:
                article_title_tag = soup.find('h2', class_='printTitle geo')

            # Kiểm tra nếu tồn tại thẻ và lấy nội dung text của tiêu đề printTitle geo
            if article_title_tag:
                article_title = article_title_tag.text.strip()
                return article_title
            else:
                return "Can not found title Eng"
        else:
            return "Web not respond"
    except Exception as e:
        return ""

def get_vn_article_title(url):
    try:
        # kiem tra
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https:" + url  # Thêm schema "https:" nếu cần
        # Tải nội dung của trang web
        response = requests.get(url)

        # Kiểm tra nếu yêu cầu thành công (status code 200)
        if response.status_code == 200:
            # Sử dụng BeautifulSoup để phân tích cú pháp trang web
            soup = BeautifulSoup(response.content, 'html.parser')

            # Tìm thẻ div có class là 'article-title'
            article_title_tag = soup.find('h1', class_='articleTitle cABlue')

            # Kiểm tra nếu tồn tại thẻ và lấy nội dung text của tiêu đề
            if article_title_tag:
                article_title = article_title_tag.text.strip()
                return article_title
            else:
                return "Can not find Vietnamese Title"
        else:
            return "Can not find Vietnamese Title"
    except Exception as e:
        return "Can not find Vietnamese Link"


def get_vn_article_content(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https:" + url  # Thêm schema "https:" nếu cần
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='articleBody')
        if article_body:
            # Tìm các phần tử con của 'articleBody'
            paragraphs = article_body.find_all('p')

            # Loại bỏ nội dung của đoạn đầu tiên nếu không chứa ký tự "["
            if "[" not in paragraphs[0].get_text(strip=True):
                paragraphs = paragraphs[1:]
            valid_paragraphs = []
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)
                match = re.match(r'^\d+\.\s*(.*)', text)
                if match:
                    valid_paragraphs.append(match.group(1))
                else:
                    valid_paragraphs.append(text)

            # Ghi nội dung các đoạn văn bản hợp lệ vào biến article_content
            article_content = "\n".join(valid_paragraphs)
            return article_content
        else:
            return []
    else:
        return []


def get_links_from_csv(file_path):
    links_en = []
    links_vn = []

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Bỏ qua header nếu có

        for row in reader:
            link_en, link_vn = row[0], row[1]
            links_en.append(link_en)
            links_vn.append(link_vn)

    return links_en, links_vn


def text_normalization_vn_f(vn_article):
    if vn_article:
        lines_vn = vn_article.split('\n')
    else:
        lines_vn =[]
    new_vn_list = []

    for text_vn in lines_vn:

        if "Họ và tên" in text_vn or "Ngày mất:" in text_vn or "Giới tính:" in text_vn or "Tên Trung Quốc:" in text_vn:
            continue
        if 'Họ và tên' in text_vn or 'Ngày mất' in text_vn or 'Giới tính:' in text_vn or 'Tên Trung Quốc:' in text_vn:
            continue
        if  "Danh tính và thông tin"  in text_vn or "Những người tham gia bức hại"  in text_vn or  "Tham gia bức hại" in text_vn or "Những cá nhân chịu trách" in text_vn or "Bản quyền © 2023" in text_vn or "(Hết)" in text_vn or "(Còn tiếp.)" in text_vn or "Bản tiếng" in text_vn or "Bản tiếng Hán" in text_vn or "Bài liên quan" in text_vn or "Thông tin liên hệ" in text_vn or "Thông tin liên lạc" in text_vn or "Các báo cáo liên quan" in text_vn or "Báo cáo liên quan" in text_vn or "Mọi bài viết, hình ảnh, hay nội dung" in text_vn or "Bài viết chỉ thể hiện quan điểm" in text_vn or "Mọi nội dung đăng trên trang" in text_vn or "danh sách những thủ phạm" in text_vn:
            break

        if 'Danh tính và thông tin'  in text_vn or 'Những người tham gia bức hại'  in text_vn or 'Tham gia bức hại' in text_vn or  'Những cá nhân chịu trách' in text_vn or  'Bản quyền © 2023' in text_vn or'(Hết)' in text_vn or '(Còn tiếp.)' in text_vn or 'Bản tiếng' in text_vn or 'Bản tiếng Hán' in text_vn or 'Bài liên quan' in text_vn or 'Thông tin liên hệ' in text_vn or 'Thông tin liên lạc' in text_vn or 'Các báo cáo liên quan' in text_vn or 'Báo cáo liên quan' in text_vn or 'Mọi bài viết, hình ảnh, hay nội dung' in text_vn or 'Bài viết chỉ thể hiện quan điểm' in text_vn or 'Mọi nội dung đăng trên trang' in text_vn or 'danh sách những thủ phạm' in text_vn:
            break

        if "[MINH HUỆ" in text_vn:
            text_vn = re.sub(r'\[.*?\]', '', text_vn)
        if text_vn.strip():
            new_vn_list.append(text_vn)

    return new_vn_list


def text_normalization_en_f(en_article):
    if en_article:
        lines_en = en_article.split('\n')
    else:
        lines_en = []
    new_en_list = []
    for i in range(len(lines_en)):
        text_en = lines_en[i]
        if 'Parties involved' in text_en or  'Participants in the persecution'  in text_en or 'Participant in the persecution'  in text_en or  'Key Responsible Personnel' in text_en or  'Related article' in text_en or 'Related Article' in text_en or  'Perpetrators involve' in text_en or 'Related Report' in text_en or 'Related report' in text_en or 'Perpetrators’ contact information' in text_en or 'list of the perpetrators' in text_en:
            break

        if "Parties involved" in text_en or  "Participants in the persecution"  in text_en or  "Participant in the persecution"  in text_en or "Key Responsible Personnel" in text_en or  "Related article" in text_en or "Related Article" in text_en or   "Perpetrators involve" in text_en or  "Related Report" in text_en or "Perpetrators’ contact information" in text_en or "list of the perpetrators" in text_en:
            break

        if "Chinese Name" in text_en or "English Name" in text_en:
            continue
        if 'Chinese Name' in text_en or 'English Name' in text_en:
            continue

        if "(Minghui.org)" in text_en:
            text_en = re.sub(r'\(Minghui.org\)', '', text_en)

        if "(Clearwisdom.net)" in text_en:
            text_en = re.sub(r'\(Clearwisdom.net\)', '', text_en)


        if text_en.strip():
            new_en_list.append(text_en)

    return new_en_list


def tokenize_sentences_with_name_prefix(text):
    name_prefixes = ["Mr.", "Ms.", "No."]

    # Replace name prefixes with placeholders
    for prefix in name_prefixes:
        text = text.replace(prefix, f"{prefix}DOT")

    # Tokenize sentences
    sentences = nltk.sent_tokenize(text)

    # Replace the placeholders back to name prefixes
    for prefix in name_prefixes:
        sentences = [sentence.replace(f"{prefix}DOT", prefix) for sentence in sentences]

    return sentences


def paragraph_indentation(en_article, vn_article):
    new_en_list = []
    new_vn_list = []
    if len(en_article) > len(vn_article):
        index = len(en_article) - len(vn_article)
        for i in range(len(vn_article)):
            en_text = en_article[i]
            vn_text = vn_article[i]
            english_sentences = tokenize_sentences_with_name_prefix(en_text)
            vietnamese_sentences = tokenize_sentences_with_name_prefix(vn_text)
            if len(vietnamese_sentences) == len(english_sentences):
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
            else:
                break

        """
        for i in range(len(en_article) - 1, -1, -1):
            en_text = en_article[i]
            vn_text = vn_article[i-index]
            english_sentences = tokenize_sentences_with_name_prefix(en_text)
            vietnamese_sentences = tokenize_sentences_with_name_prefix(vn_text)
            if len(vietnamese_sentences) == len(english_sentences):
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
            else:
                break
                
        """

    else:
        index = len(vn_article) - len(en_article)
        for i in range(len(en_article)):
            en_text = en_article[i]
            vn_text = vn_article[i]
            english_sentences = tokenize_sentences_with_name_prefix(en_text)
            vietnamese_sentences = tokenize_sentences_with_name_prefix(vn_text)
            if len(vietnamese_sentences) == len(english_sentences):
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
            else:
                break

        """        
        for i in range(len(vn_article) - 1, -1, -1):
            en_text = en_article[i-index]
            vn_text = vn_article[i]
            english_sentences = tokenize_sentences_with_name_prefix(en_text)
            vietnamese_sentences = tokenize_sentences_with_name_prefix(vn_text)
            if len(vietnamese_sentences) == len(english_sentences):
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
            else:
                break
        """

    return new_en_list, new_vn_list

def write_process_add(lines_en, lines_vn):
    # print("write_process_add")
    if len(lines_en) != len(lines_vn):
        return
    for i in range(len(lines_en)):
        if i == 1:
            continue
        en_text = lines_en[i]
        vn_text = lines_vn[i]
        english_sentences = tokenize_sentences_with_name_prefix(en_text)
        vietnamese_sentences = nltk.sent_tokenize(vn_text)

        if len(english_sentences) == len(vietnamese_sentences):
            # Tạo DataFrame từ danh sách câu tiếng Anh và tiếng Việt đã tách
            df = pd.DataFrame({'English': english_sentences, 'Vietnamese': vietnamese_sentences}, index=None)
            # Ghi vào file 'dic_eng_vn_data.csv'
            df.to_csv('dic_eng_vn_data_new.csv', mode='a', header=False, index=False)


def write_process(lines_en, lines_vn):
    # print("write_process")
    if len(lines_en) != len(lines_vn):
        return
    for i in range(len(lines_en)):
        en_text = lines_en[i]
        vn_text = lines_vn[i]
        english_sentences = tokenize_sentences_with_name_prefix(en_text)
        vietnamese_sentences = nltk.sent_tokenize(vn_text)
        if len(english_sentences) == len(vietnamese_sentences):
            # Tạo DataFrame từ danh sách câu tiếng Anh và tiếng Việt đã tách
            df = pd.DataFrame({'English': english_sentences, 'Vietnamese': vietnamese_sentences}, index=None)
            # Ghi vào file 'dic_eng_vn_data.csv'
            df.to_csv('dic_eng_vn_data_new.csv', mode='a', header=False, index=False)

def write_to_csv():
    # Khai bao
    file_name = 'link_eng_vn_gct_new.csv'
    index_file_name = 'row_number.txt'

    # Lay gia tri
    links_en, links_vn = get_links_from_csv(file_name)
    index = read_number_from_file(index_file_name)
    a =10000
    for i in range(index, index + a):
        write_number_to_file(index_file_name, i+1)
        en_link_index = links_en[i]
        vn_link_index = links_vn[i]
        #print("link sử dụng: "+ en_link_index)
        #print("link sử dụng: " + vn_link_index)

        if "Can not find English Link" in en_link_index:
            # print("Can not find English Link")
            continue

        en_article_content = get_en_article_content(en_link_index)
        vn_article_content = get_vn_article_content(vn_link_index)
        article_title = get_en_article_title(en_link_index)
        text_normalization_en = text_normalization_en_f(en_article_content)
        text_normalization_vn = text_normalization_vn_f(vn_article_content)

        if len(text_normalization_en) != len(text_normalization_vn):
            write_not_use_link_to_csv(en_link_index, vn_link_index)
            text_normalization_en, text_normalization_vn = paragraph_indentation(text_normalization_en,text_normalization_vn)

        write_use_link_to_csv(en_link_index, vn_link_index)
        if "Additional Persecution News" in article_title:
            write_process_add(text_normalization_en, text_normalization_vn)
        else:
            write_process(text_normalization_en, text_normalization_vn)
    write_number_to_file(index_file_name, index + a)

def get_en_line(url):
    # Gửi yêu cầu HTTP để lấy nội dung trang web
    if "Can not" in url:
        return "Can not get article line from web"
    response = requests.get(url)
    if response.status_code == 200:
        # Sử dụng BeautifulSoup để phân tích cú pháp trang web
        soup = BeautifulSoup(response.content, 'html.parser')
        article_title_line = " "
        article_title_tag_byline = soup.find('div', class_='article-byline')
        if not article_title_tag_byline:
            article_title_tag_byline = soup.find('div', class_='dateShare cf')
        if article_title_tag_byline:
            article_title_line = article_title_tag_byline.text.strip()
            parts = article_title_line.split("|")
            if len(parts) > 1:
                article_title_line = parts[1].strip()
        if article_title_line:
            return article_title_line
        else:
            return "Can not find line content"
    else:
        return "Can not connect website"


def get_vn_line(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https:" + url  # Thêm schema "https:" nếu cần
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='articleBody')
        if article_body:
            # Tìm các phần tử con của 'articleBody'
            paragraphs = article_body.find_all('p')
            line = ""
            # Loại bỏ nội dung của đoạn đầu tiên nếu không chứa ký tự "["
            if "[" not in paragraphs[0].get_text(strip=True):
                line = paragraphs[0].get_text().strip()
                return line
            else:
                return "Check html structure"
        else:
            return "Can not get artical content"
    else:
        return "can not connect to website"

def write_line():
    # Khai bao
    file_name = 'link_eng_vn_gct_new.csv'
    index_file_name = 'row_number.txt'

    # Lay gia tri
    links_en, links_vn = get_links_from_csv(file_name)
    index = read_number_from_file(index_file_name)
    a = 10000

    for i in range(index, index + a):
        data = []
        write_number_to_file(index_file_name, i + 1)
        line_en = get_en_line(links_en[i])
        line_vn = get_vn_line(links_vn[i])
        #print(links_en[i])
        #print(links_vn[i])
        # Thêm dữ liệu vào danh sách data
        data.append([line_en, line_vn])

        # Tạo DataFrame từ danh sách data và chỉ định index là None
        df = pd.DataFrame(data, columns=['English_Link', 'Vietnamese_Link'], index=None)

        # Ghi vào file line_en_vn.csv mà không ghi đè dữ liệu
        df.to_csv("dic_eng_vn_data_new.csv", mode='a', header=False, index=False)

    write_number_to_file(index_file_name, index + a)

def get_vn_addition(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https:" + url  # Thêm schema "https:" nếu cần
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_contents = soup.find('div', class_='articleBody')
        if article_contents:
            # Tìm tất cả các đoạn văn bản có chứa ký tự số ở đầu đoạn (ví dụ: 1., 2., 3.)
            paragraphs = article_contents.find_all(['p', 'h3', 'div'])
            filtered_paragraphs = [p.text.strip() for p in paragraphs if re.match(r'^\d+\.', p.text.strip())]
        if len(filtered_paragraphs) > 0:
            filtered_paragraphs = filtered_paragraphs[1:]  # Lấy danh sách từ phần tử thứ hai trở đi
            return filtered_paragraphs
        else:
            return "Can not found infor in article"
    else:
        return "Can not connect to wwebsite"

def get_en_addition(url):
    # Gửi yêu cầu HTTP để lấy nội dung trang web
    if "Can not" in url:
        return "Can not get article line from web"
    response = requests.get(url)
    if response.status_code == 200:
        article_contents = []
        soup = BeautifulSoup(response.content, 'html.parser')
        article_contents_1 = soup.find('div', class_='article-body-content')
        article_contents_2 = soup.find('div', class_='articleZhengwen geo cBBlack')
        article_contents_3 = soup.find('div', class_='articleZhengwen geo')
        if article_contents_1:
            article_contents = article_contents_1
        if article_contents_2:
            article_contents = article_contents_2
        if article_contents_3:
            article_contents = article_contents_3
        if article_contents:
            # Tìm tất cả các đoạn văn bản có chứa ký tự số ở đầu đoạn (ví dụ: 1., 2., 3.)
            paragraphs = article_contents.find_all(['p', 'h3', 'div'])
            filtered_paragraphs = [p.text.strip() for p in paragraphs if re.match(r'^\d+\.', p.text.strip())]
        if len(filtered_paragraphs) > 0:
            filtered_paragraphs = filtered_paragraphs[1:]  # Lấy danh sách từ phần tử thứ hai trở đi

        if filtered_paragraphs:
            return filtered_paragraphs
        else:
            return "Can not found infor in article"
    else:
            return "Can not connect to wwebsite"

def extract_proper_nouns_vn(text):

    # Loại bỏ các ký số dạng "1." hoặc "2." hoặc "3." khỏi văn bản
    text_without_numbers = re.sub(r'\d+\.\s*', '', text)

    # Tách đoạn văn bản đã loại bỏ ký số thành các phần tử
    pattern = r'\[|,|;|\]|và'
    elements = re.split(pattern, text_without_numbers)
    for i in range(len(elements)):
        elements[i] = elements[i].replace("Hồ sơ", "Remove").replace("Vụ án", "Remove").replace("Vụ án", "Remove").strip()
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


    return result
def extract_proper_nouns_en(text):
    # Tải mô hình ngôn ngữ tiếng Anh
    # Loại bỏ các ký số dạng "1." hoặc "2." hoặc "3." khỏi văn bản
    text_without_numbers = re.sub(r'\d+\.\s*', '', text)

    # Tách đoạn văn bản đã loại bỏ ký số thành các phần tử
    pattern = r'\[|,|;|\]| and '
    elements = re.split(pattern, text_without_numbers)

    # Loại bỏ khoảng trắng thừa ở đầu và cuối mỗi phần tử (nếu có)
    elements = [element.strip() for element in elements if element.strip()]
    words_to_remove = ["Whereabouts Unknown","Her Job Contract Terminated","Four Months in","Family", "Members" ,"Prison","Court", "Others", "Face", "Trial", "Sent", "Sentenced", "Arrested", "Detained", "Harassed", "Submitted", "Framed", "Home", "Ransacked"]
    # Duyệt qua từng phần tử trong danh sách
    for i in range(len(elements)):
        # Loại bỏ các từ khỏi phần tử hiện tại
        for word in words_to_remove:
            elements[i] = elements[i].replace(word, "")
    # Loại bỏ các phần tử trống khỏi danh sách
    elements = [element for element in elements if element.strip() != ""]


    return elements

def write_addition():
    # Khai bao
    file_name = 'link_eng_vn_gct_new.csv'
    index_file_name = 'row_number.txt'

    # Lay gia tri
    links_en, links_vn = get_links_from_csv(file_name)
    index = read_number_from_file(index_file_name)
    a = 1000
    for i in range(index, index + a):
        write_number_to_file(index_file_name, i + 1)
        text_en = get_en_addition(links_en[i])
        text_vn = get_vn_addition(links_vn[i])
        article_title = get_en_article_title(links_en[i])
        if "Additional Persecution News" in article_title:
            if len(text_en) == len(text_vn):
                for j in range(len(text_en)):
                    list_en = extract_proper_nouns_en(text_en[j])
                    list_vn =extract_proper_nouns_vn(text_vn[j])
                    if len(list_en) > len(list_vn):
                        for h in range(len(list_vn)):
                            data = {'English': list_en[h], 'Vietnamese': list_vn[h]}
                            # Tạo DataFrame từ danh sách data
                            df = pd.DataFrame([data])  # Đặt dữ liệu trong dấu [ ] để tạo DataFrame từ danh sách
                            df.to_csv('new_addition.csv', mode='a', header=False, index=False)
                    else:
                        for h in range(len(list_en)):
                            data = {'English': list_en[h], 'Vietnamese': list_vn[h]}
                            # Tạo DataFrame từ danh sách data
                            df = pd.DataFrame([data])  # Đặt dữ liệu trong dấu [ ] để tạo DataFrame từ danh sách
                            df.to_csv('new_addition.csv', mode='a', header=False, index=False)
    write_number_to_file(index_file_name, index + a)

def write_title():
    # Khai bao
    file_name = 'link_eng_vn_gct_new.csv'
    index_file_name = 'row_number.txt'

    # Lay gia tri
    links_en, links_vn = get_links_from_csv(file_name)
    index = read_number_from_file(index_file_name)
    a = 13000
    for i in range(index, index + a):
        data = []
        write_number_to_file(index_file_name, i + 1)
        line_en = get_en_article_title(links_en[i])
        line_vn = get_vn_article_title(links_vn[i])
        print(links_en[i])
        print(links_vn[i])
        # Thêm dữ liệu vào danh sách data
        data.append([line_en, line_vn])

        # Tạo DataFrame từ danh sách data và chỉ định index là None
        df = pd.DataFrame(data, columns=['English_Link', 'Vietnamese_Link'], index=None)

        # Ghi vào file line_en_vn.csv mà không ghi đè dữ liệu
        df.to_csv("dic_eng_vn_data_new.csv", mode='a', header=False, index=False)

    write_number_to_file(index_file_name, index + a)


#get_new_link_vn(article_url_GCT)
#get_new_link_en(file_new_gct_vn)
#add_link_to_csv(file_new_gct_en, file_new_gct_vn)

#write_to_csv()
#write_line()
#write_title()
#write_addition()
