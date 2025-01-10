import cv2
import numpy as np

from Greyscale import convert_to_grayscale
from ImagePaths import *

def pad_image(image):
    """
    Pad the image so that both height and width are divisible by 8.

    Args:
        image (numpy.ndarray): The input image.

    Returns:
        numpy.ndarray: Padded image.
    """
    h, w = image.shape[:2]

    # Calculate padding amounts
    pad_h = (8 - h % 8) % 8
    pad_w = (8 - w % 8) % 8

    # Pad the image with black (zero) pixels
    padded_image = cv2.copyMakeBorder(image, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    cv2.imwrite(path_to_padded_image + "padded_sid.jpg", padded_image)
    return padded_image

def convert_to_grayscale(image):
    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    cv2.imwrite(path_to_grayscale_image + "grayscale_sid.jpg", grayscale_image)

    return grayscale_image

def embed_message_dct_grayscale(image, secret_message):
    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # if image is None:
    #     raise ValueError("Could not load image.")

    h, w = image.shape
    binary_message = ''.join([format(ord(ch), '08b') for ch in secret_message]) + '11111111'  # End marker
    idx = 0

    for row in range(0, h, 8):
        for col in range(0, w, 8):
            if idx < len(binary_message):
                block = image[row:row + 8, col:col + 8]
                dct_block = cv2.dct(np.float32(block))

                bit = int(binary_message[idx])
                coeff = int(round(dct_block[3, 3]))
                dct_block[3, 3] = coeff - (coeff % 2) + bit

                idct_block = cv2.idct(dct_block)
                image[row:row + 8, col:col + 8] = np.uint8(np.clip(idct_block, 0, 255))
                idx += 1

    cv2.imwrite(path_to_stego_image + "_stego_dct_" + "sid.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 95])
    # print(f"Message embedded and saved to {output_path}")
    return image

def extract_message_dct_grayscale(image):
    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # if image is None:
    #     raise ValueError("Could not load image.")

    h, w = image.shape
    binary_message = ''

    for row in range(0, h, 8):
        for col in range(0, w, 8):
            if binary_message.endswith('11111111'):  # End marker
                break

            block = image[row:row + 8, col:col + 8]
            dct_block = cv2.dct(np.float32(block))

            bit = int(round(dct_block[3, 3])) & 1
            binary_message += str(bit)

    binary_message = binary_message[:-8]  # Remove end marker
    secret_message = ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])

    return secret_message


def apply_dct(image_name):
    # Load the image
    image = cv2.imread(path_to_original_image + image_name)

    # Pad image
    padded_image = pad_image(image.copy())

    # Grayscale image
    grayscale_image = convert_to_grayscale(padded_image)

    # Embed data
    stego_image = embed_message_dct_grayscale(grayscale_image.copy(), "Hello, this is secret! Don't read.")

    # Save stego image
    # cv2.imwrite(path_to_stego_image + "stego_" + image_name, stego_image)

    # Extract data
    retrieved_data = extract_message_dct_grayscale(stego_image)
    print("Retrieved Data:", retrieved_data)


# embed_message_dct_grayscale(path_to_original_image + "sid_grayscale.jpg", "Hello, this is secret! Don't read.", "stego_dct_" + "sid.jpg")
# message = extract_message_dct_grayscale(path_to_stego_image + "stego_dct_" + "sid.jpg")
# print("Extracted message:", message)


image_name = "sid.jpg"
apply_dct(image_name)
