import imageManipulator
import cv2
import numpy as np
import random

def resizeHost(host_img, secret_img):
    height_secret, width_secret, channels_secret = secret_img.shape
    return imageManipulator.resize_image_to_fit(host_img, (width_secret, height_secret * 3))

# Encryption function

host = cv2.imread('images/original/night.jpg')
secret = cv2.imread('images/original/lake.jpg')
# Driver's code
resized_image = resizeHost(host, secret)

def encrypt(host_img, secret_img):
    resizedHost_img = resizeHost(host_img, secret_img)

    for height in range(secret_img.shape[0]):
        for width in range(secret_img.shape[1]):
            for channel in range(3):
                # v1 and v2 are 8-bit pixel values
                # of img1 and img2 respectively
                v1 = format(resizedHost_img[height * 3 + channel][width][0], '08b')
                v2 = format(secret_img[height][width][channel], '08b')

                # Taking 4 MSBs of each image
                v3 = v1[:4] + v2[:4]

                resizedHost_img[height * 3 + channel][width][0] = int(v3, 2)

    cv2.imwrite('encrypted.png', resizedHost_img)

def decrypt2(encrypted_img):
    # Get dimensions of the encrypted image
    height_encrypted, width_encrypted, channels_encrypted = encrypted_img.shape
    secret_img = np.zeros((height_encrypted//3, width_encrypted, 3), dtype=np.uint8)

    for height in range(height_encrypted//3):
        for width in range(width_encrypted):
            for channel in range(3):
                # Extract 8-bit pixel value from encrypted image
                encrypted_pixel = format(encrypted_img[height * 3 + channel][width][0], '08b')

                # Extract the 4 LSBs (Least Significant Bits)
                lsb_bits = encrypted_pixel[4:]  # bits after 4 MSBs
                bits_to_save = lsb_bits + chr(random.randint(0, 1) + 48) * 4
                # Convert binary back to decimal and assign to the secret image
                secret_img[height, width, channel] = int(bits_to_save, 2)

    cv2.imwrite('secret_decrypted.png', secret_img)
# Decryption function
def decrypt():
    # Encrypted image
    img = cv2.imread('pic2in1.png')
    width = img.shape[0]
    height = img.shape[1]

    # img1 and img2 are two blank images
    img1 = np.zeros((width, height, 3), np.uint8)
    img2 = np.zeros((width, height, 3), np.uint8)

    for i in range(width):
        for j in range(height):
            for l in range(3):
                v1 = format(img[i][j][l], '08b')
                v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4

                # Appending data to img1 and img2
                img1[i][j][l] = int(v2, 2)
                img2[i][j][l] = int(v3, 2)

                # These are two images produced from
    # the encrypted image
    cv2.imwrite('img1_re.png', img1)
    cv2.imwrite('img2_re.png', img2)

encrypted_img = cv2.imread('encrypted.png')
#encrypt(host,secret)
decrypt2(encrypted_img)
#resized_image = resizeHost(host, secret)

#cv2.imwrite('resiz.png', resized_image)