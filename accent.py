import tkinter as tk

# Bảng ánh xạ cho các dead key
accent_map = {
    "'": {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú',
          'A': 'Á', 'E': 'É', 'I': 'Í', 'O': 'Ó', 'U': 'Ú'},
    "`": {'a': 'à', 'e': 'è', 'i': 'ì', 'o': 'ò', 'u': 'ù',
          'A': 'À', 'E': 'È', 'I': 'Ì', 'O': 'Ò', 'U': 'Ù'},
    "^": {'a': 'â', 'e': 'ê', 'i': 'î', 'o': 'ô', 'u': 'û',
          'A': 'Â', 'E': 'Ê', 'I': 'Î', 'O': 'Ô', 'U': 'Û'},
    '"': {'a': 'ä', 'e': 'ë', 'i': 'ï', 'o': 'ö', 'u': 'ü',
          'A': 'Ä', 'E': 'Ë', 'I': 'Ï', 'O': 'Ö', 'U': 'Ü'},
    # Thêm mapping cho chữ c cédille: gõ dấu phẩy sau đó gõ chữ c (hoặc C) sẽ tạo ra 'ç' (hoặc 'Ç')
    ",": {'c': 'ç', 'C': 'Ç'},
}

# Biến toàn cục lưu dead key đang chờ xử lý
pending_accent = None

def on_key_press(event):
    """
    Xử lý sự kiện gõ phím để chuyển dead key thành ký tự có dấu nếu có mapping.
    Nếu không có mapping, dead key sẽ được in ra như một ký tự thông thường.
    """
    global pending_accent
    widget = event.widget
    char = event.char

    # Nếu phím không có ký tự (ví dụ: phím chức năng) thì bỏ qua.
    if not char:
        return

    # Nếu đã có dead key chờ, kiểm tra ký tự hiện tại có mapping hay không.
    if pending_accent:
        if char in accent_map[pending_accent]:
            # Nếu có mapping, in ký tự có dấu thay cho dead key + ký tự gõ.
            accented_char = accent_map[pending_accent][char]
            widget.insert(tk.INSERT, accented_char)
            pending_accent = None
            return "break"  # Ngăn ký tự gốc được in ra.
        else:
            # Nếu không có mapping, in dead key như ký tự thông thường rồi xử lý ký tự hiện tại.
            widget.insert(tk.INSERT, pending_accent)
            pending_accent = None
            # Sau đó cho phép ký tự hiện tại được xử lý như thường.

    # Nếu ký tự gõ vào là một dead key đã được định nghĩa, lưu lại và không in ngay.
    if char in accent_map:
        pending_accent = char
        return "break"

    # Các ký tự khác được xử lý theo mặc định.

# Tạo cửa sổ Tkinter
root = tk.Tk()
root.title("Nhập liệu tiếng Pháp (Hỗ trợ chữ c cédille)")

# Sử dụng Text widget để nhập liệu nhiều dòng
text_widget = tk.Text(root, width=50, height=10, font=("Arial", 14))
text_widget.pack(padx=10, pady=10)

# Ràng buộc sự kiện gõ phím
text_widget.bind("<Key>", on_key_press)

root.mainloop()
