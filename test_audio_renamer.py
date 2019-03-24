import unittest
from unittest import mock
import audio_renamer

class TestMp3Files(unittest.TestCase):
    @mock.patch('audio_renamer.os.listdir')
    def test_mp3files(self, mock_listdir):
        mock_listdir.return_value = ['a.mp3', 'b.mp3', 'c.mp3', 'd.txt']
        files = audio_renamer.mp3files('.')
        self.assertEqual(3, len(files))
        self.assertNotEqual(2, len(files))

def test_artists():
    data = [{'id': 'cc', 'name': 'Adele'}]
    rst = "Adele"
    assert audio_renamer.artists(data) == rst

    data = [{'joinphrase': ' & ', 'name': 'Skrillex'},
            {'joinphrase':' feat. ', 'name': 'Diplo'},
            {'name': 'Justin Bieber'}]
    rst = "Skrillex & Diplo feat. Justin Bieber"
    assert audio_renamer.artists(data) == rst


def test_suggestions_title_style():
    data = [{'title': 'Hello', 'artists': [{'name': 'Adele'}]},
            {'title': 'Hello (radio edit)', 'artists': [{'name': 'Adele'}]},
            {'title': 'Where Are Ü Now', 'artists':
             [{'joinphrase':' & ', 'name': 'Skrillex'},
              {'joinphrase': ' feat. ', 'name':'Diplo'},
            {'name': 'Justin Bieber'}]}, {'title': 'Hello', 'artists':
            [{'name': 'Adele'}]}, {'title': 'Cry Baby', 'artists':
            [{'name': 'Melanie Martinez'}]}]

    names = {0: 'Hello.mp3',
             1: 'Hello (radio edit).mp3',
             2: 'Where Are Ü Now.mp3',
             3: 'Hello.mp3'}

    printer = ['(0): Hello.mp3',
               '(1): Hello (radio edit).mp3',
               '(2): Where Are Ü Now.mp3',
               '(3): Hello.mp3', "(9): 'SKIP THIS FILE'"]
    with mock.patch('audio_renamer.automation', False):
        #No-automation
        assert audio_renamer.suggestions(data, True) == (names, printer)

    names = {0: 'Hello.mp3'}
    printer = ['(0): Hello.mp3', "(9): 'SKIP THIS FILE'"]

    with mock.patch('audio_renamer.automation', True):
        #Automation
        assert audio_renamer.suggestions(data, True) == (names, printer)


def test_suggestions_combo_style():
    data = [{'title': 'Hello', 'artists': [{'name': 'Adele'}]},
            {'title': 'Hello (radio edit)', 'artists': [{'name': 'Adele'}]},
            {'title': 'Where Are Ü Now', 'artists':
             [{'joinphrase':' & ', 'name': 'Skrillex'},
              {'joinphrase': ' feat. ', 'name':'Diplo'},
            {'name': 'Justin Bieber'}]}, {'title': 'Hello', 'artists':
            [{'name': 'Adele'}]}, {'title': 'Cry Baby', 'artists':
            [{'name': 'Melanie Martinez'}]}]
    
    names = {0: 'Adele - Hello.mp3',
             1: 'Adele - Hello (radio edit).mp3',
             2: 'Skrillex & Diplo feat. Justin Bieber - Where Are Ü Now.mp3',
             3: 'Adele - Hello.mp3'}

    printer = ['(0): Adele - Hello.mp3',
               '(1): Adele - Hello (radio edit).mp3',
               '(2): Skrillex & Diplo feat. Justin Bieber - Where Are Ü Now.mp3',
               '(3): Adele - Hello.mp3', "(9): 'SKIP THIS FILE'"]
    with mock.patch('audio_renamer.automation', False):
        #No-automation
        assert audio_renamer.suggestions(data, False) == (names, printer)

    names = {0: 'Adele - Hello.mp3'}
    printer = ['(0): Adele - Hello.mp3', "(9): 'SKIP THIS FILE'"]
    
    with mock.patch('audio_renamer.automation', True):
        #Automation
        assert audio_renamer.suggestions(data, False) == (names, printer)


def test_user_input():
    file_name = "fakename"
    options = {0 : "name0",
               1 : "name1",
               2 : "name2"}

    input_values = [0, 1, 2, 9]
    output = [("name0", "'fakename' RENAMED AS 'name0'"),
              ("name1", "'fakename' RENAMED AS 'name1'"),
              ("name2", "'fakename' RENAMED AS 'name2'"),
              (False, "Skipped 'fakename'")]

    def mock_input():
        return input_values.pop(0)
    for i, _ in enumerate(output):
        audio_renamer.getch.getch = mock_input
        with mock.patch('audio_renamer.automation', False):
            #No-automation
            assert audio_renamer.user_input(file_name, options) == output[i]

    with mock.patch('audio_renamer.automation', True):
        #Automation
        assert audio_renamer.user_input(file_name, options) == output[0]
