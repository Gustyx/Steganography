import os
import re
import tkinter

from tkinter import messagebox
import tkinter.font
from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk
import cv2

import BlueChannel
from DCT import extract_message_dct_color, extract_message_dct_grayscale
from ImgStegano1 import decrypt
from LSB import extract_data



def decodePopup(chosenImagePath):
    if not chosenImagePath:
        tkinter.messagebox.showerror("Error", "No image chosen for decoding.")
        return

    popup = Toplevel()
    popup.title("Decode Image")
    popup.geometry("600x400")

    try:
        imageFilename = os.path.basename(chosenImagePath)

        # Determine the encoding type from the filename
        match = re.search(r'stego_(\w+)_', imageFilename)
        if not match:
            raise ValueError("Unable to determine encoding type from the filename.")

        encoding_type = match.group(1).upper()

        # Read the stego image
        stego_image = cv2.imread(chosenImagePath)

        if encoding_type == "4MSB":
            # Call decrypt and display only the decrypted image
            decrypted_image = decrypt(stego_image)
            decrypted_image = cv2.cvtColor(decrypted_image, cv2.COLOR_BGR2RGB)
            decrypted_image = Image.fromarray(decrypted_image)
            decrypted_image = ImageTk.PhotoImage(decrypted_image)

            decryptedLabel = Label(popup, image=decrypted_image)
            decryptedLabel.image = decrypted_image
            decryptedLabel.pack(pady=10)

        elif encoding_type == "4MSBBL":
            decrypted_image = BlueChannel.decrypt(stego_image)
            decrypted_image = cv2.cvtColor(decrypted_image, cv2.COLOR_BGR2RGB)
            decrypted_image = Image.fromarray(decrypted_image)
            decrypted_image = ImageTk.PhotoImage(decrypted_image)

            decryptedLabel = Label(popup, image=decrypted_image)
            decryptedLabel.image = decrypted_image
            decryptedLabel.pack(pady=10)

        else:
            # Load and display the chosen image
            image = Image.open(chosenImagePath)
            image = image.resize((250, 250))
            imageTk = ImageTk.PhotoImage(image)

            imageLabel = Label(popup, image=imageTk)
            imageLabel.image = imageTk
            imageLabel.pack(pady=10)

            imageTitle = Label(popup, text=f"Decoded Image: {imageFilename}")
            imageTitle.pack()

            # Decode the message based on encoding type
            if encoding_type == "LSB":
                decoded_message = extract_data(stego_image)
            elif encoding_type == "DCT":
                decoded_message = extract_message_dct_color(stego_image)
            elif encoding_type == "DCTGR":
                decoded_message = extract_message_dct_grayscale(stego_image)
            else:
                raise ValueError(f"Unsupported encoding type: {encoding_type}")

            # Display the decoded message
            messageContent = Label(popup, text=decoded_message, wraplength=500, justify="center", bg="lightyellow")
            messageContent.pack(pady=10, padx=20)

    except Exception as e:
        tkinter.messagebox.showerror("Error", f"Failed to decode the image: {str(e)}")
        popup.destroy()
        return

    # Add a close button
    buttonFont = tkinter.font.Font(family="Comic Sans MS", size=10, weight="bold")
    closeButton = Button(popup, text="Close", command=popup.destroy, font=buttonFont, relief="groove")
    closeButton.pack(pady=10)

