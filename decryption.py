import argparse
from typing import final
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

    img_width = img.shape[1]

    stats = colors_statistics(img)
    # print(stats)

    img = detect_words(img, stats)

    # modyfing img by reference
    contours = detect_contours(img)

    word_lengths = get_word_lengths_from_contours(contours, img_width)

    # wrap_words(contours)

    end = datetime.datetime.now()
    duration = (end - start).seconds
    print(f'Duration: {duration}s')
    print(img.shape)
    img = Image.fromarray(img)
    img.save('detected.png')

def get_word_lengths_from_contours(contours, img_width):
    all_widths = []
    for line in contours:
        for val in line:
            all_widths.append(val[2])

    print(all_widths)
    median = all_widths[len(all_widths) // 2]
    print(median)
    
    word_lengths = []
    diffs = []
    
    for line in contours:
        for i in range(len(line) - 1):
            cont_1 = line[i]
            cont_2 = line[i+1]

            diffs.append(abs(cont_1[0] + cont_1[2] - cont_2[0]))

        last_cont = line[-1]
        diffs.append(img_width - last_cont[0] - last_cont[2])

    print(diffs)

    tmp_len = 0
    for i, diff in enumerate(diffs):
        if diff < median:
            tmp_len += 1
            continue
        word_lengths.append(tmp_len+1)
        tmp_len = 0

    return word_lengths
            

def detect_contours(img):
    literki = img.copy()

    _, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    # Find the contours
    contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detectedContours = [cv2.boundingRect(contour) for contour in contours]

    # print(detectedContours[0])

    average_width = 0

    for cont in detectedContours:
        average_width += cont[2]

    average_width /= len(detectedContours)
    average_width *= 0.7

    final_contours = [cont for cont in detectedContours if cont[2] > average_width]

    # print(f'contours amount = {len(final_contours)}')

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

    # print(len(final_contours))

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    color = (255, 0, 255)


    # final_contours = sorted(final_contours , key=lambda k: [k[0], k[1]])



    # print("="*80)
    # print(helper_dupa)
    # print(final_contours)

    lines = []
    while final_contours:
        line_y = final_contours[0][1] + final_contours[0][3]/2
        # print(line_y)
        detected_in_line = []
        helper_dupa = final_contours[::]

        for index, contour in enumerate(helper_dupa):
            if line_y - 40 < contour[1] < line_y + 40:
                detected_in_line.append(contour)
                final_contours.remove(contour)
        lines.append(detected_in_line)

    print("="*80)    
    for i in lines:
        print(i)

    for line in lines:
        line.sort(key=lambda k: k[0])

    lines.sort(key=lambda k: k[0][1])

    print("="*80)    
    for i in lines:
        print(i)


    for line in lines:
        id = 0
        for cnt in line:
            (x, y, w, h) = cnt
            # cv2.rectangle(literki,(x, y), (x + w, y + h), (200,0,0), -1)
            cv2.putText(literki, f'{id}', (x,y), font,
                        font_scale, color, 1, cv2.LINE_AA)
            id += 1

    literki = Image.fromarray(literki)
    literki.save('literki.png')

    # final_contours.sort(key=)

    return lines

def compare_contours(c1, c2):
    if c1[0] < c2[0] and c1[1] <= c2[1]:
        return -1

    # if c1[0] < c2[0]
    
        

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
