word_list = ["hello", "world", "python", "programming", "keyboard", "practice", "typing", "challenge"]

# Iterate through each word in the word list
for word in word_list:
    while True:  # Loop until correct input is received
        # Prompt user for input
        user_input = input(f"Type the word '{word}': ").strip()  # Read user input and strip whitespace
        
        # Check if the input matches the current word
        if user_input == word:
            print("Correct! Moving to the next word.")
            break  # Exit the inner loop to proceed to the next word
        else:
            print("Incorrect. Please try again.")  # Prompt for correct input again

# Final message after all words have been typed correctly
print("Congratulations! You've completed all words.")