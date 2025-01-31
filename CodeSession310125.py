word_list = ["hello", "world", "python", "programming", "keyboard", "practice", "typing", "challenge"]

word = "Tran"

c_word = 0
c_typing = 0

typing = input("Nhap vao day:     ")
list_word = list(word)
print(    'split word:   '   +   str(list_word))
list_typing = list(typing)

limit = len(list_word)
print ( '   count of chars:   '   + str( limit ))


# Initialize index for character comparison
index = 0




while True:
    # Get user input for typing
    list_typing = input("Enter your typing (e.g., 'Tran'): ").strip()  # Read user input and strip whitespace
    
    # Check if the input length matches the word length
    if len(list_typing) != len(list_word):
        print("Input length does not match the expected word length. Please try again.")
        continue  # Ask for input again

    # Initialize index for character comparison
    index = 0
    c_word = 0  # Reset correct word counter for each new attempt
    c_typing = 0  # Reset typing counter for each new attempt

    while index < len(list_word):
        char_word = list_word[index]
        char_type = list_typing[index]

        print(f"Index: {index}, Word Char: {char_word}, Typing Char: {char_type}")

        if char_word == char_type:
            print(f'Correct: {char_word}')
            c_word += 1
            c_typing += 1
            
            # Check if typing limit is reached
            if c_typing == limit:
                print("Limit reached. Proceeding to next word.")
                break  # Exit loop or handle next word logic here

        else:
            print("Wrong")
            # Reset counters and ask for new input
            print("Please try typing the word again.")
            break  # Break to restart the outer loop to get new input

        # Move to the next character
        index += 1

    # Final output of counters (if needed)
    print(f"Final correct characters: {c_word}, Total characters typed: {len(list_typing)}")