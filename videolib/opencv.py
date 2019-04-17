# opencv.py
import sys          # for command line arguments
import subprocess   # for command executing
import cv2          # for using Opencv

# before use, requires install opencv with pip
# pip install opencv-python
# pip install opencv-contrib-python --user

def check_diff(input_path1, input_path2, output_path):
    # load images
    img_src1 = cv2.imread(input_path1, 1)
    img_src2 = cv2.imread(input_path2, 1)

    # check diff
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    fgmask = fgbg.apply(img_src1)
    fgmask = fgbg.apply(img_src2)

    # save image
    bg_diff_path  = output_path
    cv2.imwrite(bg_diff_path,fgmask)

    # show
    # cv2.imshow('frame',fgmask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return


if __name__ == "__main__":
    # execute only if run as a script
    # ex. python opencv.py sample/000001.jpg sample/000002.jpg sample/diff000001.jpg
    args = sys.argv
    if(len(args) != 1 + 3) :
        print("args not have 1 arg")
        exit()
    input_path1 = args[1]
    input_path2 = args[2]
    output_path = args[3]

    print("input_path1:", input_path1)
    print("input_path2:", input_path2)
    print("output_path:", output_path)
    
    check_diff(input_path1, input_path2, output_path)