import tkinter as tk
from tkinter import messagebox
from tkinter import font
from update_link import *
from write_to_world import *

waiting_text = "please wait, under processing..."

def search_main_article_link(english_link):
    result_link = []
    vietnamese_link = find_vietnamese_link_1(english_link)
    if "Can not" in vietnamese_link:
        return vietnamese_link
    else:
        result_link.append("Search result:")
        result_link.append(get_en_article_title(english_link))
        result_link.append(get_vn_article_title(vietnamese_link))
        result_link.append(vietnamese_link)
        result_link = "\n".join(result_link)
        return result_link

def search_related_article_link(english_link):
    result_text = []
    result_text.append("Related reports:")
    result_text.append("Bài liên quan:")

    if find_all_var.get() == 1:
        vietnam_link, english_link_list = find_vietnamese_link_2(english_link)
        if english_link_list:
            for i in range(len(english_link_list)):
                # Kiểm tra xem link có chứa "en.minghui.org" hay không
                if "en.minghui.org" in english_link_list[i]:
                    result_text.append(get_en_article_title(english_link_list[i]))
                    result_text.append(get_vn_article_title(vietnam_link[i]))
                    result_text.append(vietnam_link[i])
                    result_text.append("      ")
            result_text_final = "\n".join(result_text)
        else:
            result_text_final = "Have no related link in article"
    else:
        english_text, vietnam_link, english_link = find_vietnamese_link(english_link)
        if english_link:
            for i in range(len(english_link)):
                result_text.append(get_en_article_title(english_link[i]))
                result_text.append(get_vn_article_title(vietnam_link[i]))
                result_text.append(vietnam_link[i])
                result_text.append("      ")
            result_text_final = "\n".join(result_text)
        else:
            result_text_final = "Have no related link in article"

    return result_text_final

def update_new_link():

    get_new_link_vn(article_url_GCT)
    get_new_link_en(file_new_gct_vn)
    add_link_to_csv(file_new_gct_en, file_new_gct_vn)

    get_new_link_vn(article_url_tdth)
    get_new_link_en(file_new_gct_vn)
    add_link_to_csv(file_new_gct_en, file_new_gct_vn)

    get_new_link_vn(article_url_new)
    get_new_link_en(file_new_gct_vn)
    add_link_to_csv(file_new_gct_en, file_new_gct_vn)

    get_new_link_vn(article_url_ddbl)
    get_new_link_en(file_new_gct_vn)
    add_link_to_csv(file_new_gct_en, file_new_gct_vn)

    get_new_link_vn(article_url_tguh)
    get_new_link_en(file_new_gct_vn)
    add_link_to_csv(file_new_gct_en, file_new_gct_vn)


    text = "Update Successful"
    return text


def create_docx_file(url):
    english_artical, link_en, link_cn = write_en_article_to_doc(url)
    english_text = "\n".join(english_artical)
    return english_text
def Auto_Translate(url):
    english_artical = read_paragraph_in_word(url)
    english_text = "\n".join(english_artical)

    return english_text

def text_execute(english, vietnam, in_text):
    count = []
    english_list =  tokenize_sentences_with_name_prefix(english)
    vietnamse_list = tokenize_sentences_with_name_prefix(vietnam)
    for i in range(len(english_list)):
        check_point = False
        for j in range(len(in_text)):
            if in_text[j] in english_list[i]:
                check_point = True
                break
        if check_point:
            count.append(i)
    return english_list, vietnamse_list, count

def update_link():
    update_text = update_new_link()
    display_result(update_text)

def search_main_link():
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    else:
        display_result(waiting_text)
        result = search_main_article_link(user_input)

        display_result(result)


def search_related_link():
    # Xóa nội dung hiển thị kết quả
    pattern = r"^(http:|https:).*\.html$"
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    elif not re.match(pattern, user_input):
            messagebox.showwarning("Warning", "Please input correct link.")
    else:
        display_result(waiting_text)
        result = search_related_article_link(user_input)
        display_result(result)

def article_content():
    # Xóa nội dung hiển thị kết quả
    pattern = r"^(http:|https:).*\.html$"
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    elif not re.match(pattern, user_input):
            messagebox.showwarning("Warning", "Please input correct link.")
    else:
        result = create_docx_file(user_input)
        display_result(result)

