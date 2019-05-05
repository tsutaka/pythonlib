import pyxel
import os # for handling directory
import re # for using regular expression

# internal import
from videolib.ffmpeg import movie_full_to_images
from videolib.ffmpeg import get_movie_duration

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
    INPUT_LONG_WAIT = 10

    VIDEO_PATH = "./assets"

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

        pyxel.run(self.update, self.draw)


    def update(self):

        # common process
        if(self.input_wait_counter > 0):
            self.input_wait_counter -= 1
            
        path = VideoCtrl.VIDEO_PATH
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
    
        if(self.cursor_pos + self.cursor_offset < len(files_dir)):  
            target_path = files_dir[self.cursor_pos + self.cursor_offset]

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
            
        # cut video
        if pyxel.btn(pyxel.KEY_C) and self.input_wait_counter == 0:
            self.input_wait_counter = VideoCtrl.INPUT_LONG_WAIT

            video_path = VideoCtrl.VIDEO_PATH + os.sep + target_path
            input_file = target_path + ".mp4"
            if(os.path.exists(video_path)):
                self.processing_file = target_path
                self.duration = get_movie_duration(video_path, input_file)
                movie_full_to_images(video_path, input_file, 1)

    def draw(self):
        # common process
        pyxel.cls(0)

        path = VideoCtrl.VIDEO_PATH
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]

        if(self.cursor_pos + self.cursor_offset < len(files_dir)):  
            target_path = files_dir[self.cursor_pos + self.cursor_offset]
        
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

        jpeg_list = self.get_file(target_path, r'^(\d){6}\.jpg$') # nnnnnn.jpg
        if(self.duration > len(jpeg_list) and target_path == self.processing_file):
            line_max = self.duration
        elif(self.duration <= len(jpeg_list) and target_path == self.processing_file):
            line_max = len(jpeg_list)
            self.duration = 0
        else:
            line_max = len(jpeg_list)

        for jpeg_file in jpeg_list:
            file_index = int(jpeg_file[:6]) - 1
            pyxel.rect(
                (VideoCtrl.SCREEN_WIDTH - 1) * file_index / line_max, 
                VideoCtrl.VIDEO_DETAIL_OFFSET_Y, 
                (VideoCtrl.SCREEN_WIDTH - 1) * (file_index + 1) / line_max - 1, 
                VideoCtrl.VIDEO_DETAIL_OFFSET_Y + 5 * 2 - 1, 
                COLOR_GREEN)

        
        # draw video detail

        disp = []

        disp += [
            "mp4:" + 
            ("ok" if(self.check_file(target_path, 'mp4$')) else "no")
            ]

        disp += [
            "jpg(" + 
            str(len(self.get_file(target_path, r'^(\d){6}\.jpg$'))) + # nnnnnn.jpg
            ")<c>:" + 
            ("ok" if(self.check_file(target_path, r'^(\d){6}\.jpg$')) else "no") # nnnnnn.jpg
            ]

        disp += [
            "diff(" + 
            str(len(self.get_file(target_path, r'^diff(\d){6}\.jpg$'))) + # diffnnnnnn.jpg            
            "):" + 
            ("ok" if(self.check_file(target_path, r'^diff(\d){6}\.jpg$')) else "no")
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
