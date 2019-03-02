from os import listdir

def mp3files(path):
    "Returns mp3 files from the given directory"
    return [f for f in listdir(path) if ".mp3" in f]

if __name__ == "__main__":
    audiopath = "./audiodir"
    print(mp3files(audiopath))
