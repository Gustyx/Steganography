import cv2
import numpy as np
import random

def encrypt(img1, img2):
    # img1 and img2 are the
    # two input images

    for height in range(img2.shape[0]):
        for width in range(img2.shape[1]):
            for channel in range(3):
                # v1 and v2 are 8-bit pixel values
                # of img1 and img2 respectively
                v1 = format(img1[height][width][channel], '08b')
                v2 = format(img2[height][width][channel], '08b')

                # Taking 4 MSBs of each image
                v3 = v1[:4] + v2[:4]

                img1[height][width][channel] = int(v3, 2)

    return img1


def decrypt(img):
    # Encrypted image
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
    return img2

