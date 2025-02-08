import tkinter as tk
import pyttsx3
import threading, queue

# --- Hỗ trợ dead key & ligature ---
accent_map = {
    "'": {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú',
          'A': 'Á', 'E': 'É', 'I': 'Í', 'O': 'Ó', 'U': 'Ú'},
    "`": {'a': 'à', 'e': 'è', 'i': 'ì', 'o': 'ò', 'u': 'ù',
          'A': 'À', 'E': 'È', 'I': 'Ì', 'O': 'Ò', 'U': 'Ù'},
    "^": {'a': 'â', 'e': 'ê', 'i': 'î', 'o': 'ô', 'u': 'û',
          'A': 'Â', 'E': 'Ê', 'I': 'Î', 'O': 'Ô', 'U': 'Û'},
    '"': {'a': 'ä', 'e': 'ë', 'i': 'ï', 'o': 'ö', 'u': 'ü',
          'A': 'Ä', 'E': 'Ë', 'I': 'Ï', 'O': 'Ö', 'U': 'Ü'},
    ",": {'c': 'ç', 'C': 'Ç'},
}
pending_accent = None

# --- Dữ liệu từ vựng & chủ đề (3 bài học) ---
lessons = [
  [  # Bài 1: Chào hỏi
    {"word": "Bonjour, comment ça va ?", "ipa": "[bɔ̃ʒuʁ kɔmɑ̃ sa va]", "definition": "Xin chào, bạn khỏe không?", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Salut, ça va ?", "ipa": "[saly sa va]", "definition": "Chào, khỏe không?", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Bonsoir, comment allez-vous ?", "ipa": "[bɔ̃swaʁ kɔmɑ̃ tale vu]", "definition": "Chào buổi tối, quý vị khỏe không?", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Bonne journée", "ipa": "[bɔn ʒuʁne]", "definition": "Chúc một ngày tốt lành", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Bonne soirée", "ipa": "[bɔn swaʁe]", "definition": "Chúc buổi tối tốt lành", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "À bientôt", "ipa": "[a bjɛ̃to]", "definition": "Hẹn gặp lại", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Au revoir", "ipa": "[o ʁəvwaʁ]", "definition": "Tạm biệt", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Enchanté de vous rencontrer", "ipa": "[ɑ̃ʃɑ̃te də vu ʁɑ̃kɔ̃tʁe]", "definition": "Rất vui được gặp bạn", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Bienvenue", "ipa": "[bjɛ̃vny]", "definition": "Chào mừng", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "À tout à l'heure", "ipa": "[a tu ta lœʁ]", "definition": "Hẹn gặp lại sau", "pos": "phrase", "gender": "n/a", "number": "n/a"}
  ],
  [  # Bài 2: Thực phẩm
    {"word": "Pain frais", "ipa": "[pɛ̃ fʁɛ]", "definition": "Bánh mì tươi", "pos": "phrase", "gender": "masculine", "number": "singular"},
    {"word": "Fromage de chèvre", "ipa": "[fʁɔmaʒ də ʃɛvʁ]", "definition": "Phô mai dê", "pos": "phrase", "gender": "masculine", "number": "singular"},
    {"word": "Vin rouge", "ipa": "[vɛ̃ ʁuʒ]", "definition": "Rượu vang đỏ", "pos": "phrase", "gender": "masculine", "number": "singular"},
    {"word": "Eau minérale", "ipa": "[o mineʁal]", "definition": "Nước khoáng", "pos": "phrase", "gender": "feminine", "number": "singular"},
    {"word": "Fruits frais", "ipa": "[fʁɥi fʁɛ]", "definition": "Trái cây tươi", "pos": "phrase", "gender": "masculine", "number": "plural"},
    {"word": "Légumes verts", "ipa": "[leɡym vɛʁ]", "definition": "Rau xanh", "pos": "phrase", "gender": "masculine", "number": "plural"},
    {"word": "Bœuf bourguignon", "ipa": "[bœf buʁɡiɲɔ̃]", "definition": "Thịt bò hầm vang", "pos": "phrase", "gender": "masculine", "number": "singular"},
    {"word": "Poulet rôti", "ipa": "[pule ʁo.ti]", "definition": "Gà quay", "pos": "phrase", "gender": "masculine", "number": "singular"},
    {"word": "Crème brûlée", "ipa": "[kʁɛm bʁyle]", "definition": "Kem caramen", "pos": "phrase", "gender": "feminine", "number": "singular"},
    {"word": "Café au lait", "ipa": "[kafe o lɛ]", "definition": "Cà phê sữa", "pos": "phrase", "gender": "masculine", "number": "singular"}
  ],
  [  # Bài 3: Giao tiếp
    {"word": "S'il vous plaît", "ipa": "[sil vu plɛ]", "definition": "Làm ơn", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Merci beaucoup", "ipa": "[mɛʁsi boku]", "definition": "Cảm ơn rất nhiều", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "De rien", "ipa": "[də ʁjɛ̃]", "definition": "Không có gì", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Excusez-moi", "ipa": "[ɛkskyze mwa]", "definition": "Xin lỗi", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Je ne sais pas", "ipa": "[ʒə nə sɛ pa]", "definition": "Tôi không biết", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Comment ça s'appelle ?", "ipa": "[kɔmɑ̃ sa sapɛl]", "definition": "Tên bạn là gì?", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Enchanté de vous rencontrer", "ipa": "[ɑ̃ʃɑ̃te də fɛʁ vɔtʁ kɔnɛsɑ̃s]", "definition": "Rất vui được gặp bạn", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Pardon, répétez s'il vous plaît", "ipa": "[paʁdɔ̃ ʁepete sil vu plɛ]", "definition": "Xin lỗi, nhắc lại được không?", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "Je suis désolé", "ipa": "[ʒə sɥi dezɔle]", "definition": "Tôi xin lỗi", "pos": "phrase", "gender": "n/a", "number": "n/a"},
    {"word": "C'est très intéressant", "ipa": "[se tʁɛ ɛ̃teʁɛsɑ̃]", "definition": "Thật thú vị", "pos": "phrase", "gender": "n/a", "number": "n/a"}
  ],
  [  # Bài 4: Gia đình
    {"word": "La mère", "ipa": "[la mɛʁ]", "definition": "Mẹ", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le père", "ipa": "[lə pɛʁ]", "definition": "Bố", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La sœur", "ipa": "[la sœʁ]", "definition": "Chị/em gái", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le frère", "ipa": "[lə fʁɛʁ]", "definition": "Anh/em trai", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La famille", "ipa": "[la famij]", "definition": "Gia đình", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Les enfants", "ipa": "[le zɑ̃fɑ̃]", "definition": "Trẻ em", "pos": "noun", "gender": "masculine", "number": "plural"},
    {"word": "La grand-mère", "ipa": "[la ɡʁɑ̃ mɛʁ]", "definition": "Bà", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le grand-père", "ipa": "[lə ɡʁɑ̃ pɛʁ]", "definition": "Ông", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "Le cousin", "ipa": "[lə kuzɛ̃]", "definition": "Anh em họ (nam)", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La cousine", "ipa": "[la kuzin]", "definition": "Anh em họ (nữ)", "pos": "noun", "gender": "feminine", "number": "singular"}
  ],
  [  # Bài 5: Thời tiết
    {"word": "Le soleil", "ipa": "[lə sɔlɛj]", "definition": "Mặt trời", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La pluie", "ipa": "[la plɥi]", "definition": "Mưa", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le vent", "ipa": "[lə vɑ̃]", "definition": "Gió", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La neige", "ipa": "[la nɛʒ]", "definition": "Tuyết", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le nuage", "ipa": "[lə nɥaʒ]", "definition": "Mây", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "L'orage", "ipa": "[lɔʁaʒ]", "definition": "Bão", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "Le brouillard", "ipa": "[lə bʁujaʁ]", "definition": "Sương mù", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La tempête", "ipa": "[la tɑ̃pɛt]", "definition": "Bão tố", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le tonnerre", "ipa": "[lə tɔnɛʁ]", "definition": "Sấm sét", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "L'éclair", "ipa": "[lek.lɛʁ]", "definition": "Chớp", "pos": "noun", "gender": "masculine", "number": "singular"}
  ],
  [  # Bài 6: Số đếm
    {"word": "Un", "ipa": "[œ̃]", "definition": "Một", "pos": "number", "gender": "masculine", "number": "singular"},
    {"word": "Deux", "ipa": "[dø]", "definition": "Hai", "pos": "number", "gender": "n/a", "number": "n/a"},
    {"word": "Trois", "ipa": "[tʁwa]", "definition": "Ba", "pos": "number", "gender": "n/a", "number": "n/a"},
    {"word": "Quatre", "ipa": "[katʁ]", "definition": "Bốn", "pos": "number", "gender": "n/a", "number": "n/a"},
    {"word": "Cinq", "ipa": "[sɛ̃k]", "definition": "Năm", "pos": "number", "gender": "n/a", "number": "n/a"},
    {"word": "Six", "ipa": "[sis]", "definition": "Sáu", "pos": "number", "gender": "n/a", "number": "n/a"},
    {"word": "Sept", "ipa": "[sɛt]", "definition": "Bảy", "pos": "number", "gender": "n/a", "number": "n/a"},
    {"word": "Huit", "ipa": "[ɥit]", "definition": "Tám", "pos": "number", "gender": "n/a", "number": "n/a"},
    {"word": "Neuf", "ipa": "[nœf]", "definition": "Chín", "pos": "number", "gender": "n/a", "number": "n/a"},
    {"word": "Dix", "ipa": "[dis]", "definition": "Mười", "pos": "number", "gender": "n/a", "number": "n/a"}
  ],
  [  # Bài 7: Màu sắc
    {"word": "Rouge", "ipa": "[ʁuʒ]", "definition": "Đỏ", "pos": "adjective", "gender": "masculine", "number": "singular"},
    {"word": "Bleu", "ipa": "[blø]", "definition": "Xanh dương", "pos": "adjective", "gender": "masculine", "number": "singular"},
    {"word": "Jaune", "ipa": "[ʒon]", "definition": "Vàng", "pos": "adjective", "gender": "n/a", "number": "n/a"},
    {"word": "Vert", "ipa": "[vɛʁ]", "definition": "Xanh lá", "pos": "adjective", "gender": "masculine", "number": "singular"},
    {"word": "Noir", "ipa": "[nwaʁ]", "definition": "Đen", "pos": "adjective", "gender": "masculine", "number": "singular"},
    {"word": "Blanc", "ipa": "[blɑ̃]", "definition": "Trắng", "pos": "adjective", "gender": "masculine", "number": "singular"},
    {"word": "Rose", "ipa": "[ʁoz]", "definition": "Hồng", "pos": "adjective", "gender": "feminine", "number": "singular"},
    {"word": "Violet", "ipa": "[vjo.lɛ]", "definition": "Tím", "pos": "adjective", "gender": "masculine", "number": "singular"},
    {"word": "Gris", "ipa": "[ɡʁi]", "definition": "Xám", "pos": "adjective", "gender": "masculine", "number": "singular"},
    {"word": "Marron", "ipa": "[ma.ʁɔ̃]", "definition": "Nâu", "pos": "adjective", "gender": "masculine", "number": "singular"}
  ],
  [  # Bài 8: Trang phục
    {"word": "La chemise", "ipa": "[la ʃə.miz]", "definition": "Áo sơ mi", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le pantalon", "ipa": "[lə pɑ̃.ta.lɔ̃]", "definition": "Quần dài", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La robe", "ipa": "[la ʁɔb]", "definition": "Váy", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le costume", "ipa": "[lə kɔs.tym]", "definition": "Bộ vest", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La jupe", "ipa": "[la ʒyp]", "definition": "Chân váy", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Les chaussures", "ipa": "[le ʃo.syʁ]", "definition": "Giày dép", "pos": "noun", "gender": "feminine", "number": "plural"},
    {"word": "Le manteau", "ipa": "[lə mɑ̃.to]", "definition": "Áo khoác", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La casquette", "ipa": "[la kas.kɛt]", "definition": "Mũ lưỡi trai", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Les chaussettes", "ipa": "[le ʃo.sɛt]", "definition": "Tất", "pos": "noun", "gender": "feminine", "number": "plural"},
    {"word": "Les lunettes", "ipa": "[le lynɛt]", "definition": "Kính mắt", "pos": "noun", "gender": "feminine", "number": "plural"}
  ],
  [  # Bài 9: Cơ thể
    {"word": "La tête", "ipa": "[la tɛt]", "definition": "Đầu", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le bras", "ipa": "[lə bʁɑ]", "definition": "Cánh tay", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La main", "ipa": "[la mɛ̃]", "definition": "Bàn tay", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le pied", "ipa": "[lə pje]", "definition": "Bàn chân", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "Le cœur", "ipa": "[lə kœʁ]", "definition": "Trái tim", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "L'œil", "ipa": "[l‿œj]", "definition": "Mắt", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La bouche", "ipa": "[la buʃ]", "definition": "Miệng", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le nez", "ipa": "[lə ne]", "definition": "Mũi", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "Les oreilles", "ipa": "[le.z‿ɔ.ʁɛl]", "definition": "Tai", "pos": "noun", "gender": "feminine", "number": "plural"},
    {"word": "Le dos", "ipa": "[lə dɔs]", "definition": "Lưng", "pos": "noun", "gender": "masculine", "number": "singular"}
  ],
  [  # Bài 10: Du lịch
    {"word": "L'aéroport", "ipa": "[l‿ɛ.ʁo.pɔʁ]", "definition": "Sân bay", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "Le billet", "ipa": "[lə bijɛ]", "definition": "Vé máy bay", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La valise", "ipa": "[la va.liz]", "definition": "Hành lý", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "La réservation", "ipa": "[la ʁe.zɛʁ.va.sjɔ̃]", "definition": "Đặt phòng/đặt chỗ", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le passeport", "ipa": "[lə pas.pɔʁ]", "definition": "Hộ chiếu", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La carte", "ipa": "[la kaʁt]", "definition": "Bản đồ", "pos": "noun", "gender": "feminine", "number": "singular"},
    {"word": "Le taxi", "ipa": "[lə taksi]", "definition": "Xe taxi", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "L'hôtel", "ipa": "[l‿o.tɛl]", "definition": "Khách sạn", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "Le voyage", "ipa": "[lə vwa.jaʒ]", "definition": "Chuyến du lịch", "pos": "noun", "gender": "masculine", "number": "singular"},
    {"word": "La gare", "ipa": "[la ɡaʁ]", "definition": "Ga tàu", "pos": "noun", "gender": "feminine", "number": "singular"}
  ]]

lesson_topics = [
  "Chào hỏi",
  "Thực phẩm",
  "Giao tiếp",
  "Gia đình",
  "Thời tiết",
  "Số đếm",
  "Màu sắc",
  "Trang phục",
  "Cơ thể",
  "Du lịch"
]

# --- Global variables ---
current_lesson_index = 0
current_word_index = 0

# --- TTS với pyttsx3 (Worker & Queue) ---
engine = pyttsx3.init()
engine.setProperty('rate', 140)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
french_voice = None
for voice in voices:
  try:
    langs = [lang.decode('utf-8') for lang in voice.languages]
  except Exception:
    langs = voice.languages
  if any("fr" in lang.lower() for lang in langs) or "french" in voice.name.lower():
    french_voice = voice.id
    break
if french_voice:
  engine.setProperty('voice', french_voice)

tts_queue = queue.Queue()
def tts_worker():
  while True:
    text = tts_queue.get()
    if text is None:
      break
    engine.say(text)
    engine.runAndWait()
    tts_queue.task_done()
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

# Định nghĩa mapping cho các cụm cần nối âm (ví dụ "bon appétit")
special_liaison = {
  "bon appétit": "bon\u2060appétit",
  
}

# --- Hàm TTS, dead key, ligature ---
def speak_current_word():
  current_entry = lessons[current_lesson_index][current_word_index]
  word_to_speak = current_entry["word"]
  if word_to_speak in special_liaison:
    tts_word = special_liaison[word_to_speak]
  else:
    tts_word = word_to_speak.replace("œ", "oe") #Log Err: chỗ này nếu không thay bằng "oe" thì sẽ bị đọc sai!!!
  tts_queue.put(tts_word)

def on_key_press(event):
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
    if char in accent_map[pending_accent]:
      accented_char = accent_map[pending_accent][char]
      widget.insert(tk.INSERT, accented_char)
      pending_accent = None
      return "break"
    else:
      widget.insert(tk.INSERT, pending_accent)
      pending_accent = None
  if char in accent_map:
    pending_accent = char
    return "break"

def replace_ligature(event):
  widget = event.widget
  text = widget.get()
  if len(text) >= 2:
    if text[-2:] == "oe":
      widget.delete(len(text)-2, tk.END)
      widget.insert(tk.END, "œ")
    elif text[-2:] == "OE":
      widget.delete(len(text)-2, tk.END)
      widget.insert(tk.END, "Œ")

def show_current_word():
  global current_lesson_index, current_word_index
  current_entry = lessons[current_lesson_index][current_word_index]
  word = current_entry["word"]
  ipa = current_entry["ipa"]
  definition = current_entry["definition"]
  pos = current_entry["pos"]
  gender = current_entry["gender"]
  number = current_entry["number"]
  topic_label.config(text=f"Chủ đề: {lesson_topics[current_lesson_index]}")
  word_label.config(text=f"Nhập từ: {word}")
  ipa_label.config(text=f"Phiên âm: {ipa}")
  definition_label.config(text=f"Định nghĩa: {definition}")
  info_label.config(text=f"Từ loại: {pos} | Giống: {gender} | Số: {number}")
  entry.delete(0, tk.END)
  feedback_label.config(text="")
  root.after(500, speak_current_word)

def check_input(event=None):
  global current_lesson_index, current_word_index
  if current_word_index >= len(lessons[current_lesson_index]):
    next_lesson()
    return "break"
  user_input = entry.get()
  current_entry = lessons[current_lesson_index][current_word_index]
  if user_input == current_entry["word"]:
    feedback_label.config(text=f"Bạn đã nhập đúng từ '{current_entry['word']}'!")
    root.after(1000, next_word)
  else:
    feedback_label.config(text="Sai rồi! Bắt đầu lại.")
    entry.delete(0, tk.END)

def next_word():
  global current_word_index, current_lesson_index
  entry.delete(0, tk.END)
  current_word_index += 1
  if current_word_index >= len(lessons[current_lesson_index]):
    word_label.config(text=f"Bạn đã hoàn thành bài {current_lesson_index+1}!")
    ipa_label.config(text="")
    definition_label.config(text="")
    info_label.config(text="")
    feedback_label.config(text="Nhấn Enter hoặc chọn bài mới để luyện tiếp.")
    return
  show_current_word()

def next_lesson():
  global current_lesson_index, current_word_index
  if current_lesson_index < len(lessons) - 1:
    current_lesson_index += 1
    current_word_index = 0
    show_current_word()
  else:
    feedback_label.config(text="Đây là bài cuối cùng.")

def change_lesson(*args):
  global current_lesson_index, current_word_index
  selected = selected_lesson.get()
  try:
    lesson_num = int(selected.split()[1])
    current_lesson_index = lesson_num - 1
    current_word_index = 0
    show_current_word()
  except Exception as e:
    feedback_label.config(text="Lựa chọn bài không hợp lệ.")

# --- Giao diện Tkinter ---
root = tk.Tk()
root.title("French Typing Trainer")
root.geometry("650x550")
root.configure(bg="#f7f7f7")

control_frame = tk.Frame(root, bg="#d0e1f9", bd=2, relief=tk.RIDGE, padx=10, pady=5)
control_frame.pack(fill=tk.X, padx=10, pady=10)
lesson_label = tk.Label(control_frame, text="Chọn bài:", font=("Helvetica", 12, "bold"), bg="#d0e1f9")
lesson_label.pack(side=tk.LEFT, padx=5)
selected_lesson = tk.StringVar(control_frame)
selected_lesson.set("Bài 1")
selected_lesson.trace("w", change_lesson)
option_menu = tk.OptionMenu(control_frame, selected_lesson, *[f"Bài {i+1}" for i in range(len(lessons))])
option_menu.config(font=("Helvetica", 12))
option_menu.pack(side=tk.LEFT, padx=5)
next_lesson_button = tk.Button(control_frame, text="Bài tiếp theo", font=("Helvetica", 12), command=next_lesson, bg="#87CEFA")
next_lesson_button.pack(side=tk.LEFT, padx=5)
speak_button = tk.Button(control_frame, text="Nghe phát âm", font=("Helvetica", 12), command=speak_current_word, bg="#87CEFA")
speak_button.pack(side=tk.LEFT, padx=5)

content_frame = tk.Frame(root, bg="#f7f7f7")
content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
topic_label = tk.Label(content_frame, text="", font=("Helvetica", 16, "italic"), bg="#f7f7f7", anchor="w", justify="left")
topic_label.pack(fill=tk.X, padx=5, pady=2)
word_label = tk.Label(content_frame, text="", font=("Helvetica", 18, "bold"), bg="#f7f7f7", anchor="w", justify="left")
word_label.pack(fill=tk.X, padx=5, pady=5)
ipa_label = tk.Label(content_frame, text="", font=("Helvetica", 14), bg="#f7f7f7", anchor="w", justify="left")
ipa_label.pack(fill=tk.X, padx=5, pady=2)
definition_label = tk.Label(content_frame, text="", font=("Helvetica", 14), bg="#f7f7f7", anchor="w", justify="left")
definition_label.pack(fill=tk.X, padx=5, pady=2)
info_label = tk.Label(content_frame, text="", font=("Helvetica", 14), bg="#f7f7f7", anchor="w", justify="left")
info_label.pack(fill=tk.X, padx=5, pady=2)

entry = tk.Entry(root, font=("Helvetica", 16), width=40)
entry.pack(pady=10)
entry.focus_set()
feedback_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f7f7f7")
feedback_label.pack(pady=5)
entry.bind("<Key>", on_key_press)
entry.bind("<KeyRelease>", replace_ligature)
entry.bind("<Return>", check_input)

show_current_word()
root.mainloop()
