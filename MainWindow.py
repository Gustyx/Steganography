import tkinter
from tkinter import *
import tkinter.font
from ChooseImage import chooseImg

def showOptionDialog():
    dialog = Toplevel()
    dialog.title("Choose an Option")
    dialog.geometry("300x200")
    dialog.resizable(False, False)
    dialog.transient()
    dialog.grab_set()

    messageLabel = Label(dialog, text="What do you choose?", font=("Comic Sans MS", 12, "bold"))
    messageLabel.pack(pady=20)

    def option1():
        dialog.destroy()

    def option2():
        dialog.destroy()

    def option3():
        dialog.destroy()

    btnOption1 = Button(dialog, text="Option 1", width=10, command=option1)
    btnOption2 = Button(dialog, text="Option 2", width=10, command=option2)
    btnOption3 = Button(dialog, text="Option 3", width=10, command=option3)

    btnOption1.pack(pady=5)
    btnOption2.pack(pady=5)
    btnOption3.pack(pady=5)


def changeOnHover(button, colorOnHover, colorOnLeave):
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover, relief="raised"))

    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave, relief="flat"))


def mainWindow():
    root = tkinter.Tk()
    root.title("Image Steganography")
    root.geometry("700x400+500+200")

    pageTitle = Label(root, text="Let's test Image Steganography!")
    pageTitle.pack()
    desiredFont = tkinter.font.Font(family="Comic Sans MS",
                                    size=20,
                                    weight="bold")
    pageTitle.configure(font=desiredFont)

    buttonFont = tkinter.font.Font(family="Comic Sans MS", size=10, weight="bold")
    chooseImgButton = tkinter.Button(root, text='Choose Image', font=buttonFont, relief="flat", width=25, command=chooseImg)
    chooseImgButton.pack(side=LEFT, padx=20, pady=20)
    changeOnHover(chooseImgButton, "#D3D3D3", root.cget("bg"))

    encodeButton = tkinter.Button(root, text='Encode', font=buttonFont, relief="flat", width=25, command=showOptionDialog)
    encodeButton.pack(side=LEFT, padx=20, pady=20)
    changeOnHover(encodeButton, "#D3D3D3", root.cget("bg"))

    decodeButton = tkinter.Button(root, text='Decode', font=buttonFont, relief="flat", width=25, command=root.destroy)
    decodeButton.pack(side=LEFT, padx=20, pady=20)
    changeOnHover(decodeButton, "#D3D3D3", root.cget("bg"))

    root.mainloop()
