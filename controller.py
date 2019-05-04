import pyxel
import os # for handling directory
import re # for using regular expression

# internal import
from videolib.ffmpeg import movie_full_to_images

COLOR_GREEN = 3
COLOR_LIGHTGREEN = 11

class VideoCtrl:

    SCREEN_WIDTH = 255
    SCREEN_HEIGHT = 255

    VIDEO_LIST_OFFSET_X = 2
    VIDEO_LIST_OFFSET_Y = 2

    VIDEO_DETAIL_OFFSET_X = 2
    VIDEO_DETAIL_OFFSET_Y = 60

    MENU_MAX = 8
    INPUT_WAIT = 5
    INPUT_LONG_WAIT = 50

    VIDEO_PATH = "./assets"

    def __init__(self):
        pyxel.init(
            VideoCtrl.SCREEN_WIDTH, 
            VideoCtrl.SCREEN_HEIGHT, 
            caption="video controller")
            
        self.cursor_pos = 0
        self.cursor_offset = 0
        self.input_wait_counter = 0

        pyxel.run(self.update, self.draw)


    def update(self):
        # quit app
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # select video
        path = VideoCtrl.VIDEO_PATH
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]

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
            
        if(self.input_wait_counter > 0):
            self.input_wait_counter -= 1
        
        # cut video
        if pyxel.btn(pyxel.KEY_C) and self.input_wait_counter == 0:
            self.input_wait_counter = VideoCtrl.INPUT_LONG_WAIT


    def draw(self):
        pyxel.cls(0)

        # draw video list
        path = VideoCtrl.VIDEO_PATH
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        
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

        # draw video detail
        pyxel.rectb(
            1, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_Y, 
            VideoCtrl.SCREEN_WIDTH - 1, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_Y + 5 * 2 - 1, 
            COLOR_GREEN)
        
        disp = []

        if(self.cursor_pos + self.cursor_offset < len(files_dir)):  
            target_path = files_dir[self.cursor_pos + self.cursor_offset]

        disp += [
            "mp4:" + 
            ("ok" if(self.check_file(target_path, 'mp4$')) else "no")
            ]

        disp += [
            "jpg:" + 
            ("ok" if(self.check_file(target_path, 'jpg$')) else "no")
            ]

        disp += [
            "diff:" + 
            ("ok" if(self.check_file(target_path, '^diff')) else "no")
            ]

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
