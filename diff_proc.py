"""
diff_proc.py
"""
import os # for handling directory
import re # for using regular expression
import sys # for command line arguments
import json # for using json

# internal import
from videolib.opencv import check_diff

def diff_proc(target_path):
    """
    make diff.json 
    """
    prev_file_name = ""

    jpeg_list = []
    files = os.listdir(target_path)
    for file_str in files:
        if(re.findall(r'^(\d){6}\.jpg$', file_str)):
            jpeg_list += [file_str]

    for file_name in jpeg_list:
        if prev_file_name == "":
            prev_file_name = file_name
            continue

        output_json = {}
        diff_frame, full_frame = check_diff(
            target_path + os.sep + prev_file_name,
            target_path + os.sep + file_name)

        output_json[str(file_name)] = {
            'target':prev_file_name,
            'diff':diff_frame,
            'full':full_frame}

        prev_file_name = file_name

        output_fp = open(
            target_path + os.sep +
            'diff' + file_name[:-3] + 'json', 'w')
        json.dump(output_json, output_fp, indent=4)

if __name__ == "__main__":
    # execute only if run as a script
    # ex. python diff_proc.py ./assets/sample1
    args = sys.argv
    if(len(args) != 1 + 1):
        exit()
    path = args[1]

    print("diff_chk_path:", path)

    diff_proc(path)
