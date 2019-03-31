# ffmpeg.py
import sys          # for command line arguments
import subprocess   # for command executing

# before use, requires install ffmpeg and add path

def movie_to_images(input_path, start_seconds, end_seconds, interval):

    #ex. ffmpeg -i sample_movie.mp4 -ss 0 -t 19 -r 1 -q:v 1 %06d.jpg
    cmd = "ffmpeg -i " + input_path + " -ss " + start_seconds + \
        " -t " + end_seconds + " -r " + interval + " -q:v 1 %06d.jpg"
    subprocess.call(cmd)

    return


if __name__ == "__main__":
    # execute only if run as a script
    # ex. python ffmpeg.py test.mp4 0 10 1
    args = sys.argv
    input_path = args[1]
    start_seconds = args[2]
    end_seconds = args[3]
    interval = args[4]
    if(len(args) != 5) :
        print("args not have 4 arg")

    print("input_path:", input_path)
    print("start_seconds:", start_seconds)
    print("end_seconds:", end_seconds)
    print("interval:", interval)
    
    movie_to_images(input_path, start_seconds, end_seconds, interval)