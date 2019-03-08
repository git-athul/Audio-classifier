import audio_renamer

def test_mp3files():
    rst = ["2.mp3", "Adele - Hello.mp3"]
    assert audio_renamer.mp3files('./test_data') == rst

def test_process_file():
    # Fails: if API-key is missing or
    # if recording data is updated
    mp3file = './test_data/2.mp3'
    with open('./test_data/1.songdata')as f:
        rst = f.readline()
    assert str(audio_renamer.process_file(mp3file)) == rst[:-1]

def test_artists():
    data = [{'id': 'cc', 'name': 'Adele'}]
    rst = "Adele"
    assert audio_renamer.artists(data) == rst

    data = [{'joinphrase': ' & ', 'name': 'Skrillex'}, {'joinphrase':
            ' feat. ', 'name': 'Diplo'}, {'name': 'Justin Bieber'}]
    rst ="Skrillex & Diplo feat. Justin Bieber"
    assert audio_renamer.artists(data) == rst

def test_suggestions():
    data = [{'title': 'Hello', 'artists': [{'name': 'Adele'}]},
            {'title': 'Hello (radio edit)', 'artists': [{'name': 'Adele'}]},
            {'title': 'Where Are Ü Now', 'artists': [{'joinphrase':' & ',
            'name': 'Skrillex'}, {'joinphrase': ' feat. ','name':'Diplo'},
            {'name': 'Justin Bieber'}]}, {'title': 'Hello', 'artists':
            [{'name': 'Adele'}]}, {'title': 'Cry Baby', 'artists': [{'name': 
            'Melanie Martinez'}]}]

    names = {0: 'Hello.mp3',
             1: 'Hello (radio edit).mp3',
             2: 'Where Are Ü Now.mp3',
             3: 'Hello.mp3'}
    
    printer = ['(0): Hello.mp3',
               '(1): Hello (radio edit).mp3',
               '(2): Where Are Ü Now.mp3',
               '(3): Hello.mp3', "(9): 'SKIP THIS FILE'"]
    assert audio_renamer.suggestions(data, True) == (names, printer)

    names = {0: 'Adele - Hello.mp3',
             1: 'Adele - Hello (radio edit).mp3',
             2: 'Skrillex & Diplo feat. Justin Bieber - Where Are Ü Now.mp3',
             3: 'Adele - Hello.mp3'}
    
    printer = ['(0): Adele - Hello.mp3',
               '(1): Adele - Hello (radio edit).mp3',
               '(2): Skrillex & Diplo feat. Justin Bieber - Where Are Ü Now.mp3',
               '(3): Adele - Hello.mp3', "(9): 'SKIP THIS FILE'"]
    assert audio_renamer.suggestions(data, False) == (names, printer)
    

