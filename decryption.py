import argparse
from utils import (read_image)
from PIL import Image
import numpy as np
import datetime

def main():
    print('Script started')
    parser = argparse.ArgumentParser(description='CLI argument processing')
    parser.add_argument('--image_path', required=True, help='Path to image that is meant to be processed')
    parser.add_argument('--offset', required=False, default=3, help='Path to image that is meant to be processed')
    args = parser.parse_args()

    print('Reading image')
    img = read_image(args.image_path)
    print(f'Read image with shape{img.shape}')

    start = datetime.datetime.now()
    stats = colors_statistics(img)
    # print(stats)

    img_after_detection = detect_words(img, stats, treshold=1400)

    end = datetime.datetime.now()
    duration = (end - start).seconds
    print(f'Duration: {duration}s')
    img = Image.fromarray(img_after_detection)
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

    for i in range(height):
        for j in range(width):
            color = np.array2string(img[i,j,:])
            if stats[color] <= treshold:
                img[i,j,:] = [255,255,255]

    return img

if __name__ == '__main__':
    main()
