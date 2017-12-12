#!/usr/bin/python
# -*- coding: utf-8 -*-
import wave
import pyaudio
import time
from datetime import datetime

import file_io

def play_wav(wavfile):
    # WAVファイルを開く
    wr = wave.open(wavfile, "rb")

    # PyAudioのインスタンスを生成
    p = pyaudio.PyAudio()

    # 再生用のコールバック関数を定義
    def callback(in_data, frame_count, time_info, status):
        data = wr.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # Streamを生成
    stream = p.open(format=p.get_format_from_width(wr.getsampwidth()),
                    channels=wr.getnchannels(),
                    rate=wr.getframerate(),
                    output=True,
                    stream_callback=callback)

    # Streamをつかって再生開始
    stream.start_stream()
    base_time = datetime.now()

    #ファイルの読み取り
    ## ファイル形式
    # 00:00,xxxxx
    def str2sec(time_str):
        return int(time_str[0:2]) * 60 + int(time_str[3:5])

    time_list = file_io.read_file("./sample/","kashi.txt")
    tmp_list = []
    for time_str in time_list:
        time_temp, str_temp = time_str.split(',')
        tmp_list += [[str2sec(time_temp), str_temp]]
    time_list = tmp_list

    # 再生中はひとまず待っておきます
    count = 0
    while stream.is_active():
        now_time = datetime.now() - base_time
        if(count < len(time_list) and time_list[count][0] == now_time.seconds):
            print(time_list[count][1])
            count += 1

        time.sleep(0.1)

    # 再生が終わると、ストリームを停止・解放
    stream.stop_stream()
    stream.close()
    wr.close()

    # close PyAudio
    p.terminate()

if __name__ == '__main__':
    print(">start")
    play_wav("./sample/test.wav")
    print(">end")
