import cv2
import numpy as np

from ImagePaths import *


def pad_image_8x8(image):
    h, w = image.shape[:2]

    # Calculate padding amounts
    pad_h = (8 - h % 8) % 8
    pad_w = (8 - w % 8) % 8

    # Pad the image with black (zero) pixels
    padded_image = cv2.copyMakeBorder(image, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    cv2.imwrite(path_to_padded_image + "padded_8x8_" + image_name, padded_image)

    return padded_image


def embed_message_dct_grayscale(image, secret_message):
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

    cv2.imwrite(path_to_stego_image + "stego_dct_grayscale_" + image_name, image)

    return image


def extract_message_dct_grayscale(image):
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


def embed_message_dct_color(image, secret_message):
    h, w, _ = image.shape
    binary_message = ''.join([format(ord(ch), '08b') for ch in secret_message]) + '11111111'  # End marker
    idx = 0

    # Split the image into B, G, R channels
    channels = list(cv2.split(image))

    # Embed the message in the blue channel (or choose another)
    for channel_idx in range(len(channels)):
        channel = channels[channel_idx]
        for row in range(0, h, 8):
            for col in range(0, w, 8):
                if idx < len(binary_message):
                    block = channel[row:row + 8, col:col + 8]
                    dct_block = cv2.dct(np.float32(block))

                    # Embed the bit in a middle-frequency coefficient
                    bit = int(binary_message[idx])
                    coeff = int(round(dct_block[3, 3]))
                    dct_block[3, 3] = coeff - (coeff % 2) + bit

                    idct_block = cv2.idct(dct_block)
                    channel[row:row + 8, col:col + 8] = np.uint8(np.clip(idct_block, 0, 255))
                    idx += 1
                else:
                    break
        channels[channel_idx] = channel

        # Stop embedding if the entire message is embedded
        if idx >= len(binary_message):
            break

    # Merge the modified channels back together
    stego_image = cv2.merge(channels)
    cv2.imwrite(path_to_stego_image + "stego_dct_color_" + image_name, stego_image)

    return stego_image


def extract_message_dct_color(image):
    h, w, _ = image.shape
    binary_message = ''

    # Split the image into B, G, R channels
    channels = cv2.split(image)

    # Extract the message from the blue channel (or the same channel used for embedding)
    for channel in channels:
        for row in range(0, h, 8):
            for col in range(0, w, 8):
                if binary_message.endswith('11111111'):  # End marker
                    break

                block = channel[row:row + 8, col:col + 8]
                dct_block = cv2.dct(np.float32(block))

                # Extract the bit from the middle-frequency coefficient
                bit = int(round(dct_block[3, 3])) & 1
                binary_message += str(bit)

        # Stop extraction if the end marker is detected
        if binary_message.endswith('11111111'):
            break

    binary_message = binary_message[:-8]  # Remove the end marker
    secret_message = ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])
    return secret_message


def apply_dct_grayscale(image_name):
    # Load the image
    image = cv2.imread(path_to_original_image + image_name, cv2.IMREAD_GRAYSCALE)

    # Pad image
    padded_image = pad_image_8x8(image.copy())

    # Embed data
    stego_image = embed_message_dct_grayscale(padded_image.copy(), "Hello, this is secret! Don't read")

    # Extract data
    retrieved_data = extract_message_dct_grayscale(stego_image)
    print("Retrieved Data:", retrieved_data)


def apply_dct_color(image_name):
    # Load the image
    image = cv2.imread(path_to_original_image + image_name)

    # Pad image
    padded_image = pad_image_8x8(image.copy())

    # Embed data
    stego_image = embed_message_dct_color(padded_image.copy(), "Hello, this is secret! Don't read")

    # Extract data
    retrieved_data = extract_message_dct_color(stego_image)
    print("Retrieved Data:", retrieved_data)


image_name = "sid.jpg"
apply_dct_grayscale(image_name)
apply_dct_color(image_name)
