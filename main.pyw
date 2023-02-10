from tkinter import *
from tkinter import filedialog
from idlelib.tooltip import Hovertip
import pandas


def get_last_studied():
    try:
        with open("data/last_studied_list.txt") as last_studied:
            return last_studied.read()
    except FileNotFoundError:
        return ""


FRONT_BG_COLOR = "#B1DDC6"
BACK_BG_COLOR = "#91C2AF"
TRANSPARENT = "#e60ed4"
FONT = ("Arial", 60, "bold")
WORD_FONT = ("Arial", 40, "italic")
GLOSS_FONT = ("Arial", 60, "bold")

data_path = get_last_studied()
original_data = pandas.DataFrame(columns=["Word Language", "Gloss Language"])
word_language = "Word language"
gloss_language = "Gloss language"
known_words = pandas.DataFrame(columns=[word_language, gloss_language])
current_word = None
word_language_tooltip = None
gloss_language_tooltip = None


def load_words(path):
    global original_data, word_language, gloss_language, known_words, word_language_tooltip, gloss_language_tooltip

    try:
        original_data = pandas.read_csv(path)
        word_language = original_data.columns[0]
        gloss_language = original_data.columns[1]
        word_language_tooltip = Hovertip(front_label, word_language)
        gloss_language_tooltip = Hovertip(gloss_label, gloss_language)
    except FileNotFoundError:
        return

    with open("data/last_studied_list.txt", mode="w") as file:
        file.write(path)

    # load progress
    try:
        known_words = pandas.read_csv(f"data/known_words/known_{word_language}_words.csv")
    except FileNotFoundError:
        known_words = pandas.DataFrame(columns=[word_language, gloss_language])

    start()
    next_card()


def open_file():
    filename = filedialog.askopenfilename(filetypes=[("Comma Separated Values", ".csv")])
    load_words(filename)


def get_random_word():
    return original_data.sample()


def enable_buttons():
    incorrect_button.config(state=NORMAL)
    correct_button.config(state=NORMAL)


def disable_buttons():
    incorrect_button.config(state=DISABLED)
    correct_button.config(state=DISABLED)


def listener(event):
    if incorrect_button['state'] == 'disabled':
        flip_to_back()
    else:
        if event.keysym == "Up":
            correct()
        elif event.keysym == "Down":
            incorrect()


def flip_to_back():
    front_label.grid_remove()
    word_label.grid()
    gloss_label.grid()
    canvas.itemconfig(card_background, image=back_image)

    enable_buttons()


def flip_to_front():
    front_label.grid()
    word_label.grid_remove()
    gloss_label.grid_remove()
    canvas.itemconfig(card_background, image=front_image)


def is_deck_empty():
    return len(known_words) == len(original_data)


def stop():
    flip_to_back()
    disable_buttons()
    window.unbind('<KeyRelease>')
    front_label.unbind('<ButtonRelease-1>')
    word_label.config(text="Congratulations!")
    gloss_label.config(text="You've finished\nthis set!")


def start():
    # enable binding and flip to front of card
    window.bind('<KeyRelease>', listener)
    front_label.bind('<ButtonRelease-1>', listener)
    flip_to_front()


def correct():
    global known_words, current_word
    known_words = pandas.concat([known_words, current_word], ignore_index=True)
    save_progress()
    next_card()


def incorrect():
    next_card()


def next_card():
    global known_words, current_word

    if is_deck_empty():
        stop()
    else:
        current_word = get_random_word()
        while current_word[word_language].isin(known_words[word_language]).bool():
            current_word = get_random_word()
        front_label.config(text=current_word.iloc[0][word_language])
        word_label.config(text=current_word.iloc[0][word_language])
        gloss_label.config(text=current_word.iloc[0][gloss_language])

        flip_to_front()

        disable_buttons()


def save_progress():
    known_words.to_csv(f"data/known_words/known_{word_language}_words.csv", index=False)


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=FRONT_BG_COLOR)
window.resizable(False, False)

# load button
icon_image = PhotoImage(file="images/load_icon.png")
load_button = Button(image=icon_image, bg=FRONT_BG_COLOR, highlightthickness=0,
                     borderwidth=0, command=open_file)

# card image
canvas = Canvas(width=800, height=526, bg=FRONT_BG_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_image)

# labels
front_label = Label(text="No words loaded", bg='white', font=FONT, )
word_label = Label(fg='white', bg=BACK_BG_COLOR, font=WORD_FONT)
gloss_label = Label(fg='white', bg=BACK_BG_COLOR, font=GLOSS_FONT)

# buttons
wrong_image = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=wrong_image, bg=FRONT_BG_COLOR, highlightthickness=0,
                          borderwidth=0, command=incorrect)

correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, bg=FRONT_BG_COLOR, highlightthickness=0,
                        borderwidth=0, command=correct)
disable_buttons()

# grid placements
load_button.grid(column=2, row=0, sticky=NE)
canvas.grid(column=0, row=0, columnspan=2, rowspan=2)
front_label.grid(column=0, row=0, columnspan=2, rowspan=2)
word_label.grid(column=0, row=0, columnspan=2)
gloss_label.grid(column=0, row=1, columnspan=2, sticky=N)
word_label.grid_remove()
gloss_label.grid_remove()
correct_button.grid(column=1, row=2)
incorrect_button.grid(column=0, row=2)
load_tooltip = Hovertip(load_button, "Load word list")
start()

load_words(data_path)

window.mainloop()
