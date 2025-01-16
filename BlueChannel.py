import imageManipulator
import numpy as np


def resizeHost(host_img, secret_img):
    height_secret, width_secret, channels_secret = secret_img.shape
    new_img = imageManipulator.resize_image_to_fit(host_img, (width_secret * 3, height_secret * 3))
    return new_img

# Encryption function

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

                v1 = format(resizedHost_img[height * 3 + channel][width][0], '08b')
                v2 = format(secret_img[height][width][channel], '08b')

                # Taking 4 MSBs of each image
                v3 = v1[:4] + v2[4:]

                resizedHost_img[height * 3 + channel][width][0] = int(v3, 2)

    return resizedHost_img
def decrypt(encrypted_img):
    # Get dimensions of the encrypted image
    height_encrypted, width_encrypted, channels_encrypted = encrypted_img.shape
    secret_img = np.zeros((height_encrypted // 3, width_encrypted// 3, 3), dtype=np.uint8)

    for height in range(height_encrypted//3):
        for width in range(width_encrypted//3):
            for channel in range(3):
                encrypted_pixel = format(encrypted_img[height ][width * 3 + channel][0], '08b')

                lsb_bits1 = encrypted_pixel[4:]  # bits after 4 MSBs

                encrypted_pixel = format(encrypted_img[height * 3 + channel][width][0], '08b')

                lsb_bits2 = encrypted_pixel[4:]  # bits after 4 MSBs
                bits_to_save = lsb_bits1 + lsb_bits2

                secret_img[height, width, channel] = int(bits_to_save, 2)

    return secret_img