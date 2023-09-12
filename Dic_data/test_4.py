import pandas as pd

# Đọc tệp CSV vào DataFrame, bỏ qua các dòng có lỗi
try:
    df = pd.read_csv('unique_rows.csv', header=None)  # Đặt header=None để không sử dụng tên cột
except pd.errors.ParserError as e:
    print(f"Lỗi khi đọc tệp CSV: {e}")
    df = None  # Gán df bằng None để đảm bảo nó được định nghĩa

# Kiểm tra xem df có được định nghĩa hay không
if df is not None:
    # Tạo một DataFrame mới để lưu trữ các hàng đã được xử lý
    processed_df = pd.DataFrame(columns=[0, 1])

    # Duyệt qua từng hàng của DataFrame
    for index, row in df.iterrows():
        # Loại bỏ khoảng trắng không cần thiết ở cột 1 và cột 2
        column1 = ' '.join(row[0].split())
        column2 = ' '.join(row[1].split())

        # Kiểm tra điều kiện "hoặc" cho cả hai cột
        if len(column1.split()) > 4 or (len(column2.split()) > 4 and "thành phố" not in column2):
            # Thêm hàng đã xử lý vào DataFrame mới
            processed_df = processed_df.append({0: column1, 1: column2}, ignore_index=True)

    # Ghi DataFrame mới vào file CSV tương ứng
    processed_df.to_csv('processed_rows.csv', header=False, index=False)
