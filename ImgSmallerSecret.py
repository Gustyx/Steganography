import imageManipulator
import cv2
import numpy as np

def resizeSecret(host_img, secret_img):
    height_host, width_host, _ = host_img.shape
    # Resize secret image to 1/3 the width of the host image
    return imageManipulator.resize_image_to_fit(secret_img, (width_host // 3, height_host))

# Encryption function
def encrypt(host_img, secret_img):
    resized_secret_img = resizeSecret(host_img, secret_img)
    for height in range(resized_secret_img.shape[0]):
        for width in range(resized_secret_img.shape[1]):
            for channel in range(3):
                # Convert pixel values to binary
                v1 = format(host_img[height][width][channel], '08b')
                v2 = format(resized_secret_img[height][width][channel], '08b')

                # Combine 4 MSBs from host and secret images
                v3 = v1[:4] + v2[:4]

                # Update the host image with the embedded secret
                host_img[height][width][channel] = int(v3, 2)

    # Save the encrypted image
    cv2.imwrite('encrypted.png', host_img)

def decrypt():
    encrypted_img = cv2.imread('encrypted.png')
    # Get dimensions of the encrypted image
    height, width, _ = encrypted_img.shape
    secret_width = width // 3

    # Create an empty array for the secret image
    secret_img = np.zeros((height, secret_width, 3), dtype=np.uint8)

    for height_idx in range(height):
        for width_idx in range(secret_width):
            for channel in range(3):
                # Extract 8-bit pixel value from the encrypted image
                encrypted_pixel = format(encrypted_img[height_idx][width_idx][channel], '08b')

                # Extract the 4 LSBs (embedded secret information)
                lsb_bits = encrypted_pixel[4:]

                # Reconstruct the secret image pixel value
                secret_img[height_idx, width_idx, channel] = int(lsb_bits + '0000', 2)

    # Save the reconstructed secret image

    cv2.imwrite('secret_decrypted.png', secret_img)

# Load images
host = cv2.imread('images/original/shell.jpg')
secret = cv2.imread('images/original/matrioska.jpg')

# Perform encryption and decryption
encrypt(host, secret)
decrypt()
