import pandas as pd

# Đọc tệp CSV vào DataFrame
try:
    df = pd.read_csv('dic_eng_vn_data.csv')
except pd.errors.ParserError as e:
    print(f"Lỗi khi đọc tệp CSV: {e}")
    df = None

# Kiểm tra xem df có được định nghĩa hay không
if df is not None:
    # Tạo một danh sách để lưu trữ các hàng thỏa mãn điều kiện
    rows_with_condition = []

    # Tạo một danh sách để lưu trữ các hàng không thỏa mãn điều kiện
    rows_no_condition = []

    # Duyệt qua từng hàng của DataFrame
    for index, row in df.iterrows():
        # Tách nội dung của cột 'English' và 'Vietnamese' thành các từ
        words_in_english = row[0].split()
        words_in_vietnamese = row[1].split()

        # Kiểm tra điều kiện
        if (len(words_in_english) >= 2 * len(words_in_vietnamese)) or (len(words_in_vietnamese) >= 2 * len(words_in_english)):
            if len(words_in_english) > 30 or len(words_in_english) > 30:
                rows_with_condition.append(row)
            else:
                rows_no_condition.append(row)
        else:
            rows_no_condition.append(row)

    # Kiểm tra xem có hàng nào thỏa mãn điều kiện hay không
    if len(rows_with_condition) > 0:
        # Tạo DataFrame mới từ danh sách các hàng thỏa mãn điều kiện
        result_df = pd.DataFrame(rows_with_condition, columns=df.columns)

        # Ghi vào tệp CSV 'rows_with_condition.csv'
        result_df.to_csv('rows_with_condition.csv', index=False)

    # Tạo DataFrame mới từ danh sách các hàng không thỏa mãn điều kiện
    result_no_condition_df = pd.DataFrame(rows_no_condition, columns=df.columns)

    # Ghi vào tệp CSV 'rows_no_condition.csv'
    result_no_condition_df.to_csv('rows_no_condition.csv', index=False)

    print("Đã ghi tệp 'rows_with_condition.csv' cho các hàng thỏa mãn điều kiện.")
    print("Đã ghi tệp 'rows_no_condition.csv' cho các hàng không thỏa mãn điều kiện.")
else:
    print("Không thể thực hiện vì không có DataFrame.")
