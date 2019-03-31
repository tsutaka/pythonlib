# rename.py
# files under the specified directory rename and convert from png to jpg

import sys              # for command line arguments
import os               # for command executing
import re               # for using regular expression
import shutil           # for hadling file system
from PIL import Image   # for converting image files(pip:pillow,libtiff)

# convert image file(png -> jpg)
def convert_png_jpg(old_path, out_file_path):
    input_im = Image.open(old_path)
    rgb_im = input_im.convert('RGB')
    new_file = out_file_path + os.sep + ("image%06d.jpg" % (num))
    print("png->jpg:" + new_file)
    rgb_im.save(new_file ,quality=30)

# image copy and rename with serial number 
def rename(file, out_file_path, num):
    # search with regular expression
    png = re.compile("png") 
    if png.search(file):
        # copy + rename
        old_path = out_file_path + os.sep + ("image%06d.png" % (num))
        print("copy:" + file + "->" + old_path)
        shutil.copy2(file, old_path)

        # png -> jpg
        convert_png_jpg(old_path, out_file_path)

        # del
        os.remove(old_path)


        num += 1
    else:
        pass
    
    # return next number 
    return num

# recursive processing in specified directory
def recursive_file_check(in_dir_path, out_dir_path, num):
    if os.path.exists(in_dir_path) != True:
        print("not exists:" + in_dir_path)
        exit()

    if os.path.exists(out_dir_path) != True:
        print("not exists:" + out_dir_path)
        exit()

    # directory
    if os.path.isdir(in_dir_path):
        dirs = os.listdir(in_dir_path)
        for dir in dirs:
            num = recursive_file_check(in_dir_path + os.sep + dir, out_dir_path, num)
    
    # file
    else:
        num = rename(in_dir_path, out_dir_path, num)

    return num


if __name__ == "__main__":
    # execute only if run as a script
    # ex. python rename.py test_in test_out
    args = sys.argv
    in_dir_path = args[1]
    out_dir_path = args[2]
    if(len(args) != 3) :
        print("args not have 2 arg")

    print("in_dir_path:", in_dir_path)
    print("out_dir_path:", out_dir_path)
    
    recursive_file_check(in_dir_path, out_dir_path, 1)
