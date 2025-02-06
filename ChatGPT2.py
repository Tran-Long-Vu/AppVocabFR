import readchar

def typing_trainer():
    word_lists = [
        ["good", "apple", "happy", "smile", "world"],
        ["train", "great", "smart", "lucky", "tiger"],
        ["honest", "strong", "future", "brave", "quick"]
    ]
    
    for word_list in word_lists:
        print("\nBắt đầu danh sách từ mới!\n")
        for word in word_list:
            print(f"Nhập từ: {word}") #print(f"Nhập từ: {word}", end='\r')
            index = 0
            typed = list(" " * len(word))
            
            while index < len(word):
                char = readchar.readchar()
                if char == word[index]:
                    typed[index] = char
                    index += 1
                    print(f"Nhập từ: {word[:index] + ' ' * (len(word) - index)}", end='\r')
                else:
                    print("Sai rồi! Bắt đầu lại.") #print("Sai rồi! Bắt đầu lại.", end='\r')
                    typed = list(" " * len(word))
                    index = 0
                    print(f"Nhập từ: {word}", end='\r')
            print(f"Bạn đã nhập đúng từ '{word}'!\n")
    
    print("\nChúc mừng! Bạn đã hoàn thành tất cả các danh sách từ!")

if __name__ == "__main__":
    typing_trainer()