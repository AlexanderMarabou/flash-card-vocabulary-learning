from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
flip_timer = None

# ---------------------------- LOAD FILES ------------------------------- #
try:
    # Loads lists of words yet to learn and already acquired
    words_to_learn = pd.read_csv("data/words_to_learn.csv")
    words_acquired = pd.read_csv("data/words_acquired.csv")

except FileNotFoundError:
    # Loads initial list of words and create a copy
    words_list = pd.read_csv("data/french_words.csv")
    words_to_learn = words_list.copy(deep=True)

    # Loads the copy of list of words and creates a dictionary
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    words_to_learn_dictionary = words_list.to_dict(orient='records')

    # Creates an empty file to save acquired words
    words_acquired = pd.DataFrame(columns=[words_to_learn.columns[0], words_to_learn.columns[1]])
    words_acquired.to_csv("data/words_acquired.csv", index=False)

else:
    # Creates a dictionary from words to learn for further use
    words_to_learn_dictionary = words_to_learn.to_dict(orient='records')

# Defines the names of the columns to use in a dictionary
target_language = words_to_learn.columns[0]
native_language = words_to_learn.columns[1]


# ---------------------------- GENERATE NEW WORD ------------------------------- #


def next_card():
    global current_card, flip_timer, words_to_learn_dictionary
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn_dictionary)
    update_card(target_language, current_card[target_language], card_front_image, "black")
    flip_timer = window.after(3000, func=show_solution)


# ---------------------------- SAVE PROGRESS ------------------------------- #

def known_word():
    # Appends the current card to words_acquired.csv
    pd.DataFrame.from_records([current_card]).to_csv("data/words_acquired.csv",
                                                     mode="a", index=False, header=False)

    # Removes a current card from words_to_learn
    words_to_learn_dictionary.remove(current_card)
    pd.DataFrame(words_to_learn_dictionary).to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- DISPLAY SOLUTION ------------------------------- #

def show_solution():
    # Displays card with a solution
    update_card(native_language, current_card[native_language], card_back_image, "white")


def update_card(title, word, image, text_color):
    canvas.itemconfig(card_title, text=title, fill=text_color)
    canvas.itemconfig(card_word, text=word, fill=text_color)
    canvas.itemconfig(canvas_image, image=image)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=show_solution)

canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, fill="black", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, fill="black", font=("Ariel", 60, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
cross_button_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_button_image, highlightbackground=BACKGROUND_COLOR, highlightthickness=0,
                        command=next_card)
unknown_button.grid(column=0, row=1)

check_button_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_button_image, highlightbackground=BACKGROUND_COLOR, highlightthickness=0,
                      command=known_word)
known_button.grid(column=1, row=1)

next_card()


window.mainloop()
