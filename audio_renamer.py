"""
Renames mp3 files in selected directory.
Renaming is based on the information collected from acoustid web
service.
"""

import os
from os.path import join
import argparse as ap
import acoustid as ad
import getch

automation = None #This is a global variable and used for mock.patch in test

def load_apikey():
    with open(".apikey") as f:
        apikey = f.read().strip()
        if apikey == "XXXXX":
            raise Exception("You haven't configured the API key. Please read Readme")
    return apikey

def call_parser():  # pragma: no cover
    "Returns audio directory and style of renaming"
    parser = ap.ArgumentParser(description="""
    Renames mp3 files in a selected directory based on the data from acoustid web
    service.
    """)
    parser.add_argument('mp3dir', action='store',
                        metavar='audio_path',
                        help='file-path of the mp3 directory')

    parser.add_argument('-n','--no-auto', action='store_false',
                        dest="auto", default=True,
                        help="""
                        If '--no-auto' is used, asks user the suggestions
                        for the renaming. Else, renames all songs with first choice.
                        """)
                        
    parser.add_argument('-t','--title-style', default=False,
                        dest="style", action='store_true',
                        help="""
                        If '--title-style' is used, renames will have
                        titles of the song. Else, renames will be a
                        combination of artists and title.
                        """)
    args = parser.parse_args()
    return args.mp3dir, args.auto, args.style

def mp3files(path):
    "Returns mp3 files from the given directory."
    return [f for f in os.listdir(path) if ".mp3" in f]


def process_file(file_name):
    "process a file and returns information about the audio."
    (duration, fingerprint) = ad.fingerprint_file(file_name)
    return ad.lookup(apikey, fingerprint, duration)


def suggestions(rcd, style):
    "Returns top 4 name suggestions"
    names = {}
    printer = []
    for i, _ in enumerate(rcd):
        if i == 4:
            break
        title = rcd[i]['title']
        artst = ""
        if not style:
            artst = artists(rcd[i]['artists']) + ' - '
        names[i] = artst + title + '.mp3'
        printer.append("({}): {}".format(i, names[i]))

        if automation:
            break

    printer.append("(9): 'SKIP THIS FILE'")
    return names, printer

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

def user_input(file_name, options):
    "Asks for user input"
    if not automation:
        choice = int(getch.getch())
        if choice == 9:
            newname = False
            printer = "Skipped '{}'".format(file_name)
        else:
            newname = options[choice]
            printer = "'{}' RENAMED AS '{}'".format(file_name, newname)
    else:
        newname = options[0]
        printer = "'{}' RENAMED AS '{}'".format(file_name, newname)
        
    return newname, printer


def main():
    "Renames the mp3 files based on the data from acoustid"
    global apikey
    apikey = load_apikey()

    global automation
    audio_path, automation, name_style = call_parser()
    audio_list = mp3files(audio_path)

    for name in audio_list:
        n_path = join(audio_path, name)
        rst = process_file(n_path)
        try:
            if rst['error']:
                print("Invalid API key")
                break
        except KeyError:
            pass
        try:
            record = rst['results'][0]['recordings']
            n_options, print_sugg = suggestions(record, name_style)
            if not automation:
                print("\nRename '{}' as".format(name))
                print("\n".join(print_sugg))
            rename, print_action = user_input(name, n_options)
            if rename:
                dst = join(audio_path, rename)
                os.rename(n_path, dst)
            print(print_action)
        except KeyError:
            if not automation:
                print('')
            print("No recording data found for '{}'".format(name))

if __name__ == "__main__":
    main()
