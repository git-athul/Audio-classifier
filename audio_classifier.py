import acoustid
import config   #contains API-key
from os import listdir
from os.path import join

def mp3files(path):
    "Returns mp3 files from the given directory."
    return [f for f in listdir(path) if ".mp3" in f]

def process_file( file_name) :
    "process a file and returns fingerprint and duration."
    (duration, fingerprint) = acoustid.fingerprint_file(file_name)
    return duration, fingerprint

if __name__ == "__main__":
    audio_path = "./audiodir"
    audio_list = mp3files(audio_path)
    for f in audio_list:
        dur, fp = process_file(join(audio_path,f ))
        out = acoustid.lookup(config.apikey, fp, dur)
        print(out)

