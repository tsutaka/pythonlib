# ffmpeg.py
import sys          # for command line arguments
import subprocess   # for command executing
import shlex        # for escaping cmd

# before use, requires install ffmpeg and add path

def movie_to_images(path, input_file, start_seconds, end_seconds, interval):

    #ex. ffmpeg -i sample.mp4 -ss 0 -t 19 -r 1 -q:v 1 %06d.jpg
    cmd = "ffmpeg -i " + str(input_file) + " -ss " + str(start_seconds) + \
        " -t " + str(end_seconds) + " -r " + str(interval) + " -q:v 1 %06d.jpg"
    
    # asynchronous
    subprocess.Popen(shlex.split(cmd), cwd = str(path))

    return
    
def movie_full_to_images(path, input_file, interval):

    #ex. ffmpeg -i sample.mp4 -ss 0 -r 1 -q:v 1 %06d.jpg
    cmd = "ffmpeg -i " + str(input_file) + " -ss 0 -r " + str(interval) + " -q:v 1 %06d.jpg"

    # asynchronous
    subprocess.Popen(shlex.split(cmd), cwd = str(path))

    return

def get_movie_duration(path, input_file):

    #ex. ffprobe sample.mp4 -hide_banner -show_entries format=duration
    cmd = "ffprobe " + str(input_file) + " -hide_banner -show_entries format=duration"
    
    # synchronous
    proc = subprocess.Popen(shlex.split(cmd), cwd = str(path), \
               stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    res = proc.communicate()
    dur_pos = str(res[0]).find('duration')
    str_temp = str(res[0])[dur_pos:]
    end_pos = str_temp.find('.')

    return int(str_temp[len('duration='):end_pos])


if __name__ == "__main__":
    # execute only if run as a script
    # ex. python ffmpeg.py ./ test.mp4 0 10 1
    args = sys.argv
    
    if(len(args) != 6) :
        print("args not have 5 arg")
        exit()
    
    input_path = args[1]
    file_name = args[2]
    start_seconds = args[3]
    end_seconds = args[4]
    interval = args[5]

    print("input_path:", input_path)
    print("file_name:", file_name)
    print("start_seconds:", start_seconds)
    print("end_seconds:", end_seconds)
    print("interval:", interval)
    
    get_movie_duration(input_path, file_name)
    # movie_to_images(input_path, file_name, start_seconds, end_seconds, interval)
