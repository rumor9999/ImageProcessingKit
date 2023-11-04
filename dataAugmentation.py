import os
import sys
import random
import cv2
import math
import numpy as np
import tkinter as tk
from glob import glob
from tkinter import filedialog
from multiprocessing import Pool


def rotate_image(image, angle):
    # Find the center of the image
    center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    # Calculate the largest rectangle area to be cropped after rotation
    cropped_rect = largest_rotated_rect(image.shape[1], image.shape[0], angle)
    cropped_result = result[int(cropped_rect[1]):int(cropped_rect[1]+cropped_rect[3]),
                            int(cropped_rect[0]):int(cropped_rect[0]+cropped_rect[2])]
    if cropped_result is None or not np.any(cropped_result):
        return result
    return cropped_result


def largest_rotated_rect(w, h, angle):
    """
    Calculate the largest rectangle that can be contained within the rotated rectangle.
    """
    angle = angle % 180
    angle_rad = np.deg2rad(angle)
    if w <= 0 or h <= 0:
        return 0, 0, 0, 0

    # Check if w or h is less than or equal to zero
    if w <= 0:
        w = 1
    if h <= 0:
        h = 1

    width_is_longer = w >= h
    side_long, side_short = (w, h) if width_is_longer else (h, w)

    # Ratios of the cosine and sine of the angle
    sin_a = np.sin(angle_rad)
    cos_a = np.cos(angle_rad)

    if side_short <= 2. * sin_a * cos_a * side_long:
        x = 0.5 * side_short
        wr, hr = (x / sin_a, x / cos_a)
    else:
        cos_2a = cos_a * cos_a - sin_a * sin_a
        wr, hr = (w * cos_a - h * sin_a) / \
            cos_2a, (h * cos_a - w * sin_a) / cos_2a

    return ((w - wr) / 2, (h - hr) / 2, wr, hr)


def random_crop_orig(image):
    height, width = image.shape[:2]
    if height < 512 or width < 512:
        return image
    crop_size = random.randint(512, min(height, width))
    x = random.randint(0, width - crop_size)
    y = random.randint(0, height - crop_size)
    return image[y:y+crop_size, x:x+crop_size]


def random_crop(image):
    height, width = image.shape[:2]
    min_crop_height = min(max(int(height * 0.6), 512), height)
    min_crop_width = min(max(int(width * 0.6), 512), width)
    crop_height = random.randint(min_crop_height, height)
    crop_width = random.randint(min_crop_width, width)
    for i in range(10):
        x = random.randint(0, width - crop_width)
        y = random.randint(0, height - crop_height)
        crop = image[y:y+crop_height, x:x+crop_width]
        if np.mean(crop)//255 < 0.9:
            return crop
    return image


def adjust_brightness_contrast(image, brightness=0, contrast=0):
    return cv2.addWeighted(image, 1 + float(contrast) / 100.0, image, 0, float(brightness))


def process_image(args):
    image_path, output_dir, num_rotations, num_crops, num_contrasts, num_brightnesses = args
    print(f"Processing image: {image_path}")

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Failed to read image {image_path}")
        return

    # Save a copy of the original image
    original_image_path = os.path.join(
        output_dir, f"orig_{os.path.splitext(os.path.basename(image_path))[0]}.png")
    cv2.imwrite(original_image_path, image)

    # Perform specified number of rotations and save copies
    for j in range(num_rotations):
        angle = random.uniform(-10, 10)
        rotated_image = rotate_image(image.copy(), angle)
        rotated_image_path = os.path.join(
            output_dir, f"rot{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(rotated_image_path, rotated_image)
        # print(f"Saved rotated image: {rotated_image_path}")

    # Randomly crop the image with a minimum size of 512x512 and save copies
    for j in range(num_crops):
        cropped_image = random_crop(image)
        cropped_image_path = os.path.join(
            output_dir, f"cro{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(cropped_image_path, cropped_image)
        # print(f"Saved cropped image: {cropped_image_path}")

    # Perform specified number of contrast adjustments and save copies
    for j in range(num_contrasts):
        contrast = random.uniform(0.2, 2.0)
        contrasted_image = adjust_brightness_contrast(image, contrast=contrast)
        contrasted_image_path = os.path.join(
            output_dir, f"contrast_{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(contrasted_image_path, contrasted_image)
        # print(f"Saved contrast-adjusted image: {contrasted_image_path}")

    # Perform specified number of brightness adjustments and save copies
    for j in range(num_brightnesses):
        brightness = random.uniform(-25, 25)
        brightened_image = adjust_brightness_contrast(
            image, brightness=brightness)
        brightened_image_path = os.path.join(
            output_dir, f"brightness_{j+1}_{os.path.splitext(os.path.basename(image_path))[0]}.png")
        cv2.imwrite(brightened_image_path, brightened_image)
        # print(f"Saved brightness-adjusted image: {brightened_image_path}")

    print("Data augmentation completed.")


def dataSetAug(input_dir, output_dir, num_rotations: int, num_crops: int, num_contrasts: int, num_brightnesses: int):

    # If output directory does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process images in input directory
    image_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff')
    image_paths = []
    for format in image_formats:
        image_paths.extend(glob(os.path.join(input_dir, format)))

    print("Processing images...")

    # Use a Pool of processes to process each image in parallel
    num_processes = os.cpu_count()
    with Pool(num_processes) as pool:
        pool.map(process_image, [(image_path, output_dir, num_rotations, num_crops,
                                  num_contrasts, num_brightnesses) for image_path in image_paths])

    print("Data augmentation completed.")


if __name__ == '__main__':
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Ask user to select input directory
    print("Please select the input directory...")
    input_dir = filedialog.askdirectory(title="Select input directory")

    # Ask user to select output directory
    print("Please select the output directory...")
    output_dir = filedialog.askdirectory(title="Select output directory")

    # Get user input for data augmentation parameters
    num_rotations = int(
        input("Enter the number of rotations for each image: "))
    num_crops = int(input("Enter the number of random crops for each image: "))
    num_contrasts = int(
        input("Enter the number of contrast adjustments for each image: "))
    num_brightnesses = int(
        input("Enter the number of brightness adjustments for each image: "))

    dataSetAug(input_dir, output_dir, num_rotations,
               num_crops, num_contrasts, num_brightnesses)
