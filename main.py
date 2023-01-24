from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
TRANSPARENT = "#e60ed4"
FONT = ("Arial", 60, "bold")
WORD_FONT = ("Arial", 40, "italic")
GLOSS_FONT = ("Arial", 60, "bold")


def flip(event):
    front_label.grid_remove()
    word_label.grid()
    gloss_label.grid()

    incorrect_button.config(state=NORMAL)
    correct_button.config(state=NORMAL)


def reset():
    front_label.grid()
    word_label.grid_remove()
    gloss_label.grid_remove()

    incorrect_button.config(state=DISABLED)
    correct_button.config(state=DISABLED)


def correct():
    print("Correct button clicked")
    # TODO: implemented feature

    next_card()


def incorrect():
    print("Incorrect button clicked")
    # TODO: implemented feature

    next_card()


def next_card():
    # TODO: get next word and set labels

    reset()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.resizable(False, False)
window.bind("<KeyRelease>", flip)

# card image
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = PhotoImage(file="images/card_front.png")
canvas.create_image(400, 263, image=card_image)

# labels
front_label = Label(text="Word", bg='white', font=FONT)
word_label = Label(text="Word", bg='white', font=WORD_FONT)
gloss_label = Label(text="Gloss", bg='white', font=FONT)
front_label.bind('<ButtonRelease-1>', flip)

# buttons
wrong_image = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=wrong_image, bg=BACKGROUND_COLOR, highlightthickness=0,
                          borderwidth=0, command=incorrect, state=DISABLED)

correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, bg=BACKGROUND_COLOR, highlightthickness=0,
                        borderwidth=0, command=correct, state=DISABLED)

# grid placements
canvas.grid(column=0, row=0, columnspan=2, rowspan=2)
front_label.grid(column=0, row=0, columnspan=2, rowspan=2)
word_label.grid(column=0, row=0, columnspan=2, sticky=N)
gloss_label.grid(column=0, row=1, columnspan=2, sticky=N)
word_label.grid_remove()
gloss_label.grid_remove()
correct_button.grid(column=1, row=2)
incorrect_button.grid(column=0, row=2)

window.mainloop()
