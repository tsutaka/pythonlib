# rename.py
# 指定入力フォルダ配下のpngをリネームし、jpgに変換して指定出力フォルダに出力
import sys              # コマンドライン引数
import os               # ファイルシステム
import re               # 正規表現
import shutil           # ファイル操作
from PIL import Image   # 画像ファイル変換(pip:pillow,libtiff)

# 指定パスの画像をフォーマット変換png -> jpg
def cnvert_png_jpg(old_path, out_file_path):
    input_im = Image.open(old_path)
    rgb_im = input_im.convert('RGB')
    new_file = out_file_path + os.sep + ("image%06d.jpg" % (num))
    print("png->jpg:" + new_file)
    rgb_im.save(new_file ,quality=30)

# 指定パスの画像を通番を付けてコピーリネーム
def rename(file, out_file_path, num):
    # 正規表現検索
    png = re.compile("png") 
    if png.search(file):
        # copy + rename
        old_path = out_file_path + os.sep + ("image%06d.png" % (num))
        print("copy:" + file + "->" + old_path)
        shutil.copy2(file, old_path)

        # png -> jpg
        cnvert_png_jpg(old_path, out_file_path)

        # del
        os.remove(old_path)


        num += 1
    else:
        pass
    
    # 次の通番を返却
    return num

# フォルダ内を再帰処理
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
