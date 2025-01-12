from tkinter import *


def encodePopup(updateEncodingChoice):
    dialog = Toplevel()
    dialog.title("Encode")
    dialog.geometry("300x200")
    dialog.resizable(False, False)
    dialog.transient()
    dialog.grab_set()

    messageLabel = Label(dialog, text="Choose a way to encode", font=("Comic Sans MS", 12, "bold"))
    messageLabel.pack(pady=20)

    def selectOption(option):
        global user_choice
        user_choice = option  # Store the user's choice
        updateEncodingChoice(user_choice)
        dialog.destroy()

    btnOption1 = Button(dialog, text="LSB", width=10, command=lambda: selectOption("LSB"))
    btnOption2 = Button(dialog, text="DCT", width=10, command=lambda: selectOption("DCT"))
    btnOption3 = Button(dialog, text="4MSB", width=10, command=lambda: selectOption("4MSB"))

    btnOption1.pack(pady=5)
    btnOption2.pack(pady=5)
    btnOption3.pack(pady=5)
