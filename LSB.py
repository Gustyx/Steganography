import cv2
from ImagePaths import *
from imageManipulator import compute_difference


def embed_data(image, secret_data):
    binary_secret = ''.join(format(ord(char), '08b') for char in secret_data) + '01111111'
    data_index = 0
    for row in image:
        for pixel in row:
            for channel in range(3):  # Modify RGB channels
                if data_index < len(binary_secret):
                    pixel[channel] = int(format(pixel[channel], '08b')[:-1] + binary_secret[data_index], 2)
                    data_index += 1

    # Save stego image
    # cv2.imwrite(path_to_stego_image + "lsb" + image_name, image)
    return image


def extract_data(stego_image):
    binary_secret = ''
    for row in stego_image:
        for pixel in row:
            for channel in range(3):  # Read RGB channels
                binary_secret += format(pixel[channel], '08b')[-1]
                if binary_secret.endswith('01111111'):
                    break
            if binary_secret.endswith('01111111'):
                break
        if binary_secret.endswith('01111111'):
            break

    binary_secret = binary_secret[:-8]
    secret_data = ''.join(chr(int(binary_secret[i:i+8], 2)) for i in range(0, len(binary_secret), 8))
    return secret_data


def apply_lsb(image_name):
    # Load the image
    image = cv2.imread(path_to_original_image + image_name)

    # Embed data
    stego_image = embed_data(image.copy(), 'Hello, Steganography!\n' * 2)

    image2 = cv2.imread(path_to_stego_image + 'lsb' + image_name)

    # Extract data
    retrieved_data = extract_data(image2)
    print("Retrieved Data:", retrieved_data)


image_name = "google2.png"
# apply_lsb(image_name)
# image1 = cv2.imread(path_to_original_image + image_name)
# image2 = cv2.imread(path_to_stego_image + "lsb" + image_name)
# compute_difference(image1, image2)