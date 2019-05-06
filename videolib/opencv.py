"""
opencv.py

Notes
-----
before use, requires install opencv with pip
pip install opencv-python
pip install opencv-contrib-python --user
"""
import sys          # for command line arguments
import cv2          # for using Opencv
from PIL import Image # for using PIL format


def check_diff(input_path1, input_path2):
    """
    return num of diff pixel
    """
    INTERVAL = 10

    # load images
    img_src1 = cv2.imread(str(input_path1), 1)
    img_src2 = cv2.imread(str(input_path2), 1)

    # check diff
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    diff_image = fgbg.apply(img_src1)
    diff_image = fgbg.apply(img_src2)

    # save image
    # cv2.imwrite('test.jpg',th1)

    # show image
    # cv2.imshow('frame',diff_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # calcurate diff
    diff_pixels = 0
    image_pil = Image.fromarray(diff_image)
    image_pil = image_pil.convert('RGB')
    image_size = image_pil.size

    for index_y in range(int(image_size[1])):
        if(index_y % INTERVAL != 0):
            continue

        for index_x in range(int(image_size[0])):
            if(index_x % INTERVAL != 0):
                continue

            red, green, blue = image_pil.getpixel((index_x, index_y))
            if(blue == 255 and green == 255 and red == 255):
                diff_pixels += 1

    return diff_pixels, int(int(image_size[0]) * int(image_size[1]) / (INTERVAL * INTERVAL))

def binarization(input_path, output_path, threshold):
    """
    return image of binarization
    """
    img = cv2.imread(input_path, 0)
    img = cv2.medianBlur(img, 5)

    ret, th1 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    # print(ret)

    # save image
    cv2.imwrite(output_path,th1)

    # show image
    # cv2.imshow("mono", th1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    # execute only if run as a script
    # ex. python opencv.py sample/000001.jpg sample/000002.jpg sample/diff000001.jpg
    args = sys.argv
    if(len(args) != 1 + 3):
        print("args not have 3 arg")
        exit()
    in1 = args[1]
    in2 = args[2]
    out = args[3]

    print("in1:", in1)
    print("in2:", in2)
    print("out:", out)

    check_diff(in1, in2)

    # binarization(in1, out, 127)
