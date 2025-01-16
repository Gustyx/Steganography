import tkinter

import customtkinter
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
import os
import shutil
import random
import string
from tkinter import messagebox
import tkinter.font


def chooseImg(updateChosenImageCallback):
    extra_window = tkinter.Toplevel()

    app = extra_window
    app.title("Upload Image")
    app.geometry("480x380")

    frame = customtkinter.CTkLabel(app, text="")
    frame.grid(row=0, column=0, sticky="w", padx=50, pady=20)

    def setPreviewPic(filepath):
        global img
        img = Image.open(filepath)
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)
        lbl_show_pic = tk.Label(frame, bg='#52494a', image=img)
        lbl_show_pic.grid(row=1, column=0, columnspan=3, pady=5, ipady=0, sticky="nswe")
        pathEntry.insert(0, filepath)

    def selectPic():
        global filename
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select Image",
            filetypes=[("images files", "*.png *.jpg *.jpeg"), ]
        )
        setPreviewPic(filename)

    def savePic():
        savedPath = f"./Images/{os.path.basename(filename)}"
        os.makedirs("./Images", exist_ok=True)
        shutil.copy(filename, savedPath)
        updateChosenImageCallback(savedPath)
        messagebox.showinfo("Success", "Uploaded Successfully")
        extra_window.destroy()


    selectBtn = customtkinter.CTkButton(frame, text="Browse Image", width=50, command=selectPic, fg_color="#52494a",
                                        hover_color="#211b1b",
                                        text_color="white")
    pathEntry = customtkinter.CTkEntry(frame, width=200)
    saveBtn = customtkinter.CTkButton(frame, text="Upload", width=50, command=savePic, fg_color="#52494a",
                                      hover_color="#211b1b",
                                      text_color="white")
    lbl_show_pic = tk.Label(frame, bg='#52494a')

    setPreviewPic("./Images/default.png")

    selectBtn.grid(row=0, column=0, padx=1, pady=5, ipady=0, sticky="e")
    pathEntry.grid(row=0, column=1, padx=1, pady=5, ipady=0, sticky="e")
    saveBtn.grid(row=0, column=2, padx=1, pady=5, ipady=0, sticky="e")
    lbl_show_pic.grid(row=1, column=0, columnspan=3, pady=5, ipady=0, sticky="nswe")


    app.resizable(False, False)
    app.mainloop()

