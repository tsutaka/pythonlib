"""
controll.py
"""
import os # for handling directory
import re # for using regular expression
import subprocess   # for command executing
import shlex        # for escaping cmd
import json # for using json

import pyxel # for using GUI output

# internal import
from videolib.ffmpeg import movie_full_to_images
from videolib.ffmpeg import get_movie_duration

COLOR_GREEN = 3
COLOR_LIGHTGREEN = 11
COLOR_ORANGE = 9

class VideoCtrl:
    """
    VideoCtrl is class for handling video file(mp4) on GUI.
    """
    SCREEN_WIDTH = 255
    SCREEN_HEIGHT = 255

    VIDEO_LIST_OFFSET_X = 2
    VIDEO_LIST_OFFSET_Y = 2

    VIDEO_DETAIL_OFFSET_X = 2
    VIDEO_DETAIL_OFFSET_Y = 60

    MENU_MAX = 8
    INPUT_WAIT = 5
    INPUT_LONG_WAIT = 10

    VIDEO_PATH = "." + os.sep + "assets"

    def __init__(self):
        pyxel.init(
            VideoCtrl.SCREEN_WIDTH,
            VideoCtrl.SCREEN_HEIGHT,
            caption="video controller")

        self.cursor_pos = 0
        self.cursor_offset = 0
        self.input_wait_counter = 0
        self.processing_file = ""
        self.duration = 0
        self.target_path = ""

        pyxel.run(self.update, self.draw)

    def update(self):
        """
        check key and mouse
        """

        # common process
        if(self.input_wait_counter > 0):
            self.input_wait_counter -= 1

        path = VideoCtrl.VIDEO_PATH
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]

        if(self.cursor_pos + self.cursor_offset < len(files_dir)):  
            self.target_path = files_dir[self.cursor_pos + self.cursor_offset]

        # quit app
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # select video
        if pyxel.btn(pyxel.KEY_DOWN) and self.input_wait_counter == 0:
            self.input_wait_counter = VideoCtrl.INPUT_WAIT
            if(self.cursor_pos < VideoCtrl.MENU_MAX - 1 and
                self.cursor_pos + self.cursor_offset < len(files_dir) - 1):
                self.cursor_pos += 1
            elif(self.cursor_pos + self.cursor_offset < len(files_dir) - 1):
                self.cursor_offset += 1

        if pyxel.btn(pyxel.KEY_UP) and self.input_wait_counter == 0:
            self.input_wait_counter = VideoCtrl.INPUT_WAIT
            if(self.cursor_pos > 0):
                self.cursor_pos -= 1
            elif(self.cursor_offset > 0):
                self.cursor_offset -= 1

        # cut video
        if pyxel.btn(pyxel.KEY_C) and self.input_wait_counter == 0:
            self.input_wait_counter = VideoCtrl.INPUT_LONG_WAIT

            video_path = VideoCtrl.VIDEO_PATH + os.sep + self.target_path
            input_file = self.target_path + ".mp4"
            if os.path.exists(video_path):
                self.processing_file = self.target_path
                print("test1:" + video_path + "," + input_file)
                self.duration = get_movie_duration(video_path, input_file)
                print("test2:" + str(self.duration))
                movie_full_to_images(video_path, input_file, 1)

        # diff video
        if pyxel.btn(pyxel.KEY_D) and self.input_wait_counter == 0:
            self.input_wait_counter = VideoCtrl.INPUT_LONG_WAIT

            #ex. python diff_proc.py ./assets/sample1
            cmd = 'python diff_proc.py "' + \
                VideoCtrl.VIDEO_PATH + os.sep + self.target_path + '"'

            # asynchronous
            subprocess.Popen(shlex.split(cmd), cwd='./')

    def draw(self):
        # common process
        pyxel.cls(0)

        path = VideoCtrl.VIDEO_PATH
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]

        if(self.cursor_pos + self.cursor_offset < len(files_dir)):
            self.target_path = files_dir[self.cursor_pos + self.cursor_offset]

        # draw video list
        for index_y in range(VideoCtrl.MENU_MAX):
            if(index_y + self.cursor_offset < len(files_dir)):  
                pyxel.text(
                    VideoCtrl.VIDEO_LIST_OFFSET_X, 
                    VideoCtrl.VIDEO_LIST_OFFSET_Y + 7 * index_y, 
                    files_dir[index_y + self.cursor_offset], 
                    COLOR_LIGHTGREEN if 
                        self.cursor_pos == index_y 
                        else COLOR_GREEN)
        
        # draw up arrow
        if(self.cursor_offset > 0):
            pyxel.rect(0, 0, 1, 1, COLOR_GREEN)

        # draw down arrow
        if(self.cursor_offset + VideoCtrl.MENU_MAX < len(files_dir)):
            pyxel.rect(0, 56, 1, 57, COLOR_GREEN)

        # draw time line bar
        pyxel.rectb(
            0, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_Y, 
            VideoCtrl.SCREEN_WIDTH - 1, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_Y + 5 * 2 - 1, 
            COLOR_GREEN)

        jpeg_list = self.get_file(self.target_path, r'^(\d){6}\.jpg$') # nnnnnn.jpg
        if(self.duration > len(jpeg_list) and self.target_path == self.processing_file):
            line_max = self.duration
        elif(self.duration <= len(jpeg_list) and self.target_path == self.processing_file):
            line_max = len(jpeg_list)
            self.duration = 0
        else:
            line_max = len(jpeg_list)

        # draw files exist
        for jpeg_file in jpeg_list:
            file_index = int(jpeg_file[:6]) - 1
            pyxel.rect(
                (VideoCtrl.SCREEN_WIDTH - 1) * file_index / line_max,
                VideoCtrl.VIDEO_DETAIL_OFFSET_Y,
                (VideoCtrl.SCREEN_WIDTH - 1) * (file_index + 1) / line_max - 1,
                VideoCtrl.VIDEO_DETAIL_OFFSET_Y + 5 * 2 - 1,
                COLOR_GREEN)

        # draw diff
        for jpeg_file in jpeg_list:
            diff_file = 'diff' + jpeg_file[:-3] + 'json'
            if os.path.exists(VideoCtrl.VIDEO_PATH + os.sep +
                        self.target_path + os.sep + 
                        diff_file):
                try:
                    fp_input = open(
                        VideoCtrl.VIDEO_PATH + os.sep +
                        self.target_path + os.sep + 
                        diff_file, 'r')
                    input_json = json.load(fp_input)
                        
                    if jpeg_file in input_json.keys():
                        diff_percent = input_json[jpeg_file]['diff'] * 2 / input_json[jpeg_file]['full'] # *2!
                    else:
                        diff_percent = 0
                    file_index = int(jpeg_file[:6]) - 1
                    pyxel.rect(
                        (VideoCtrl.SCREEN_WIDTH - 1) * file_index / line_max,
                        VideoCtrl.VIDEO_DETAIL_OFFSET_Y + (5 * 2 - 1) * (1 - (diff_percent if diff_percent < 1 else 1)), 
                        (VideoCtrl.SCREEN_WIDTH - 1) * (file_index + 1) / line_max - 1, 
                        VideoCtrl.VIDEO_DETAIL_OFFSET_Y + 5 * 2 - 1, 
                        COLOR_LIGHTGREEN if diff_percent < 0.5 else COLOR_ORANGE)

                except json.decoder.JSONDecodeError:
                    pass

                except IOError:
                    pass

        # draw video detail
        disp = []

        disp += [
            "mp4:" + 
            ("ok" if(self.check_file(self.target_path, 'mp4$')) else "no")
            ]

        disp += [
            "jpg(" + 
            str(len(self.get_file(self.target_path, r'^(\d){6}\.jpg$'))) + # nnnnnn.jpg
            ")<c>:" + 
            ("ok" if(self.check_file(self.target_path, r'^(\d){6}\.jpg$')) else "no") # nnnnnn.jpg
            ]

        disp += [
            "diff(" +
            str(len(self.get_file(self.target_path, r'^diff(\d){6}\.json$'))) + # diffnnnnnn.jpg         
            ")<d>:" +
            ("ok" if(self.check_file(self.target_path, r'^diff(\d){6}\.json$')) else "no")
            ]

        disp += ["incnt:" + str(self.input_wait_counter)]

        disp += ["duration:" + str(self.duration)]

        self.disp_list(
            disp, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_X, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_Y + 5 * 2, 
            5)

    def disp_list(self, str_list, pos_x, pos_y, row_hight):
        for index in range(len(str_list)):
            pyxel.text(
                pos_x, 
                pos_y + row_hight * index,
                str_list[index],
                COLOR_GREEN
            )

    def check_file(self, path, reg):
        path = VideoCtrl.VIDEO_PATH + os.sep + path
        files = os.listdir(path)

        hasExt = False
        for file_str in files:
            if(re.findall(reg, file_str)):
                hasExt = True
        
        return hasExt

    def get_file(self, path, reg):
        path = VideoCtrl.VIDEO_PATH + os.sep + path
        files = os.listdir(path)

        file_list = []
        for file_str in files:
            if(re.findall(reg, file_str)):
                file_list += [file_str]
        
        return file_list

        


if __name__ == "__main__":
    VideoCtrl()
