import cv2

from ImagePaths import path_to_grayscale_image


def convert_to_grayscale(image):
    """
    Convert an image to grayscale and save the result.

    Args:
        input_image_path (str): Path to the input image.
        output_image_path (str): Path to save the grayscale image.

    Returns:
        None
    """
    # Read the image
    # image = cv2.imread(input_image_path)

    # Check if the image was loaded successfully
    # if image is None:
    #     raise ValueError(f"Could not load image from {input_image_path}")

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    cv2.imwrite(path_to_grayscale_image + "grayscale_sid.jpg", grayscale_image)

    return grayscale_image

# input_path = "padded_sid.png"  # Replace with your input image path
# output_path = "grayscale_image.png"  # Replace with your desired output path
# convert_to_grayscale(input_path, output_path)
