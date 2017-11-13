import os

import cv2
# import numpy as np

def resize(image):
    
    height = image.shape[0]
    width = image.shape[1]
            
    # cv2.imshow("full_size",image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows() 
    
    resize_image = cv2.resize(image,(256,256))

    # cv2.imshow("half_size",resize_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()  
    
    return resize_image
    

if __name__ == '__main__':
    
    paths = os.listdir('./image')
    print(paths)

    images = []
    for path in paths:
        images.append(cv2.imread('./image/' + path))

    for (image, path) in zip(images, paths):
        cv2.imwrite('./output/' + path, resize(image))

        