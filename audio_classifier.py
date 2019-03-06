"""
Renames mp3 files in selected directory.
Renaming is based on the information collected from acoustid web
service.
"""

import os
from os.path import join
import argparse as ap
import acoustid as ad
import config   #contains API-key

def call_parser():
    "Returns audio directory and style of renaming"
    parser = ap.ArgumentParser(description="""
    Renames mp3 files in selected directory.
    Renaming is based on the information collected from acoustid web
    service.
    """)
    parser.add_argument('mp3dir', action='store',
                        metavar='audio_path',
                        help='file-path of mp3 directory')

    parser.add_argument('--style', default=False,
                        type=bool, action='store', nargs='?',
                        help="""
                        If 'style' is False, renames will have
                        title of song.  If 'style' is True, renames
                        will be a combination of artists and title.
                        (default: False)
                        """)
    args = parser.parse_args()
    return args.mp3dir, args.style

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
    audio_path, combo_style = call_parser()
    audio_list = mp3files(audio_path)

    for name in audio_list:
        n_path = join(audio_path, name)
        rst = process_file(n_path)
        # print(rst)
        try:
            title = rst['results'][0]['recordings'][0]['title']
            if combo_style:
                artst = rst['results'][0]['recordings'][0]['artists'][0]['name']
                rename = artst + ' - ' + title + '.mp3'
            else:
                rename = title + '.mp3'
            dst = join(audio_path, rename)
            os.rename(n_path, dst)
            print("'{}' RENAMED AS '{}'".format(name, rename))
        except KeyError:
            print("No recording data found for '{}'".format(name))

if __name__ == "__main__":
    main()
