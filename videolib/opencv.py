# opencv.py
import sys          # for command line arguments
import subprocess   # for command executing
import cv2          # for using Opencv

# before use, requires install opencv with pip
# pip install opencv-python
# pip install opencv-contrib-python

def check_diff(image_path):
    # input directory's style is following:
    # 000001.jpg, 000002.jpg, 000003.jpg

    # result_list = {}
    
    # get jpg file name


    # load images
    img_src1 = cv2.imread("sample/000001.jpg", 1)
    img_src2 = cv2.imread("sample/000002.jpg", 1)

    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    #fgbg = cv2.createBackgroundSubtractorMOG()

    fgmask = fgbg.apply(img_src1)
    fgmask = fgbg.apply(img_src2)

    # 表示
    cv2.imshow('frame',fgmask)

    # 検出画像
    bg_diff_path  = './sample/diff.jpg'
    cv2.imwrite(bg_diff_path,fgmask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # check diff

    return


if __name__ == "__main__":
    # execute only if run as a script
    # ex. python opencv.py sample/
    args = sys.argv
    if(len(args) != 2) :
        print("args not have 1 arg")
    input_path = args[1]

    print("input_path:", input_path)
    
    check_diff(input_path)