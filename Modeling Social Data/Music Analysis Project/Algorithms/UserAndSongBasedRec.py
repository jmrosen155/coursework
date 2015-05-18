from operator import itemgetter
import numpy as np
from collections import defaultdict

from apk import apk



def item_based_rec(user_to_song, song_to_user, N2, user_to_song_test):
    
    # Item-based similarity
    
    sim_songs = np.zeros([N2,N2])
    top_songs = {}
    
    
    alpha = 0.5
    # Gamma causes larger weights to be emphasized while dropping smaller weights to zero
    gamma = 1
    
    #Calculate similarity scores for all pairs of songs and get most similar songs to every song
    for song1 in song_to_user:
        top_songs[song1] = []
        for song2 in song_to_user:
            user1 = song_to_user[song1]
            user2 = song_to_user[song2]
            sim_songs[song1][song2] = float(len(set(user1).intersection(user2))) / (len(user1)**alpha * len(user2)**(1-alpha))
            sim_songs[song1][song2] = (sim_songs[song1][song2])**gamma
            top_songs[song1].append((song2, sim_songs[song1][song2]))
        top_songs[song1] = sorted(top_songs[song1], key = itemgetter(1), reverse = True)[0:500]
    
    #Find songs most similar to songs user listens to and recommend those songs
    recommend = {}       
    for user in user_to_song:
        songs = user_to_song[user]
        recommend[user] = []
        for song in songs:
            recommend[user] = recommend[user] + top_songs[song]
        testDict = defaultdict(float)
        for key, val in recommend[user]:
            testDict[key] += val
        recommend[user] = testDict.items()
        recommend[user] = sorted(recommend[user], key = itemgetter(1), reverse = True)
        recommend[user] = [x for x in recommend[user] if x[0] not in user_to_song[user]][0:500]                
        recommend[user] = [x[0] for x in recommend[user]]
    
    #Calculate how good of a prediction
    apk_sum = 0

    counter = 0
    for i in user_to_song_test:
        if i in recommend:
            apk_sum += apk(user_to_song_test[i],recommend[i])
            counter += 1
    
    map = apk_sum/counter
    return map
    
   
    

def user_based_rec(user_to_song, song_to_user, N1, user_to_song_test):
    
    sim_users = np.zeros([N1,N1])
    
    alpha = 0.5
    #Gamma causes larger weights to be emphasized while dropping smaller weights to zero
    gamma = 1
    
    #Find users most similar to each user
    for user1 in user_to_song:
        for user2 in user_to_song:
            song1 = user_to_song[user1]
            song2 = user_to_song[user2]
            sim_users[user1][user2] = float(len(set(song1).intersection(song2))) / (len(song1)**alpha * len(song2)**(1-alpha))
            sim_users[user1][user2] = (sim_users[user1][user2])**gamma            
    
    #For each user, find songs of most similar users and recommend those songs      
    recommend = {}
    for user1 in user_to_song:
        recommend[user1] = []
        for song in song_to_user:
            users = song_to_user[song]
            temp = 0
            for user2 in users:
                temp = temp + sim_users[user1][user2]
            recommend[user1].append((song, temp)) 
        recommend[user1] = sorted(recommend[user1], key = itemgetter(1), reverse = True)
        recommend[user1] = [x for x in recommend[user1] if x[0] not in user_to_song[user1]][0:500]        
        recommend[user1] = [x[0] for x in recommend[user1]]
    
    #Calculate how good of a prediction
    apk_sum = 0

    counter = 0
    for i in user_to_song_test:
        if i in recommend:
            apk_sum += apk(user_to_song_test[i],recommend[i])
            counter += 1
    
    map = apk_sum/counter
    return map


