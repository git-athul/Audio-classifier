import audio_renamer

def test_mp3files():
    rst = ["2.mp3", "Adele - Hello.mp3"]
    assert audio_renamer.mp3files('./test_data/test_mp3') == rst
