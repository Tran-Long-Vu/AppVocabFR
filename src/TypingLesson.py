import tkinter as tk
import pyttsx3
import threading, queue
import json 
# global_libs:







# global vars:
# --- Global variables ---
current_lesson_index = 0
current_word_index = 0
special_liaison = {
  "bon appétit": "bon\u2060appétit",
  
}
pending_accent = None




class TypingLesson():
  def __init__(self):
    self.accent_map = self.read_json("accent_map.json")
    self.lessons = self.read_json("lessons.json")
    self.lesson_topics =  self.read_json("lesson_topics.json")
    self.pending_accent = None
    self.current_lesson_index = 0
    self.current_word_index = 0
    self.special_liaison = {
    "bon appétit": "bon\u2060appétit",  
    }
    self.tts_queue = queue.Queue()
    self.engine = pyttsx3.init()
    self.engine.setProperty('rate', 140)
    self.engine.setProperty('volume', 1.0)
    self.voices = self.engine.getProperty('voices')
    self.french_voice = None
    
    for voice in self.voices:
      try:
        langs = [lang.decode('utf-8') for lang in voice.languages]
      except Exception:
        langs = voice.languages
      if any("fr" in lang.lower() for lang in langs) or "french" in voice.name.lower():
        french_voice = voice.id
        break
    if french_voice:
      self.engine.setProperty('voice', french_voice)
    self.tts_thread = threading.Thread(target=self.tts_worker, daemon=True)
    self.tts_thread.start()
    self.run_app()
    pass

      
  def run_app(self):
    self.root = tk.Tk()
    self.root.title("French Typing Trainer")
    self.root.geometry("650x550")
    self.root.configure(bg="#f7f7f7")

    self.control_frame = tk.Frame(self.root, bg="#d0e1f9", bd=2, relief=tk.RIDGE, padx=10, pady=5)
    self.control_frame.pack(fill=tk.X, padx=10, pady=10)
    self.lesson_label = tk.Label(self.control_frame, text="Chọn bài:", font=("Helvetica", 12, "bold"), bg="#d0e1f9")

    self.lesson_label.pack(side=tk.LEFT, padx=5)
    self.selected_lesson = tk.StringVar(self.control_frame)
    self.selected_lesson.set("Bài 1")
    self.selected_lesson.trace("w", self.change_lesson) # Changed to self.change_lesson
    self.option_menu = tk.OptionMenu(self.control_frame, self.selected_lesson, *[f"Bài {i+1}" for i in range(len(self.lessons))])
    self.option_menu.config(font=("Helvetica", 12))
    self.option_menu.pack(side=tk.LEFT, padx=5)
    self.next_lesson_button = tk.Button(self.control_frame, text="Bài tiếp theo", font=("Helvetica", 12), command=self.next_lesson, bg="#87CEFA") # Changed to self.next_lesson
    self.next_lesson_button.pack(side=tk.LEFT, padx=5)
    self.speak_button = tk.Button(self.control_frame, text="Nghe phát âm", font=("Helvetica", 12), command=self.speak_current_word, bg="#87CEFA") # Changed to self.speak_current_word
    self.speak_button.pack(side=tk.LEFT, padx=5)

    self.content_frame = tk.Frame(self.root, bg="#f7f7f7")
    self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    self.topic_label = tk.Label(self.content_frame, text="", font=("Helvetica", 16, "italic"), bg="#f7f7f7", anchor="w", justify="left")
    self.topic_label.pack(fill=tk.X, padx=5, pady=2)
    self.word_label = tk.Label(self.content_frame, text="", font=("Helvetica", 18, "bold"), bg="#f7f7f7", anchor="w", justify="left")
    self.word_label.pack(fill=tk.X, padx=5, pady=5)
    self.ipa_label = tk.Label(self.content_frame, text="", font=("Helvetica", 14), bg="#f7f7f7", anchor="w", justify="left")
    self.ipa_label.pack(fill=tk.X, padx=5, pady=2)
    self.definition_label = tk.Label(self.content_frame, text="", font=("Helvetica", 14), bg="#f7f7f7", anchor="w", justify="left")
    self.definition_label.pack(fill=tk.X, padx=5, pady=2)
    self.info_label = tk.Label(self.content_frame, text="", font=("Helvetica", 14), bg="#f7f7f7", anchor="w", justify="left")
    self.info_label.pack(fill=tk.X, padx=5, pady=2)

    self.entry = tk.Entry(self.root, font=("Helvetica", 16), width=40)
    self.entry.pack(pady=10)
    self.entry.focus_set()
    self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f7f7f7")
    self.feedback_label.pack(pady=5)
    self.entry.bind("<Key>", self.on_key_press) # Corrected to self.on_key_press
    self.entry.bind("<KeyRelease>", self.replace_ligature) # Corrected to self.replace_ligature
    self.entry.bind("<Return>", self.check_input) # Corrected to self.check_input

    self.show_current_word()  # Changed to self.show_current_word
    self.root.mainloop()


    pass

  def read_json(self, filename="accent_map.json"):
      """
      Reads a JSON file and returns the data as a Python dictionary.
      Defaults to reading from a file named "accent_map.json".
      """
      try:
          with open(filename, 'r', encoding='utf-8') as f:  # Specify encoding for broader compatibility
              data = json.load(f)
          return data
      except FileNotFoundError:
          print(f"Error: File '{filename}' not found.")
          return None  # Or raise the exception, depending on desired behavior
      except json.JSONDecodeError:
          print(f"Error: Could not decode JSON from file '{filename}'.  Check for syntax errors.")
          return None # Or raise the exception
      except Exception as e:
          print(f"An unexpected error occurred: {e}")
          return None 



  def tts_worker(self):
    while True:
      text = self.tts_queue.get()
      if text is None:
        break
      self.engine.say(text)
      self.engine.runAndWait()
      self.tts_queue.task_done()  

    pass

  def speak_current_word(self):
    current_entry = self.lessons[current_lesson_index][current_word_index]
    word_to_speak = current_entry["word"]
    if word_to_speak in special_liaison:
      tts_word = special_liaison[word_to_speak]
    else:
      tts_word = word_to_speak.replace("œ", "oe") #Log Err: chỗ này nếu không thay bằng "oe" thì sẽ bị đọc sai!!!
    self.tts_queue.put(tts_word) 
    pass

  def on_key_press(self, event):
    global pending_accent
    widget = event.widget
    char = event.char
    if not char:
      return
    if pending_accent:
      if char == pending_accent:
        widget.insert(tk.INSERT, pending_accent)
        pending_accent = None
        return "break"
      if char in self.accent_map[pending_accent]:
        accented_char = self.accent_map[pending_accent][char]
        widget.insert(tk.INSERT, accented_char)
        pending_accent = None
        return "break"
      else:
        widget.insert(tk.INSERT, pending_accent)
        pending_accent = None
    if char in self.accent_map:
      pending_accent = char
      return "break"


  def replace_ligature(self , event):
    widget = event.widget
    text = widget.get()
    if len(text) >= 2:
      if text[-2:] == "oe":
        widget.delete(len(text)-2, tk.END)
        widget.insert(tk.END, "œ")
      elif text[-2:] == "OE":
        widget.delete(len(text)-2, tk.END)
        widget.insert(tk.END, "Œ")


    pass
  def show_current_word(self):
    global current_lesson_index, current_word_index
    current_entry = self.lessons[current_lesson_index][current_word_index]
    word = current_entry["word"]
    ipa = current_entry["ipa"]
    definition = current_entry["definition"]
    pos = current_entry["pos"]
    gender = current_entry["gender"]
    number = current_entry["number"]
    self.topic_label.config(text=f"Chủ đề: {self.lesson_topics[current_lesson_index]}")
    self.word_label.config(text=f"Nhập từ: {word}")
    self.ipa_label.config(text=f"Phiên âm: {ipa}")
    self.definition_label.config(text=f"Định nghĩa: {definition}")
    self.info_label.config(text=f"Từ loại: {pos} | Giống: {gender} | Số: {number}")
    self.entry.delete(0, tk.END)
    self.feedback_label.config(text="")
    self.root.after(500, self.speak_current_word)
    
    
    pass

  def check_input(self):
    global current_lesson_index, current_word_index
    if current_word_index >= len(self.lessons[current_lesson_index]):
      self.next_lesson()
      return "break"
    user_input = self.entry.get()
    current_entry = self.lessons[current_lesson_index][current_word_index]
    if user_input == current_entry["word"]:
      self.feedback_label.config(text=f"Bạn đã nhập đúng từ '{current_entry['word']}'!")
      self.root.after(1000, self.next_word)
    else:
      self.feedback_label.config(text="Sai rồi! Bắt đầu lại.")
      self.entry.delete(0, tk.END)



    pass


  def next_word(self):
    global current_word_index, current_lesson_index
    self.entry.delete(0, tk.END)
    current_word_index += 1
    if current_word_index >= len(self.lessons[current_lesson_index]):
      self.word_label.config(text=f"Bạn đã hoàn thành bài {current_lesson_index+1}!")
      self.ipa_label.config(text="")
      self.definition_label.config(text="")
      self.info_label.config(text="")
      self.feedback_label.config(text="Nhấn Enter hoặc chọn bài mới để luyện tiếp.")
      return
    self.show_current_word()

    pass
  def next_lesson(self):
    global current_lesson_index, current_word_index
    if current_lesson_index < len(self.lessons) - 1:
      current_lesson_index += 1
      current_word_index = 0
      self.show_current_word()
    else:
      self.feedback_label.config(text="Đây là bài cuối cùng.")
    pass


  def change_lesson(self):
    global current_lesson_index, current_word_index
    selected = self.selected_lesson.get()
    try:
      lesson_num = int(selected.split()[1])
      current_lesson_index = lesson_num - 1
      current_word_index = 0
      self.show_current_word()
    except Exception as e:
      self.feedback_label.config(text="Lựa chọn bài không hợp lệ.")
    

    pass 


  pass



if __name__ == "__main__":
    typinglesson = TypingLesson()
    # typinglesson.run_app()
    pass



