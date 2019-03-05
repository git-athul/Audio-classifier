import os
from os.path import join
import acoustid as ad
import config   #contains API-key

def mp3files(path):
    "Returns mp3 files from the given directory."
    return [f for f in os.listdir(path) if ".mp3" in f]

def process_file(file_name):
    "process a file and returns information about the audio."
    (duration, fingerprint) = ad.fingerprint_file(file_name)
    info = ad.lookup(config.apikey, fingerprint, duration)
    return info

def main():
    "Renames the mp3 files based on the data from acoustid"
    audio_path = "./audiodir"
    audio_list = mp3files(audio_path)

    for f in audio_list:
        f_path = join(audio_path, f)
        rst = process_file(f_path)
        # print(rst)
        try:
            title = rst['results'][0]['recordings'][0]['title']
            artst = rst['results'][0]['recordings'][0]['artists'][0]['name']
            dst = join(audio_path, artst + ' - ' + title + '.mp3')
            os.rename(f_path, dst)
            print("{}\n RENAMED AS\n{} \n".format(f_path, dst))
        except KeyError:
            print("No recording data found\n")

if __name__ == "__main__":
    main()