def translation():
    # Xóa nội dung hiển thị kết quả
    pattern = r"^(http:|https:).*\.html$"
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    elif not re.match(pattern, user_input):
            messagebox.showwarning("Warning", "Please input correct link.")
    else:
        result = Auto_Translate(user_input)
        display_result(result)


def searc_kv():
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    else:
        result_textbox.delete(1.0, tk.END)
        result_textbox.configure(font=custom_font)
        result_textbox.tag_configure("bold", font=("Helvetica", 11, "bold"))
        result_textbox.tag_configure("italic", font=("Helvetica", 11, "italic"))
        english_text_in, vietname_text_in, in_text, vietname_link = find_translation(user_input)
        if not english_text_in:
            result_textbox.delete(1.0, tk.END)
            result_textbox.insert(tk.END, "Can not found, please check input text")
            return

        english_text, vietname_text, list = text_execute(english_text_in[0], vietname_text_in[0], in_text)
        for i in range(len(english_text)):
            if i in list:
                result_textbox.insert(tk.END, english_text[i] + " ", ("bold",))
            else:
                result_textbox.insert(tk.END, english_text[i] + " ", ("italic",))
        result_textbox.insert(tk.END, "\n")
        result_textbox.insert(tk.END, "======================================================================")
        result_textbox.insert(tk.END, "\n")
        for j in range(len(vietname_text)):
            if j in list:
                result_textbox.insert(tk.END, vietname_text[j] + " ", ("bold",))
            else:
                result_textbox.insert(tk.END, vietname_text[j] + " ", ("italic",))
        result_textbox.insert(tk.END, "\n")
        result_textbox.insert(tk.END, "=======================================================================")
        result_textbox.insert(tk.END, "\n")
        result = "\n".join(vietname_link)
        result_textbox.insert(tk.END, result )


def search_sentence():
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    else:
        search_result = find_sentence(user_input)
        if not search_result:
            result_textbox.delete(1.0, tk.END)
            result_textbox.insert(tk.END, "Can not found, please check input text")
            return
        result = "\n".join(search_result)
        display_result(result)

def clear_text():
    input_text.delete(0, "end")  # Xóa nội dung từ đầu đến cuối của trường văn bản

def copy_text():
    result_text = result_textbox.get("1.0", tk.END)  # Lấy nội dung từ dòng 1, ký tự 0 đến cuối
    root.clipboard_clear()  # Xóa clipboard hiện có
    root.clipboard_append(result_text)  # Đặt nội dung vào clipboard

def display_result(result_text):
    custom_font = font.Font(size=13)
    result_textbox.delete(1.0, tk.END)
    result_textbox.configure(font=custom_font)
    result_textbox.insert(tk.END, result_text)

def search_text_result():
    search_text = input_text.get()  # Lấy nội dung tìm kiếm từ trường văn bản đầu vào
    result_textbox.tag_remove("highlight", "1.0", tk.END)  # Xóa tất cả tag "highlight" hiện tại

    start = "1.0"
    while True:
        start = result_textbox.search(search_text, start, tk.END)
        if not start:
            break
        end = f"{start}+{len(search_text)}c"
        result_textbox.tag_add("highlight", start, end)
        start = end

    if not result_textbox.tag_ranges("highlight"):
        # Không tìm thấy kết quả
        messagebox.showinfo("Thông báo", "Không tìm thấy kết quả tìm kiếm.")




root = tk.Tk()
window_width = 1300
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
# Tạo 6 cột và cho phép co giãn
# Tạo 6 cột và cho phép co giãn

for i in range(6):
    root.grid_columnconfigure(i, weight=1)

# Tạo 4 hàng và cho phép co giãn
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

# Tạo các widget hoặc frame con và đặt chúng trong các cell của grid
for i in range(6):
    for j in range(6):
        frame = tk.Frame(root, bg="#FAF0E6")
        frame.grid(row=i, column=j, sticky='nsew')

button_width = 10
button_width_1 = 8
entry_width = 90 # Đặt giá trị chiều rộng cho Entry widget

# Tạo font in đậm
button_font = font.Font(weight="bold")
# Hàng 1
action_button_1 = tk.Button(root, text="Update New", width=button_width, height=1, command=update_link,bg="#00405d", fg="white",font=button_font)
action_button_1.grid(row=0, column=0, padx=(10, 0), pady=10, sticky='w')

action_button_2 = tk.Button(root, text="Main Link", width=button_width, height=1, command=search_main_link,bg="#00405d", fg="white",font=button_font)
action_button_2.grid(row=0, column=0, padx=(190, 0), pady=10, sticky='w')

