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
                        If 'style' is True, renames will have
                        title of song.  If 'style' is False, renames
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

def suggestions(rcd, style):
    "Returns top 4 name suggestions"
    names = {}
    for i, _ in enumerate(rcd):
        if i == 4:
            break
        title = rcd[i]['title']
        artst = ""
        if not style:
            artst = artists(rcd[i]['artists']) + ' - '
        names[i] = artst + title + '.mp3'

        print("({}): {}".format(i, names[i]))
    print("(9): 'SKIP THIS FILE'")
    return names

def artists(rcd_artst):
    "Returns artists of the song"
    pos = len(rcd_artst) -1
    artst = [rcd_artst[pos]['name']]
    while pos != 0:
        artst.append(rcd_artst[pos-1]['joinphrase'])
        artst.append(rcd_artst[pos-1]['name'])
        pos -= 1
    artst.reverse()
    return "".join(artst)


def main():
    "Renames the mp3 files based on the data from acoustid"
    audio_path, name_style = call_parser()
    audio_list = mp3files(audio_path)

    for name in audio_list:
        n_path = join(audio_path, name)
        rst = process_file(n_path)
        try:
            record = rst['results'][0]['recordings']
            print("Rename '{}' as".format(name))
            n_options = suggestions(record, name_style)
            choice = int(input('> '))
            if choice == 9:
                print("Skipped '{}'\n".format(name))
                continue
            else:
                rename = n_options[choice]

            dst = join(audio_path, rename)
            os.rename(n_path, dst)
            print("'{}' RENAMED AS '{}'\n".format(name, rename))
        except KeyError:
            print("No recording data found for '{}'\n".format(name))

if __name__ == "__main__":
    main()
