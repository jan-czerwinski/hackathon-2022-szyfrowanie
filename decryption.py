import argparse

from numpy.lib.npyio import save
from utils import (read_image)
from PIL import Image
import numpy as np
import datetime
import cv2
import re


def main():
    print('Script started')
    parser = argparse.ArgumentParser(description='CLI argument processing')
    parser.add_argument('--image_path', required=True, help='Path to image that is meant to be processed')
    args = parser.parse_args()

    start = datetime.datetime.now()
    print('Reading image')
    img = read_image(args.image_path)
    print(f'Read image with shape{img.shape}')

    img_width = img.shape[1]

    stats = colors_statistics(img)

    img = detect_words(img, stats)

    # modyfing img by reference
    contours = detect_contours(img)

    word_lengths = get_word_lengths_from_contours(contours, img_width)

    index1, index2 = find_word_regex(word_lengths)

    with open(f'{args.image_path[:-4]}.txt', 'w') as save_file:
        save_file.write(f'{index1} {index2}')

    end = datetime.datetime.now()
    duration = (end - start).total_seconds() * 1000
    print(f'Duration: {duration}ms')

def get_word_lengths_from_contours(contours, img_width):
    all_widths = []
    for line in contours:
        for val in line:
            all_widths.append(val[2])

    median = all_widths[len(all_widths) // 2]
    word_lengths = []
    diffs = []
    all_contours = []
    i = 0
    for line in contours:
        all_contours += line
        for i in range(len(line) - 1):

            cont_1 = line[i]
            cont_2 = line[i+1]

            current_diff = abs(cont_1[0] + cont_1[2] - cont_2[0])

            if cont_1[2] > 1.75 * median:
                diffs.append(median // 2 - 1)

            diffs.append(current_diff)
            i += 1

        last_cont = line[-1]
        diffs.append(img_width - last_cont[0] - last_cont[2])
        i += 1

    tmp_len = 0
    for i, diff in enumerate(diffs):
        if diff < median:
            tmp_len += 1
            continue
        word_lengths.append(tmp_len+1)
        tmp_len = 0

    return word_lengths
            

def detect_contours(img):
    _, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    # Find the contours
    contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detectedContours = [cv2.boundingRect(contour) for contour in contours]

    average_width = 0

    for cont in detectedContours:
        average_width += cont[2]

    average_width /= len(detectedContours)
    average_width *= 0.7

    final_contours = [cont for cont in detectedContours if cont[2] > average_width]

    for cnt in final_contours:
        (x, y, w, h) = cnt
        cv2.rectangle(img,(x, y), (x + w, y + h), (200,0,0), -1)

    
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, hierarchy= cv2.RETR_FLOODFILL)
    detectedContours = [cv2.boundingRect(contour) for contour in contours]

    for cont in detectedContours:
        average_width += cont[2]

    average_width /= len(detectedContours)
    average_width *= 0.8

    final_contours = [cont for cont in detectedContours if cont[2] > average_width]

    lines = []
    line_threshold = final_contours[0][3]
    while final_contours:
        line_y = final_contours[0][1] + final_contours[0][3]/2
        detected_in_line = []
        copy_of_final_contours = final_contours[::]

        for _, contour in enumerate(copy_of_final_contours):
            if line_y - line_threshold < contour[1] < line_y + line_threshold:
                detected_in_line.append(contour)
                final_contours.remove(contour)
        lines.append(detected_in_line)

    for line in lines:
        line.sort(key=lambda k: k[0])

    lines.sort(key=lambda k: k[0][1])

    return lines

def colors_statistics(img):
    im_pil = Image.fromarray(img)
    stats_arr = im_pil.getcolors(maxcolors=256)

    colors_statistics = {}
    for color in stats_arr:
        color_str = np.array2string(np.array([color[1][0], color[1][1], color[1][2]]))
        colors_statistics[color_str] = color[0]
    
    return colors_statistics

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

    to_color = {}
    for k,v in stats.items():
        for k_2, v_2 in stats.items():
            if k != k_2 and v_2 > v and if_simmilar(k, k_2):
                to_color[k] = 1

    new_img = np.zeros(shape=(img.shape[0], img.shape[1]), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            color = np.array2string(img[i, j, :])
            if color in to_color:
                new_img[i, j] = 255
    return new_img

def find_word_regex(words_lengths):
    search_string = " ".join(["." * word_len for word_len in words_lengths])

    with open("w_pustyni_i_w_puszczy.txt", "r", encoding="utf-8") as f:
        txt = f.read()
    sentence = re.search(search_string, txt)

    first_word_index = txt[:sentence.start()].count(" ") + 1
    last_word_index = first_word_index + sentence.group().count(" ")

    return first_word_index, last_word_index


if __name__ == '__main__':
    main()
