import cv2
from ImagePaths import *


def embed_data(image, secret_data):
    binary_secret = ''.join(format(ord(char), '08b') for char in secret_data) + '011111111'
    data_index = 0
    for row in image:
        for pixel in row:
            for channel in range(3):  # Modify RGB channels
                if data_index < len(binary_secret):
                    pixel[channel] = int(format(pixel[channel], '08b')[:-1] + binary_secret[data_index], 2)
                    data_index += 1

    # Save stego image
    cv2.imwrite(path_to_stego_image + "lsb_" + image_name, image)
    return image


def extract_data(stego_image):
    binary_secret = ''
    for row in stego_image:
        for pixel in row:
            for channel in range(3):  # Read RGB channels
                binary_secret += format(pixel[channel], '08b')[-1]
                if binary_secret.endswith('011111111'):
                    break
            if binary_secret.endswith('011111111'):
                break
        if binary_secret.endswith('011111111'):
            break

    binary_secret = binary_secret[:-9]
    secret_data = ''.join(chr(int(binary_secret[i:i+8], 2)) for i in range(0, len(binary_secret), 8))
    return secret_data


def compute_difference(image1, image2):
    # Ensure both images are the same size
    if image1.shape != image2.shape:
        raise ValueError("Images must have the same dimensions for comparison.")

    # Convert images to grayscale for simplicity
    if len(image1.shape) == 3:  # Convert RGB to Grayscale
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    else:
        gray1, gray2 = image1, image2

    # Compute the absolute difference
    difference = cv2.absdiff(gray1, gray2)

    # Threshold the difference to make it binary
    _, binary_difference = cv2.threshold(difference, 0, 255, cv2.THRESH_BINARY)

    return binary_difference


def apply_lsb(image_name):
    # Load the image
    image = cv2.imread(path_to_original_image + image_name)

    # Embed data
    stego_image = embed_data(image.copy(), 'Hello, Steganography!\n' * 3)

    image2 = cv2.imread(path_to_stego_image + 'lsb_' + image_name)

    # Extract data
    retrieved_data = extract_data(image2)
    print("Retrieved Data:", retrieved_data)


def calculate_difference_lsb(image_name):
    # Load the images
    original_image = cv2.imread(path_to_original_image + image_name)
    stego_image = cv2.imread(path_to_stego_image + "lsb_" + image_name)

    # Compute the difference
    difference_image = compute_difference(original_image, stego_image)

    # Save and display the difference image
    cv2.imwrite(path_to_difference_image + "difference_lsb_" + image_name, difference_image)
    cv2.imshow("Difference Image", difference_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_name = "sid.jpg"
apply_lsb(image_name)
# calculate_difference_lsb(image_name)
