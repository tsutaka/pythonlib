import wave
import pyaudio
import time
from datetime import datetime

import file_io

def play_wav(wavfile):
    # open wav file
    wr = wave.open(wavfile, "rb")

    # get instance of PyAudio
    p = pyaudio.PyAudio()

    # definition the callback function for playing
    def callback(in_data, frame_count, time_info, status):
        data = wr.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # create stream
    stream = p.open(format=p.get_format_from_width(wr.getsampwidth()),
                    channels=wr.getnchannels(),
                    rate=wr.getframerate(),
                    output=True,
                    stream_callback=callback)

    # start with stream
    stream.start_stream()
    base_time = datetime.now()

    # read file 
    ## file format
    # 00:00,xxxxx
    def str2sec(time_str):
        return int(time_str[0:2]) * 60 + int(time_str[3:5])

    time_list = file_io.read_file("./sample/","kashi.txt")
    tmp_list = []
    for time_str in time_list:
        time_temp, str_temp = time_str.split(',')
        tmp_list += [[str2sec(time_temp), str_temp]]
    time_list = tmp_list

    # wait while playing
    count = 0
    while stream.is_active():
        now_time = datetime.now() - base_time
        if(count < len(time_list) and time_list[count][0] == now_time.seconds):
            print(time_list[count][1])
            count += 1

        time.sleep(0.1)

    # when finished playing, stop stream and release
    stream.stop_stream()
    stream.close()
    wr.close()

    # close PyAudio
    p.terminate()

if __name__ == '__main__':
    print(">start")
    play_wav("./sample/test.wav")
    print(">end")
