import os
import tkinter
from tkinter import *
import tkinter.font

from PIL import ImageTk, Image

from ChooseImage import chooseImg
from ChooseSecretImg import chooseSecretImg
from EncodePopup import encodePopup


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

    buttonFrame = Frame(root)
    buttonFrame.pack(expand=True, pady=20)
    buttonFont = tkinter.font.Font(family="Comic Sans MS", size=10, weight="bold")
    chooseImgButton = tkinter.Button(buttonFrame, text='Choose Image', font=buttonFont, relief="flat", width=25, bd=3,
                                      command=lambda: chooseImg(updateChosenImage))
    chooseImgButton.pack(side=LEFT, padx=10)
    changeOnHover(chooseImgButton, "#D3D3D3", root.cget("bg"))

    encodeButton = tkinter.Button(buttonFrame, text='Encode', font=buttonFont, relief="flat", width=25, bd=3, command=lambda: encodePopup(updateEncodingChoice))
    encodeButton.pack(side=LEFT, padx=10)
    changeOnHover(encodeButton, "#D3D3D3", root.cget("bg"))

    decodeButton = tkinter.Button(buttonFrame, text='Decode', font=buttonFont, relief="flat", width=25, bd=3, command=root.destroy)
    decodeButton.pack(side=LEFT, padx=10)
    changeOnHover(decodeButton, "#D3D3D3", root.cget("bg"))

    imgMessage = StringVar(value="No Image Chosen")
    messageVar = Message(root, textvariable=imgMessage)
    messageVar.config(bg='lightyellow', width=200)
    messageVar.place(relx=0.0, rely=0.7, anchor="w")

    imgLabel = Label(root, bg='lightgray')
    imgLabel.place(relx=0.0, rely=0.9, anchor="w")

    def updateChosenImage(filepath):
        imgMessage.set(f"Image Chosen: {os.path.basename(filepath)}")
        img = Image.open(filepath)
        img = img.resize((100, 100))
        imgTk = ImageTk.PhotoImage(img)
        imgLabel.configure(image=imgTk)
        imgLabel.image = imgTk

    def updateEncodingChoice(userChoice):
        if hasattr(root, 'textInputLsb'):
            root.textInputLsb.destroy()
        if hasattr(root, 'textInputDct'):
            root.textInputDct.destroy()
        if hasattr(root, 'secretImgLabel'):
            root.secretImgLabel.destroy()
        if hasattr(root, 'secretImgButton'):
            root.secretImgButton.destroy()
        if hasattr(root, 'secretImgMessage'):
            root.secretImgMessage.destroy()
        if hasattr(root, 'messageVar2'):
            root.messageVar2.destroy()
        if hasattr(root, 'returnButtonLsb'):
            root.returnButtonLsb.destroy()
        if hasattr(root, 'returnButtonDct'):
            root.returnButtonDct.destroy()
        if hasattr(root, 'returnButton4Msb'):
            root.returnButton4Msb.destroy()

        encodingChoice = StringVar(value="")
        encodingChoice.set(f"Encoding method {userChoice}")
        messageVar2 = Message(root, textvariable=encodingChoice)
        messageVar2.config(bg='lightyellow', width=200)
        messageVar2.place(relx=0.3, rely=0.7, anchor="w")
        root.messageVar2 = messageVar2  # Store reference to the message widget

        # LSB (Least Significant Bit) encoding method
        if userChoice == "LSB":
            textInputLsb = Text(root, height=1, width=20)
            textInputLsb.place(relx=0.3, rely=0.8, anchor="w")
            root.textInputLsb = textInputLsb

            returnButtonLsb = Button(root, text="Run", bg="lightgreen")
            returnButtonLsb.place(relx=0.5, rely=0.9, anchor="center")
            root.returnButtonLsb = returnButtonLsb

        # DCT (Discrete Cosine Transform) encoding method
        elif userChoice == "DCT":
            textInputDct = Text(root, height=1, width=20)
            textInputDct.place(relx=0.3, rely=0.8, anchor="w")
            root.textInputDct = textInputDct

            returnButtonDct = Button(root, text="Run", bg="lightgreen")
            returnButtonDct.place(relx=0.5, rely=0.9, anchor="center")
            root.returnButtonDct = returnButtonDct

        # 4MSB (4 Most Significant Bits) encoding method
        elif userChoice == "4MSB":
            secretImgMessage = StringVar(value="")
            secretImgMVar = Message(root, textvariable=secretImgMessage)
            secretImgMVar.config(bg='lightyellow', width=200)
            secretImgMVar.place(relx=0.5, rely=0.7, anchor="w")
            root.secretImgMessage = secretImgMVar

            secretImgLabel = Label(root)
            secretImgLabel.place(relx=0.5, rely=0.9, anchor="w")
            root.secretImgLabel = secretImgLabel

            secretImgButton = Button(root, text="Choose Image", bg="gray", font=buttonFont,
                                     command=lambda: chooseSecretImg(showSecretImg))
            secretImgButton.place(relx=0.4, rely=0.8, anchor="center")
            root.secretImgButton = secretImgButton

            returnButton4Msb = Button(root, text="Run", bg="lightgreen")
            returnButton4Msb.place(relx=0.4, rely=0.9, anchor="center")
            root.returnButton4Msb = returnButton4Msb

            def showSecretImg(filepath):
                secretImgMessage.set(f"Image Chosen: {os.path.basename(filepath)}")
                secretImg = Image.open(filepath)
                secretImg = secretImg.resize((100, 100))
                secretImgTk = ImageTk.PhotoImage(secretImg)
                secretImgLabel.configure(image=secretImgTk)
                secretImgLabel.image = secretImgTk




    root.mainloop()
