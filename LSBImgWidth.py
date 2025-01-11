import imageManipulator
import cv2
import numpy as np
import random

def resizeHost(host_img, secret_img):
    height_secret, width_secret, channels_secret = secret_img.shape
    return imageManipulator.resize_image_to_fit(host_img, (width_secret * 3, height_secret))

# Encryption function

host = cv2.imread('images/original/shell.jpg')
secret = cv2.imread('images/original/matrioska.jpg')
# Driver's code
resized_image = resizeHost(host, secret)

def encrypt(host_img, secret_img):
    resizedHost_img = resizeHost(host_img, secret_img)

    for height in range(secret_img.shape[0]):
        for width in range(secret_img.shape[1]):
            for channel in range(3):
                # v1 and v2 are 8-bit pixel values
                # of img1 and img2 respectively
                v1 = format(resizedHost_img[height][width * 3 + channel][0], '08b')
                v2 = format(secret_img[height][width][channel], '08b')

                # Taking 4 MSBs of each image
                v3 = v1[:4] + v2[:4]

                resizedHost_img[height][width * 3 + channel][0] = int(v3, 2)

    cv2.imwrite('encrypted.png', resizedHost_img)

def decrypt():
    encrypted_img = cv2.imread('encrypted.png')
    # Get dimensions of the encrypted image
    height_encrypted, width_encrypted, channels_encrypted = encrypted_img.shape
    secret_img = np.zeros((height_encrypted, width_encrypted//3, 3), dtype=np.uint8)

    for height in range(height_encrypted):
        for width in range(width_encrypted//3):
            for channel in range(3):
                # Extract 8-bit pixel value from encrypted image
                encrypted_pixel = format(encrypted_img[height][width * 3 + channel][0], '08b')

                # Extract the 4 LSBs (Least Significant Bits)
                lsb_bits = encrypted_pixel[4:]  # bits after 4 MSBs
                 # Convert binary back to decimal and assign to the secret image
                secret_img[height, width, channel] = int(lsb_bits, 2)

    cv2.imwrite('secret_decrypted.png', secret_img)



encrypt(host, secret)
decrypt()
#resized_image = resizeHost(host, secret)
#cv2.imwrite('resiz.png', resized_image)