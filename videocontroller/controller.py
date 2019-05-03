import pyxel
import os # for handling directory

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
    INPUT_WAIT = 10

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
        path = "./assets"
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]

        if pyxel.btn(pyxel.KEY_DOWN) and self.input_wait_counter == 0:
            self.input_wait_counter = VideoCtrl.INPUT_WAIT
            if(self.cursor_pos < VideoCtrl.MENU_MAX - 1):
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

    def draw(self):
        pyxel.cls(0)

        # draw video list
        path = "./assets"
        files = os.listdir(path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        
        for index_y in range(len(files_dir)):
            if index_y >= 8:
                break    
            pyxel.text(
                VideoCtrl.VIDEO_LIST_OFFSET_X, 
                VideoCtrl.VIDEO_LIST_OFFSET_Y + 7 * index_y, 
                files_dir[index_y + self.cursor_offset], 
                COLOR_LIGHTGREEN if 
                    self.cursor_pos == index_y 
                    else COLOR_GREEN)

        # draw video detail
        pyxel.rect(
            0, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_Y, 
            VideoCtrl.SCREEN_WIDTH, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_Y + 1, 
            COLOR_GREEN)
        
        disp = []
        disp += ["mp4:"]
        disp += ["cursor_pos:" + str(self.cursor_pos)]
        disp += ["cursor_offset:" + str(self.cursor_offset)]
        disp += ["select_path:" + files_dir[self.cursor_pos + self.cursor_offset]]

        self.disp_list(
            disp, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_X, 
            VideoCtrl.VIDEO_DETAIL_OFFSET_Y + 5, 
            5)
            
    def disp_list(self, str_list, pos_x, pos_y, row_hight):
        for index in range(len(str_list)):
            pyxel.text(
                pos_x, 
                pos_y + row_hight * index,
                str_list[index],
                COLOR_GREEN
            )


if __name__ == "__main__":
    VideoCtrl()
