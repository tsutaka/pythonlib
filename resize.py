import os

import cv2
# import numpy as np

def half_size(images):
    
    for image in images:
        height = image.shape[0]
        width = image.shape[1]
                
        cv2.imshow("full_size",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        
        half_image = cv2.resize(image,(int(width/2),int(height/2)))

        cv2.imshow("half_size",half_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  

if __name__ == '__main__':
    
    paths = os.listdir('.\image')
    print(paths)
    print(len(paths))

    images = []
    for path in paths:
        images.append(cv2.imread(path))

    if not (images[-1].all() == None):
        half_size(images)
    else:
        print('Not exist')
        exit()
        