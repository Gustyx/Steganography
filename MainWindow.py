import os
import tkinter
from tkinter import *
import tkinter.font
from tkinter import messagebox

import cv2
from PIL import ImageTk, Image

import BlueChannel
from ChooseImage import chooseImg
from ChooseSecretImg import chooseSecretImg
from DCT import embed_message_dct_color, embed_message_dct_grayscale
from EncodePopup import encodePopup
from ImgStegano1 import encrypt
from LSB import embed_data
from DecodePopup import decodePopup
from imageManipulator import compute_difference


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

    decodeButton = tkinter.Button(buttonFrame, text='Decode', font=buttonFont, relief="flat", width=25, bd=3,
                                  command=lambda: decodePopup(getattr(root, 'chosenImagePath', None)))
    decodeButton.pack(side=LEFT, padx=10)
    changeOnHover(decodeButton, "#D3D3D3", root.cget("bg"))

    imgMessage = StringVar(value="No Image Chosen")
    messageVar = Message(root, textvariable=imgMessage)
    messageVar.config(bg='lightyellow', width=200)
    messageVar.place(relx=0.0, rely=0.7, anchor="w")

    imgLabel = Label(root, bg='lightgray')
    imgLabel.place(relx=0.0, rely=0.9, anchor="w")

    def updateChosenImage(filepath):
        root.chosenImagePath = filepath
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
        if hasattr(root, 'textInputDctGr'):
            root.textInputDctGr.destroy()
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
        if hasattr(root, 'returnButtonDctGr'):
            root.returnButtonDctGr.destroy()

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

            def handle_lsb_run():
                user_input = textInputLsb.get("1.0", "end-1c").strip()
                if not user_input or not hasattr(root, 'chosenImagePath'):
                    tkinter.messagebox.showerror("Error", "Please provide valid input text and choose an image.")
                    return

                image_path = root.chosenImagePath
                image = cv2.imread(image_path)
                stego_image = embed_data(image.copy(), user_input)

                stego_folder = "Images/stego"
                if not os.path.exists(stego_folder):
                    os.makedirs(stego_folder)

                original_filename, original_extension = os.path.splitext(os.path.basename(image_path))
                stego_filename = f"stego_lsb_{original_filename}{original_extension}"
                stego_image_path = os.path.join(stego_folder, stego_filename)

                cv2.imwrite(stego_image_path, stego_image)

                popup = Toplevel(root)
                popup.title("Original and Stego Images")
                popup.geometry("600x400")  # Adjust the size as needed

                # Labels for the images
                original_label = Label(popup, text="Original Image")
                original_label.grid(row=0, column=0, padx=10, pady=10)

                stego_label = Label(popup, text="Stego Image")
                stego_label.grid(row=0, column=1, padx=10, pady=10)

                # Display the original image
                original_img = Image.open(image_path)
                original_img = original_img.resize((250, 250))
                original_img_tk = ImageTk.PhotoImage(original_img)

                original_img_label = Label(popup, image=original_img_tk)
                original_img_label.image = original_img_tk  # Prevent garbage collection
                original_img_label.grid(row=1, column=0, padx=10, pady=10)

                # Display the stego image
                stego_img = Image.open(stego_image_path)
                stego_img = stego_img.resize((250, 250))
                stego_img_tk = ImageTk.PhotoImage(stego_img)

                stego_img_label = Label(popup, image=stego_img_tk)
                stego_img_label.image = stego_img_tk  # Prevent garbage collection
                stego_img_label.grid(row=1, column=1, padx=10, pady=10)

                difference_button = Button(popup, text="Difference", command=lambda: compute_difference(image,stego_image))
                difference_button.grid(row=2, column=0, columnspan=2, pady=10)


                close_button = Button(popup, text="Close", command=popup.destroy)
                close_button.grid(row=3, column=0, columnspan=2, pady=10)

            returnButtonLsb = Button(root, text="Run", bg="lightgreen", command=handle_lsb_run)
            returnButtonLsb.place(relx=0.5, rely=0.9, anchor="center")
            root.returnButtonLsb = returnButtonLsb

        # DCT (Discrete Cosine Transform) encoding method
        elif userChoice == "DCT":
            textInputDct = Text(root, height=1, width=20)
            textInputDct.place(relx=0.3, rely=0.8, anchor="w")
            root.textInputDct = textInputDct
            def handle_dct_run():
                user_input = textInputDct.get("1.0", "end-1c").strip()
                if not user_input or not hasattr(root, 'chosenImagePath'):
                    tkinter.messagebox.showerror("Error", "Please provide valid input text and choose an image.")
                    return

                image_path = root.chosenImagePath
                image = cv2.imread(image_path)
                stego_image = embed_message_dct_color(image.copy(), user_input)

                stego_folder = "Images/stego"
                if not os.path.exists(stego_folder):
                    os.makedirs(stego_folder)

                original_filename, original_extension = os.path.splitext(os.path.basename(image_path))
                stego_filename = f"stego_dct_{original_filename}{original_extension}"
                stego_image_path = os.path.join(stego_folder, stego_filename)

                cv2.imwrite(stego_image_path, stego_image)

                popup = Toplevel(root)
                popup.title("Original and Stego Images")
                popup.geometry("600x400")

                original_label = Label(popup, text="Original Image")
                original_label.grid(row=0, column=0, padx=10, pady=10)

                stego_label = Label(popup, text="Stego Image")
                stego_label.grid(row=0, column=1, padx=10, pady=10)

                original_img = Image.open(image_path)
                original_img = original_img.resize((250, 250))
                original_img_tk = ImageTk.PhotoImage(original_img)

                original_img_label = Label(popup, image=original_img_tk)
                original_img_label.image = original_img_tk
                original_img_label.grid(row=1, column=0, padx=10, pady=10)

                # Display the stego image
                stego_img = Image.open(stego_image_path)
                stego_img = stego_img.resize((250, 250))
                stego_img_tk = ImageTk.PhotoImage(stego_img)

                stego_img_label = Label(popup, image=stego_img_tk)
                stego_img_label.image = stego_img_tk
                stego_img_label.grid(row=1, column=1, padx=10, pady=10)

                difference_button = Button(popup, text="Difference",
                                           command=lambda: compute_difference(image, stego_image))
                difference_button.grid(row=2, column=0, columnspan=2, pady=10)

                close_button = Button(popup, text="Close", command=popup.destroy)
                close_button.grid(row=3, column=0, columnspan=2, pady=10)

            returnButtonDct = Button(root, text="Run", bg="lightgreen", command=handle_dct_run)
            returnButtonDct.place(relx=0.5, rely=0.9, anchor="center")
            root.returnButtonDct = returnButtonDct

        elif userChoice == "DCT GRAY":
            textInputDctGr = Text(root, height=1, width=20)
            textInputDctGr.place(relx=0.3, rely=0.8, anchor="w")
            root.textInputDctGr = textInputDctGr
            def handle_dctGr_run():
                user_input = textInputDctGr.get("1.0", "end-1c").strip()
                if not user_input or not hasattr(root, 'chosenImagePath'):
                    tkinter.messagebox.showerror("Error", "Please provide valid input text and choose an image.")
                    return

                image_path = root.chosenImagePath
                image = cv2.imread(image_path)  # Load as grayscale
                if image is None:
                    tkinter.messagebox.showerror("Error", "Failed to load image. Please check the file path.")
                    return

                # Embed the message into the grayscale image
                stego_image = embed_message_dct_grayscale(image.copy(), user_input)

                # Save the stego image
                stego_folder = "Images/stego"
                if not os.path.exists(stego_folder):
                    os.makedirs(stego_folder)

                original_filename, original_extension = os.path.splitext(os.path.basename(image_path))
                stego_filename = f"stego_dctgr_{original_filename}{original_extension}"
                stego_image_path = os.path.join(stego_folder, stego_filename)

                try:
                    cv2.imwrite(stego_image_path, stego_image)
                except Exception as e:
                    tkinter.messagebox.showerror("Error", f"Failed to save stego image: {e}")
                    return

                # Display the original and stego images in a popup
                popup = Toplevel(root)
                popup.title("Original and Stego Images")
                popup.geometry("600x400")

                original_label = Label(popup, text="Original Image")
                original_label.grid(row=0, column=0, padx=10, pady=10)

                stego_label = Label(popup, text="Stego Image")
                stego_label.grid(row=0, column=1, padx=10, pady=10)

                # Display the original image
                original_img = Image.open(image_path)
                original_img = original_img.resize((250, 250))
                original_img_tk = ImageTk.PhotoImage(original_img)

                original_img_label = Label(popup, image=original_img_tk)
                original_img_label.image = original_img_tk
                original_img_label.grid(row=1, column=0, padx=10, pady=10)

                # Display the stego image
                stego_img = Image.fromarray(stego_image)
                stego_img = stego_img.resize((250, 250))
                stego_img_tk = ImageTk.PhotoImage(stego_img)

                stego_img_label = Label(popup, image=stego_img_tk)
                stego_img_label.image = stego_img_tk
                stego_img_label.grid(row=1, column=1, padx=10, pady=10)

                # Close button
                close_button = Button(popup, text="Close", command=popup.destroy)
                close_button.grid(row=2, column=0, columnspan=2, pady=10)

            returnButtonDctGr = Button(root, text="Run", bg="lightgreen", command=handle_dctGr_run)
            returnButtonDctGr.place(relx=0.5, rely=0.9, anchor="center")
            root.returnButtonDctGr = returnButtonDctGr

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

            returnButton4Msb = Button(root, text="Run", bg="lightgreen", command=lambda: handle_4msb_run())
            returnButton4Msb.place(relx=0.4, rely=0.9, anchor="center")
            root.returnButton4Msb = returnButton4Msb

            def handle_4msb_run():
                # Ensure both images are chosen
                if not hasattr(root, 'chosenImagePath') or not hasattr(root, 'secretImagePath'):
                    tkinter.messagebox.showerror("Error", "Please choose both the cover image and the secret image.")
                    return

                # Load the chosen and secret images
                image1_path = root.chosenImagePath
                image2_path = root.secretImagePath

                image1 = cv2.imread(image1_path)
                image2 = cv2.imread(image2_path)

                if image1 is None or image2 is None:
                    tkinter.messagebox.showerror("Error", "Failed to load images. Please ensure valid image paths.")
                    return

                # Resize secret image to match the cover image size
                # image2_resized = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

                # Encrypt the secret image into the cover image
                stego_image = encrypt(image1.copy(), image2.copy())

                # Save the stego image
                stego_folder = "Images/stego"
                if not os.path.exists(stego_folder):
                    os.makedirs(stego_folder)

                original_filename, original_extension = os.path.splitext(os.path.basename(image1_path))
                stego_filename = f"stego_4msb_{original_filename}{original_extension}"
                stego_image_path = os.path.join(stego_folder, stego_filename)

                cv2.imwrite(stego_image_path, stego_image)

                # Display the original and stego images in a popup
                popup = Toplevel(root)
                popup.title("Original and Stego Images (4MSB)")
                popup.geometry("600x400")

                original_label = Label(popup, text="Original Image")
                original_label.grid(row=0, column=0, padx=10, pady=10)

                stego_label = Label(popup, text="Stego Image")
                stego_label.grid(row=0, column=1, padx=10, pady=10)

                # Display the original image
                original_img = Image.open(image1_path)
                original_img = original_img.resize((250, 250))
                original_img_tk = ImageTk.PhotoImage(original_img)

                original_img_label = Label(popup, image=original_img_tk)
                original_img_label.image = original_img_tk  # Prevent garbage collection
                original_img_label.grid(row=1, column=0, padx=10, pady=10)

                # Display the stego image
                stego_img = cv2.cvtColor(stego_image, cv2.COLOR_BGR2RGB)
                stego_img = Image.fromarray(stego_img)
                stego_img = stego_img.resize((250, 250))
                stego_img_tk = ImageTk.PhotoImage(stego_img)

                stego_img_label = Label(popup, image=stego_img_tk)
                stego_img_label.image = stego_img_tk  # Prevent garbage collection
                stego_img_label.grid(row=1, column=1, padx=10, pady=10)

                # Close button
                close_button = Button(popup, text="Close", command=popup.destroy)
                close_button.grid(row=2, column=0, columnspan=2, pady=10)

            def showSecretImg(filepath):
                root.secretImagePath = filepath
                secretImgMessage.set(f"Image Chosen: {os.path.basename(filepath)}")
                secretImg = Image.open(filepath)
                secretImg = secretImg.resize((100, 100))
                secretImgTk = ImageTk.PhotoImage(secretImg)
                secretImgLabel.configure(image=secretImgTk)
                secretImgLabel.image = secretImgTk
        elif userChoice == "4MSBBL":

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

            returnButton4Msb = Button(root, text="Run", bg="lightgreen", command=lambda: handle_4msbbl_run())
            returnButton4Msb.place(relx=0.4, rely=0.9, anchor="center")
            root.returnButton4Msb = returnButton4Msb

            def handle_4msbbl_run():
                # Ensure both images are chosen
                if not hasattr(root, 'chosenImagePath') or not hasattr(root, 'secretImagePath'):
                    tkinter.messagebox.showerror("Error", "Please choose both the cover image and the secret image.")
                    return

                # Load the chosen and secret images
                image1_path = root.chosenImagePath
                image2_path = root.secretImagePath

                image1 = cv2.imread(image1_path)
                image2 = cv2.imread(image2_path)

                if image1 is None or image2 is None:
                    tkinter.messagebox.showerror("Error", "Failed to load images. Please ensure valid image paths.")
                    return

                # Resize secret image to match the cover image size
                # image2_resized = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

                # Encrypt the secret image into the cover image
                stego_image = BlueChannel.encrypt(image1.copy(), image2.copy())

                # Save the stego image
                stego_folder = "Images/stego"
                if not os.path.exists(stego_folder):
                    os.makedirs(stego_folder)

                original_filename, original_extension = os.path.splitext(os.path.basename(image1_path))
                stego_filename = f"stego_4msbbl_{original_filename}{original_extension}"
                stego_image_path = os.path.join(stego_folder, stego_filename)

                cv2.imwrite(stego_image_path, stego_image)

                # Display the original and stego images in a popup
                popup = Toplevel(root)
                popup.title("Original and Stego Images (4MSB)")
                popup.geometry("600x400")

                original_label = Label(popup, text="Original Image")
                original_label.grid(row=0, column=0, padx=10, pady=10)

                stego_label = Label(popup, text="Stego Image")
                stego_label.grid(row=0, column=1, padx=10, pady=10)

                # Display the original image
                original_img = Image.open(image1_path)
                original_img = original_img.resize((250, 250))
                original_img_tk = ImageTk.PhotoImage(original_img)

                original_img_label = Label(popup, image=original_img_tk)
                original_img_label.image = original_img_tk  # Prevent garbage collection
                original_img_label.grid(row=1, column=0, padx=10, pady=10)

                # Display the stego image
                stego_img = cv2.cvtColor(stego_image, cv2.COLOR_BGR2RGB)
                stego_img = Image.fromarray(stego_img)
                stego_img = stego_img.resize((250, 250))
                stego_img_tk = ImageTk.PhotoImage(stego_img)

                stego_img_label = Label(popup, image=stego_img_tk)
                stego_img_label.image = stego_img_tk  # Prevent garbage collection
                stego_img_label.grid(row=1, column=1, padx=10, pady=10)

                # Close button
                close_button = Button(popup, text="Close", command=popup.destroy)
                close_button.grid(row=2, column=0, columnspan=2, pady=10)

            def showSecretImg(filepath):
                root.secretImagePath = filepath
                secretImgMessage.set(f"Image Chosen: {os.path.basename(filepath)}")
                secretImg = Image.open(filepath)
                secretImg = secretImg.resize((100, 100))
                secretImgTk = ImageTk.PhotoImage(secretImg)
                secretImgLabel.configure(image=secretImgTk)
                secretImgLabel.image = secretImgTk



    root.mainloop()