action_button_3 = tk.Button(root, text="Related Link", width=button_width, height=1, command=search_related_link,bg="#00405d", fg="white",font=button_font)
action_button_3.grid(row=0, column=0, padx=(380, 0), pady=10, sticky='w')

action_button_4 = tk.Button(root, text="A_Content", width=button_width, height=1, command=article_content,bg="#00405d", fg="white",font=button_font)
action_button_4.grid(row=0, column=0, padx=(1140, 0), pady=10, sticky='w')

action_button_5 = tk.Button(root, text="KV_Search", width=button_width, height=1, command=searc_kv,bg="#00405d", fg="white",font=button_font)
action_button_5.grid(row=0, column=0, padx=(760, 0), pady=10, sticky='w')

action_button_6 = tk.Button(root, text="Auto_Trans", width=button_width, height=1, command=translation,bg="#00405d", fg="white",font=button_font)
action_button_6.grid(row=0, column=0, padx=(950, 0), pady=10, sticky='w')

action_button_7 = tk.Button(root, text="VHM_text", width=button_width, height=1, command=search_sentence,bg="#00405d", fg="white",font=button_font)
action_button_7.grid(row=0, column=0, padx=(570, 0), pady=10, sticky='w')


# Hàng 2
label_font = font.Font(family="Helvetica", size=15)
# Tạo Label widget và sử dụng font đã chỉ định
input_label = tk.Label(root, text="Search Text", font=label_font, bg="white", fg="black")
input_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky='w')

# Tạo một font với chiều cao mong muốn
custom_font = font.nametofont("TkDefaultFont")
custom_font.configure(size=15)  # Thay đổi size để điều chỉnh chiều cao

# Tạo một tk.Entry và sử dụng font đã chỉ định
input_text = tk.Entry(root, width=entry_width, font=custom_font)
input_text.grid(row=1, column=0, padx=(150, 0), pady=0, sticky='w')

# Tạo một nút "Clear" để xóa nội dung trường văn bản
button_font = font.Font(family="Helvetica", size=13)
clear_button = tk.Button(root, text="Clr", width=6, height=1, command=clear_text, font=button_font, bg="white", fg="black")
clear_button.grid(row=1, column=0, padx=(1130, 0), pady=0, sticky='w')


# Tạo Label widget và sử dụng font đã chỉ định
result_label = tk.Label(root, text="Result text", font=label_font, bg="white", fg="black")
result_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky='w')

# Tạo nút "Copy" để sao chép nội dung từ vùng văn bản đa dòng
copy_button = tk.Button(root, text="Copy text result", width=20, height=1, command=copy_text, font=button_font, bg="white", fg="black")
copy_button.grid(row=2, column=0, padx=(150, 0), pady=0, sticky='w')

find_all_var = tk.IntVar()

# Tạo checkbox "Find All Link" và liên kết nó với biến find_all_var
find_all_checkbox = tk.Checkbutton(root, text="All Link", width=10, height=1, variable=find_all_var, font=button_font, bg="white", fg="black")
find_all_checkbox.grid(row=2, column=0, padx=(380, 0), pady=0, sticky='w')

search_button = tk.Button(root, text="Search Text Result", width=20, height=1, command=search_text_result, font=button_font, bg="white", fg="black")
search_button.grid(row=2, column=0, padx=(550, 0), pady=0, sticky='w')



# Tạo Text widget với wrap="word" để tự động xuống dòng khi cần
result_textbox = tk.Text(root, height=18, width=100, wrap="word")
result_textbox.grid(row=3, column=0, padx=(10, 0), pady=10, sticky='w')

# Tạo thanh cuộn theo chiều dọc
scrollbar = tk.Scrollbar(root, orient="vertical", command=result_textbox.yview)
scrollbar.grid(row=3, column=0, padx=(1130, 0), pady=10, sticky="ns")

result_textbox.config(yscrollcommand=scrollbar.set)


result_textbox.tag_configure("highlight", font=font.Font(weight="bold"))

title_font = font.Font(family="Helvetica", size=20, weight="bold")  # Điều chỉnh family, size, và weight theo mong muốn
root.title("SEARCHING TOOL")
root.option_add("*TLabel*Font", title_font)
root.option_add("*TLabel*Foreground", "blue")  # Đổi màu chữ của title thành màu xanh

root.mainloop()
