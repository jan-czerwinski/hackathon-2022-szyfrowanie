import argparse
from utils import (read_image)
from PIL import Image
import numpy as np
import datetime
import cv2

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
    print(stats)

    img = detect_words(img, stats)

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

def if_simmilar(first, second, diff=5):
    f = np.array([int(x) for x in first[1:-1].split(' ') if x != ' ' and x != ''], dtype=int)
    s = np.array([int(x) for x in second[1:-1].split(' ') if x != ' ' and x != ''], dtype=int)
    calculated_diff = 0
    for i in range(f.shape[0]):
        calculated_diff += abs(f[i] - s[i])

    if calculated_diff <= diff: return True
    return False

def detect_words(img, stats):
    height, width = img.shape[:2]

    to_color = []
    for k,v in stats.items():
        for k_2, v_2 in stats.items():
            if k != k_2 and v_2 > v and if_simmilar(k, k_2):
                to_color.append(k)

    new_img = np.zeros(shape=(img.shape[0], img.shape[1]), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            color = np.array2string(img[i,j,:])
            if color in to_color:
                new_img[i,j] = 255

    return new_img

if __name__ == '__main__':
    main()
