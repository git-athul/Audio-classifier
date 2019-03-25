for i in os.listdir(directory):
    try:
        details = acoustid.identify_song(i)
        # Here, details is a new type
        details.name
        details.artist
        details.albums

        # Here details is a dictionary
        # details['name']
        # details['artist']
        # details['albums']
    except ValueError as e:
        print ("Couldn't identify {} ({})".format(i, e))
        
