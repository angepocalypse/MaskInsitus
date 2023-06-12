import cv2
import numpy as np
from PIL import Image

def overlay_images(background_path, mask_path, foreground_path, output_path):
    # Load images
    background = cv2.imread(background_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    foreground = cv2.imread(foreground_path)

    # Extract the alpha channel from the mask
    alpha_channel = mask[:, :, 3]

    # Find the coordinates of the non-zero alpha values
    coords = np.where(alpha_channel != 0)

    # Calculate the bounding box of the non-zero alpha values
    ymin, ymax = np.min(coords[0]), np.max(coords[0])
    xmin, xmax = np.min(coords[1]), np.max(coords[1])

    # Resize the foreground image to match the size of the bounding box
    foreground_resized = cv2.resize(foreground, (xmax - xmin + 1, ymax - ymin + 1))

    # Create a blank image with the size of the mask
    overlay = np.zeros_like(mask)

    # Calculate translation values for aligning the resized foreground with the mask
    tx = xmin
    ty = ymin

    # Apply the translation to the resized foreground
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    foreground_translated = cv2.warpAffine(foreground_resized, M, (mask.shape[1], mask.shape[0]))

    # Merge the foreground with the alpha channel
    overlay[:, :, :3] = foreground_translated
    overlay[:, :, 3] = mask[:, :, 3]

    # Resize the overlay image to match the size of the background image
    overlay_resized = cv2.resize(overlay, (background.shape[1], background.shape[0]), interpolation=cv2.INTER_AREA)

    # Normalize the alpha channel values to the range [0, 1]
    alpha_normalized = overlay_resized[:, :, 3] / 255.0

    # Blend the foreground and background images using the alpha channel
    result = np.zeros_like(background, dtype=np.uint8)
    for c in range(3):
        result[:, :, c] = (1 - alpha_normalized) * background[:, :, c] + alpha_normalized * overlay_resized[:, :, c]

    # Convert the resulting image to RGB format
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # Save the resulting image using PIL
    result_pil = Image.fromarray(result_rgb)
    result_pil.save(output_path)


# Example usage
background_path = 'img/pexels-karolina-grabowska-4207891_1080.png'
mask_path = 'img/pexels-karolina-grabowska-4207891_1080_mask.png'
foreground_path = 'img/tame_impala_bleed_11x14.jpg'
output_path = 'output4.jpg'

overlay_images(background_path, mask_path, foreground_path, output_path)
