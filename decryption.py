import argparse
from utils import (read_image)
from PIL import Image
import numpy as np
import datetime

def main():
    print('Script started')
    parser = argparse.ArgumentParser(description='CLI argument processing')
    parser.add_argument('--image_path', required=True, help='Path to image that is meant to be processed')
    args = parser.parse_args()

    start = datetime.datetime.now()
    print('Reading image')
    img = read_image(args.image_path)
    print(f'Read image with shape{img.shape}')

    stats = colors_statistics(img)
    # print(stats)

    img = detect_words(img, stats, treshold=1400)

    end = datetime.datetime.now()
    duration = (end - start).seconds
    print(f'Duration: {duration}s')
    print(img.shape)
    img = Image.fromarray(img)
    img.save('detected.png')

def colors_statistics(img):
    width = img.shape[1]
    height = img.shape[0]

    statistics = {}

    for i in range(height):
        for j in range(width):
            color = np.array2string(img[i,j,:])
            if color not in statistics:
                statistics[color] = 1
            else:
                statistics[color] += 1

    return statistics

def detect_words(img, stats, treshold=1000):
    height, width = img.shape[:2]

    new_img = np.zeros(shape=(img.shape[0], img.shape[1]), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            color = np.array2string(img[i,j,:])
            if stats[color] <= treshold:
                new_img[i,j] = 255

    return new_img

if __name__ == '__main__':
    main()
