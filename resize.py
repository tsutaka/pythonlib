import cv2
import numpy as np

def half_size(im):
        height = im.shape[0]
        width = im.shape[1]
        
        cv2.imshow("full_size",im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  
        
        half_size = cv2.resize(im,(int(width/2),int(height/2)))

        cv2.imshow("half_size",half_size)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  

if __name__ == '__main__':
    im = cv2.imread("image.jpg")
    if not (im.all() == None):
        half_size(im)
    else:
        print('Not exist')
        