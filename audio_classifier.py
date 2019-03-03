import acoustid
from os import listdir
from os.path import join
from pydub import AudioSegment

def mp3files(path):
    "Returns mp3 files from the given directory"
    return [f for f in listdir(path) if ".mp3" in f]

def mp3_to_RAW(mp3, audiopath):
    "Converts mp3file to RAW audio file"
    mp3path = join(audiopath, mp3)
    return AudioSegment.from_mp3(mp3path)

if __name__ == "__main__":
    audio_path = "./audiodir"
    audio_list = mp3files(audio_path)
    for f in audio_list:
        mp3_to_RAW(f, audio_path)
        # print(mp3_to_RAW(f, audio_path))
