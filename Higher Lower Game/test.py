import tkinter as tk
import random

# Dictionary to store the questions, answers, and images

# This is a question dictionary. It contains the questions, answers, and images for the game.
# In order to change the questions, you can add or remove questions from this dictionary.
# You can also chnage the images by replacing the image files in the same folder as the script.

questions = {
    1: {"question": "Is the height of Mount Kilimanjaro higher or lower than 5,000 meters?", "answer": "higher", "image": "mu.png"},
    2: {"question": "Is the length of the Amazon River higher or lower than 6,400 km?", "answer": "higher", "image": "madrid.png"},
    3: {"question": "Is the population of Brazil higher or lower than 200 million?", "answer": "higher", "image": "mu.png"},
    4: {"question": "Is the number of bones in the human body higher or lower than 200? ", "answer": "lower", "image": "madrid.png"},
    5: {"question": "Is the speed of sound in air higher or lower than 1,100 ft/s?", "answer": "lower", "image": "mu.png"},
    6: {"question": "Is the height of the Burj Khalifa higher or lower than 2,700 feet?", "answer": "higher", "image": "madrid.png"},
    7: {"question": "Is the distance from the Earth to the Moon higher or lower than 238,855 miles?", "answer": "lower", "image": "mu.png"},
    8: {"question": "Is the length of the Great Barrier Reef higher or lower than 1,400 miles?", "answer": "higher", "image": "madrid.png"},
    9: {"question": "Is the population of Russia higher or lower than 144 million? ", "answer": "higher", "image": "mu.png"},
    10: {"question": "Is the length of the Yangtze River higher or lower than 6,300 km?", "answer": "higher", "image": "madrid.png"},
    11: {"question": "Is the height of Mount Denali higher or lower than 20,000 feet?", "answer": "higher", "image": "madrid.png"},
    12: {"question": "Is the speed of a cheetah higher or lower than 60 mph?", "answer": "higher", "image": "mu.png"},
    13: {"question": "Is the population of Australia higher or lower than 25 million?", "answer": "higher", "image": "madrid.png"},
    14: {"question": "Is the number of countries in Europe higher or lower than 50? ", "answer": "lower", "image": "mu.png"},
    15: {"question": "Is the height of the Eiffel Tower higher or lower than 1,000 feet? ", "answer": "lower", "image": "madrid.png"},
    16: {"question": "Is the length of the Congo River higher or lower than 4,000 km? ", "answer": "higher", "image": "madrid.png"},
    17: {"question": "Is the population of South Africa higher or lower than 60 million? ", "answer": "higher", "image": "mu.png"},
    18: {"question": "Is the height of Mount Aconcagua higher or lower than 22,000 feet?", "answer": "higher", "image": "madrid.png"},
    19: {"question": "Is the speed of a hummingbird's wing beat higher or lower than 1,000 beats per minute? ", "answer": "higher", "image": "mu.png"},
    20: {"question": "Is the length of the Yellow River higher or lower than 5,000 km? ", "answer": "higher", "image": "madrid.png"},
}

# Function to start the game
def start_game():
    global current_question
    current_question = random.choice(list(questions.keys()))
    question.config(text=questions[current_question]["question"])
    image = tk.PhotoImage(file=questions[current_question]["image"])
    image_label.config(image=image)
    image_label.image = image

# Function to check the user's guess
def check_guess(guess):
    global questions_left

    # If the user's guess is correct, remove the question from the dictionary
    if guess == questions[current_question]["answer"]:
        result.config(text="Correct! Let's go on to the next question.")
        questions_left -= 1
    else:
        result.config(text="Wrong answer. Game over.")
        higher_button.config(state="disabled")
        lower_button.config(state="disabled")

    if questions_left == 0:
        result.config(text="You've reached the end of the game. Good job!")
        higher_button.config(state="disabled")
        lower_button.config(state="disabled")
    else:
        start_game()

# Create the GUI window
root = tk.Tk()
root.geometry("600x400")
root.title("Higher Lower Game")
root.config(bg="lightblue")

# Create the title label
title = tk.Label(root, text="Higher or Lower?", font=("Arial", 20), bg="lightblue")
title.pack(pady=10)

# Create the question label
question = tk.Label(root, text="", font=("Arial", 16), bg="lightblue")
question.pack(pady=10)

# Create the image label
image_label = tk.Label(root, bg="lightblue")
image_label.pack(pady=10)

# Create the buttons
higher_button = tk.Button(root, text="Higher", font=("Arial", 14), command=lambda: check_guess("higher"), bg="lightblue")
higher_button.pack(pady=10, side="left")

lower_button = tk.Button(root, text="Lower", font=("Arial", 14), command=lambda: check_guess("lower"), bg="lightblue")
lower_button.pack(pady=10, side="right")

result = tk.Label(root, text="", font=("Arial", 16), bg="lightblue")
result.pack(pady=10)

questions_left = 20
start_game()

root.mainloop()

