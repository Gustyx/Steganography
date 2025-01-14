import cv2

from ImagePaths import path_to_difference_image


def pad_image_to_fit(image, target_size):
    target_width, target_height = target_size
    h, w = image.shape[:2]

    # # Calculate padding to center the image
    top_pad = (target_height - h) // 2
    bottom_pad = target_height - h - top_pad
    left_pad = (target_width - w) // 2
    right_pad = target_width - w - left_pad

    # Pad the image
    padded_image = cv2.copyMakeBorder(image, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=0)

    return padded_image

def resize_image_to_fit(image, target_size):
    """
    Resize an image to fit within a maximum size, maintaining aspect ratio.

    Args:
        image (numpy.ndarray): Image to be resized.
        max_size (tuple): Maximum (height, width) of the output image.

    Returns:
        numpy.ndarray: Resized image.
    """

    target_width, target_height = target_size
    h, w = image.shape[:2]

    # if h > target_height or w > target_width:
    scaling_factor = min(target_height / h, target_width / w)
    new_height = int(h * scaling_factor)
    new_width = int(w * scaling_factor)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    if new_width == target_width and new_height == target_height:
        return resized_image
    else:
        padded_image = pad_image_to_fit(resized_image.copy(), target_size)
    return padded_image
    # else:
    #     padded_image = pad_image_to_fit(image.copy(), target_size)
    #     return padded_image


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

    cv2.imwrite(path_to_difference_image + "difference", binary_difference)
    cv2.imshow("Difference Image", binary_difference)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return binary_difference


# Example usage
embedded_image = cv2.imread("images/original/sid.jpg")
resized_image = resize_image_to_fit(embedded_image, (700, 400))

cv2.imwrite("resize_sid.jpg", resized_image)
