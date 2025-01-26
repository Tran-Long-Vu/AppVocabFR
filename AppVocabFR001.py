import tkinter as tk
import random

# Danh sách từ vựng để luyện gõ
word_list = ["hello", "world", "python", "programming", "keyboard", "practice", "typing", "challenge"]

class TypingPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Practice")

        self.current_word = ""
        self.current_index = 0

        # Hiển thị từ cần gõ và nhận nhập liệu
        self.word_label = tk.Label(root, text="", font=("Arial", 24), anchor="center")
        self.word_label.pack(pady=20, fill="x")

        # Hộp nhập dữ liệu
        self.entry = tk.Entry(root, font=("Arial", 24), justify="center")
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.check_typing)

        # Nút bắt đầu
        self.start_button = tk.Button(root, text="Start", font=("Arial", 14), command=self.start_practice)
        self.start_button.pack(pady=10)

    def start_practice(self):
        """Bắt đầu bài luyện gõ."""
        self.next_word()

    def next_word(self):
        """Chọn một từ ngẫu nhiên và đặt lại trạng thái."""
        self.current_word = random.choice(word_list)
        self.current_index = 0
        self.update_word_display()
        self.entry.delete(0, tk.END)

    def update_word_display(self):
        """Cập nhật giao diện hiển thị từ cần gõ."""
        display_text = ""
        for i, char in enumerate(self.current_word):
            if i < self.current_index:
                display_text += f"{char} "  # Ký tự đã gõ đúng hiển thị màu xanh
            else:
                display_text += f"{char} "  # Ký tự chưa gõ hiển thị màu xám
        self.word_label.config(text=display_text, fg="gray")

    def check_typing(self, event):
        """Kiểm tra từng ký tự người dùng gõ."""
        typed_text = self.entry.get()

        if typed_text == self.current_word[:len(typed_text)]:
            self.current_index = len(typed_text)
            self.update_word_display()
            self.word_label.config(fg="green")

            if typed_text == self.current_word:
                self.root.after(500, self.next_word)  # Chuyển sang từ mới sau 0.5 giây
        else:
            self.word_label.config(fg="red")
            self.entry.delete(0, tk.END)
            self.current_index = 0
            self.update_word_display()

# Khởi chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingPracticeApp(root)
    root.mainloop()
