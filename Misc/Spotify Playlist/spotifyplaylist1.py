# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 11:32:55 2015

@author: Jordan Rosenblum
"""

import spotipy
import spotipy.util as util
import webbrowser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Setting up Spotify API and getting token
scope = 'playlist-modify-public'
#username = '12174691773'
username = raw_input("\nPlease enter your Spotify username: ") 
#Make sure username is valid and matches current user
try:
    token = util.prompt_for_user_token(username, scope)     
    spotify = spotipy.Spotify(auth = token) 
    if spotify.me()['id'] != username:
        raise Exception("Must enter your own username")
except:
    print ("\nInvalid username or token. Remember you must enter your own username. Please try again...\n")        
    sys.exit()

#Global variables to keep track of Spotify track ids and names
global songdict
songdict = {}
global tracks
tracks = []

#Message/Poem input
def processInput():
    message = raw_input("\nPlease enter a short message or poem to be converted to a playlist: ") 
    if message == '':
        print ("\nInvalid Entry. Please try again...\n")        
        sys.exit()
    #message = message.encode('utf8')    
    sys.stdout.write("\nProcessing... You will be directed to your playlist in a moment...\n")
    sys.stdout.flush()
    return message

#Search to see if a given input is the title of a song
def search(track):
    spotify = spotipy.Spotify()
    results = spotify.search(q='track:' + track, type='track', limit=10)
    if results['tracks']['items'] == []:
        return 'NA', 'NA'
    else:
        for i in xrange(0, len(results['tracks']['items'])):
            if (track.lower() == str(results['tracks']['items'][i]['name']).lower().translate(None, ",;:.'?")):
                trackid = str(results['tracks']['items'][i]['id'])
                trackname = str(results['tracks']['items'][i]['name'])  
                if trackid not in tracks:
                    return trackid, trackname
        return 'NA', 'NA'

#Algorithm to break up message into segments which are song titles
def breakup(words, start, end, maxsonglength = 6):
    if end > start + maxsonglength:
        end = start + maxsonglength
    if start < end:
        song = ' '.join(words[start:end])
        trackid, trackname = search(song)
        if trackid == 'NA':
            if start == end - 1:
                breakup(words, end, len(words))
            else: 
                breakup(words, start, end - 1)
        else:
            songdict[trackid] = trackname
            tracks.append(trackid)
            breakup(words, end, len(words))
                     
#Create a Spotify playlist
def createPlaylist(playlistname):
    create = spotipy.Spotify(auth=token)
    playlist = create.user_playlist_create(username, playlistname)
    playlistid = str(playlist['id'])
    return playlist, playlistid

#Add tracks from segmented message to Spotify playlist        
def addTracks(playlistid):
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    sp.user_playlist_add_tracks(username, playlistid, tracks)

def main():
    #Get message from user and name the playlist
    message = processInput()
    playlistname = ' '.join(message.split()[0:10])

    #Remove certain punctuation and break up message into individual words
    message = message.translate(None, ",;:.'?")
    words = message.split()

    #See if entire message is a song title and then recursively
    #call function until entire string is segmented into song titles
    breakup(words, 0, len(words))  
    
    #Prevent against creating an empty playlist    
    if tracks == []:
        print ("\nEnter at least one valid track name. Please try again...\n")        
        sys.exit()

    #Create a Spotify playlist
    playlist, playlistid = createPlaylist(playlistname)

    #Add tracks from segmented message to Spotify playlist
    addTracks(playlistid)

    #Open url of playlist in default browser
    url = playlist['external_urls']['spotify']
    webbrowser.open_new(url)
    
if __name__ == "__main__":
    main()






#Sample inputs
#message = "blahhhhhhh since you been gone blahhhhh wasted"
#message = "The telephone never rings. Still you pick it up, smile into the static, the breath of those you've loved; long dead."
#message = "if i can't let it go out of my mind"
