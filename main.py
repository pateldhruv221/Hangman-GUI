
from tkinter import *
from PIL import Image, ImageTk
from random import randint

# "root"/main window of game
root = Tk()
root.title("Hangman")
root.configure(background="white")
root.state("zoomed") # open app maximized
# root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# DETERMINING LENGTH OF FILE
num_words = 0
with open("words_file.txt", "r") as words_file:
    for word in words_file:
        num_words += 1

# EXTRACTING A RANDOM WORD FROM THE FILE
answer = ""
rand_index = randint(0, num_words-1)
with open("words_file.txt", "r") as words_file:
    for i, word in enumerate(words_file):
        if i == rand_index:
            answer = word.strip() #removing new-line character at the end
            break

# NECESSARY VARIABLES AND FUNCTIONS
user_progress = "_"*len(answer)
user_guess = ''
wrong_guesses_left = 7
wrong_letters_guessed = []
right_answer_indices = []
is_game_over = False

# creating all frames and labels
main_frame = Frame(root)
title_label = Label(main_frame,text="HANGMAN",font=("Gothic", 36),bg="white")
body_frame = Frame(main_frame)
user_progress_frame = Frame(body_frame)
intro_label = Label(user_progress_frame,text=f"You have to guess a {len(answer)}-letter word")
guesses_left_label = Label(user_progress_frame,text=f"You have {wrong_guesses_left} guesses left!")
wrong_letters_label = Label(user_progress_frame,text=f"Wrong letters guessed: {wrong_letters_guessed}")
input_frame = Frame(user_progress_frame)
output_message = Label(input_frame)
input_entry = Entry(input_frame)
image_word_frame = Frame(body_frame,bg="white")

hangman_image = Image.open("./pics/pic1.png")
hangman_image = hangman_image.resize((364,412),Image.ANTIALIAS) # set to 68%, 100% = 536x607
temp_img = ImageTk.PhotoImage(hangman_image)
hangman_image_label = Label(image_word_frame,image=temp_img,borderwidth=0,highlightthickness=0,bg="white")

def show_hangman():
    global wrong_guesses_left
    new_image = Image.open(f"./pics/pic{8-wrong_guesses_left}.png")
    new_image = ImageTk.PhotoImage(new_image.resize((364,412),Image.ANTIALIAS))
    hangman_image_label.configure(image=new_image)
    hangman_image_label.image = new_image


def display_user_progress():
    to_return = ""
    for letter in user_progress:
        to_return += " {} ".format(letter)
    return to_return

word_label = Label(image_word_frame,text=f"{display_user_progress()}",bg="white")

def check_input():
    # allows access to global variables
    global user_progress
    global user_guess
    global wrong_guesses_left
    global wrong_letters_guessed
    global right_answer_indices
    global is_game_over

    if not is_game_over:
        user_guess = input_entry.get().lower()
        if len(user_guess) != 1 or user_guess not in "abcdefghijklmnopqrstuvwxyz":
            #fg = foreground = text colour
            output_message.configure(text="Wrong input type. Try again.",fg="red")
        else:
            output_message.configure(text="")
            # Evaluate user guess
            if user_guess in answer:
                #Check to see if user has guessed this right letter before or not
                if user_guess in user_progress:
                    output_message.configure(text="Right answer already guessed. Try again.",fg="red")
                else:
                    output_message.configure(text="RIGHT GUESS!", fg="green")
                    # Find our where in the answer the letter is
                    for i, letter in enumerate(answer):
                        if letter == user_guess:
                            right_answer_indices.append(i)
                    # Replace the appropriate places in the user progress
                    for i in right_answer_indices:
                        user_progress = user_progress[:i] + user_guess + user_progress[i+1:]
                        if user_progress == answer:
                            word_label.configure(text=f"{display_user_progress()}\nYOU WON!",fg="green")
                            output_message.configure(text="GAME OVER!",fg="green")
                            is_game_over = True
                        else:
                            word_label.configure(text=f"{display_user_progress()}")

            else:
                #Check to see if user has guessed this wrong letter before or not
                if user_guess in wrong_letters_guessed:
                    output_message.configure(text="Wrong letter already guessed. Try again.",fg="red")
                else:
                    output_message.configure(text="WRONG GUESS!",fg="red")
                    wrong_letters_guessed.append(user_guess)
                    wrong_guesses_left -= 1
                    wrong_letters_label.configure(text=f"Wrong letters guessed: {wrong_letters_guessed}")
                    guesses_left_label.configure(text=f"You have {wrong_guesses_left} guesses left!")
                    if wrong_guesses_left == 0:
                        user_progress = answer
                        word_label.configure(text=f"You lost :( Correct answer: {display_user_progress()}",fg="red")
                        output_message.configure(text="GAME OVER!",fg="red")
                        is_game_over = True
                    show_hangman()


        right_answer_indices = []

input_button = Button(input_frame,text="Enter a letter",command=check_input)

# place all frames and labels
main_frame.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)
title_label.place(relx=0,rely=0,relwidth=1,relheight=0.1)
body_frame.place(relx=0,rely=0.1,relwidth=1,relheight=0.9)
user_progress_frame.place(relx=0,rely=0,relwidth=0.4,relheight=1)
intro_label.place(relx=0,rely=0,relwidth=1,relheight=0.25)
guesses_left_label.place(relx=0,rely=0.25,relwidth=1,relheight=0.25)
wrong_letters_label.place(relx=0,rely=0.5,relwidth=1,relheight=0.25)
input_frame.place(relx=0,rely=0.75,relwidth=1,relheight=0.25)
input_button.place(relx=0,rely=0.4,relwidth=0.5,relheight=0.2)
output_message.place(relx=0,rely=0.6,relwidth=0.5,relheight=0.2)
input_entry.place(relx=0.5,rely=0.4,relwidth=0.5,relheight=0.2)
image_word_frame.place(relx=0.4,rely=0,relwidth=0.6,relheight=1)
hangman_image_label.place(relx=0,rely=0,relwidth=1,relheight=0.8)
word_label.place(relx=0,rely=0.8,relwidth=1,relheight=0.2)

def run_game():
    root.mainloop()

run_game()
