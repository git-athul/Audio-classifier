import acoustid
import requests
from os import listdir
from os.path import join
from pydub import AudioSegment

def mp3files(path):
    "Returns mp3 files from the given directory."
    return [f for f in listdir(path) if ".mp3" in f]

# Able to fingerprint without this function
# def mp3_to_RAW(mp3, audiopath):
#     "Converts mp3file to RAW audio file"
#     mp3path = join(audiopath, mp3)
#     return AudioSegment.from_mp3(mp3path)

def process_file( file_name) :
    "process a file, given file_name and returns fingerprint of that file."
    (duration, fingerprint) = acoustid.fingerprint_file(file_name)
    return duration, fingerprint

if __name__ == "__main__":
    audio_path = "./audiodir"
    audio_list = mp3files(audio_path)
    dict_aud = {}
    for f in audio_list:
        dur, fingerprint = process_file(join(audio_path,f ))
        out = acoustid.lookup('2Shct5QtQi', fingerprint, dur)
        print(out)

