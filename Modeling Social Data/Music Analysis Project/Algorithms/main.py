import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib
import random
import pandas.io.sql as psql
import sqlite3 as sqlite
from collections import OrderedDict

from matrix_factorization import MF
from matrix_factorization import MF2

from popularity_baseline import popularity_baseline

from artist_based import artist_based

from UserAndSongBasedRec import user_based_rec
from UserAndSongBasedRec import item_based_rec

from NMF import NMF
from k_means import rawkmeans

matplotlib.style.use('ggplot')

### Data Loading Section
# load observation data
# kaggle_visible_evaluation_triplets.txt is available at https://www.kaggle.com/c/msdchallenge/data
f = open("kaggle_visible_evaluation_triplets.txt", 'rb')
eval = pd.read_csv(f,sep='\t',header = None, names = ['user_id','sid','plays'])

# count number of songs per user and subset
userhist = eval.groupby('user_id').count()
userhist = pd.DataFrame(userhist).reset_index()
usersub = userhist[userhist['plays']>27]

# count number of users per song and subset
songhist = eval.groupby('sid').count()
songhist = pd.DataFrame(songhist).reset_index()
songsub = songhist[songhist['plays']>22]

# subset the whole dataset
sub = eval[eval['sid'].isin(songsub['sid'])]
sub = sub[sub['user_id'].isin(usersub['user_id'])]

# sampling/splitting the dataset
sample = random.sample(sub.index, int(sub.shape[0]*0.2))
trainsub = sub.copy()
trainsub.ix[trainsub.index.isin(sample),'plays'] = 0
testsub = sub.copy()
testsub.ix[~trainsub.index.isin(sample),'plays'] = 0

# generating a matrix out of dataframe
trainpivot = trainsub.pivot(index='user_id',columns='sid', values='plays')
# creating the mapping of user index to user id
user_index = pd.DataFrame(trainpivot.index).reset_index()
user_index.columns = [['user_index','user_id']]
trainsub = pd.merge(trainsub, user_index, on='user_id')
testsub = pd.merge(testsub, user_index, on='user_id')
# creating the mapping of song index to song id
song_index = pd.DataFrame(trainpivot.columns).reset_index()
song_index.columns = [['song_index','sid']]
trainsub = pd.merge(trainsub, song_index, on='sid')
testsub = pd.merge(testsub, song_index, on='sid')

# Generating the default M_train and M_test matrices
M_train = trainpivot.as_matrix()
M_train = np.nan_to_num(M_train)

testpivot = testsub.pivot(index='user_id',columns='sid', values='plays')
M_test = testpivot.as_matrix()
M_test = np.nan_to_num(M_test)

# creating omegau_test
testplays = testsub[testsub.plays>0]
test_usergroup = testsub[testsub.plays>0].groupby('user_index')
omegau_test = {}
for i in list(set(testplays.user_index.values)):
    omegau_test[i] = list(test_usergroup.get_group(i)['song_index'])
# creating omegau_train
trainplays = trainsub[trainsub.plays>0]
train_usergroup = trainplays.groupby('user_index')
omegau_train = {}
for i in list(set(trainplays.user_index.values)):
    omegau_train[i] = list(train_usergroup.get_group(i)['song_index'])
# creating omegav_train
train_songgroup = trainplays.groupby('song_index')
omegav_train = {}
for i in list(set(trainplays.song_index.values)):
    omegav_train[i] = list(train_songgroup.get_group(i)['user_index'])   
    
# creating tuple lists
omega = [tuple(x) for x in trainsub[trainsub.plays>0][['user_index','song_index']].values]
omega_test = [tuple(x) for x in testsub[trainsub.plays>0][['user_index','song_index']].values]


### Data Exploratory and Plotting Section
def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

#cumulative sum for plays vs songs
songplaycsum = songhist.sort('plays')
songplaycsum['plays'] = songplaycsum['plays'].cumsum()
songplaycsum['plays'] = songplaycsum['plays']/songplaycsum['plays'].max()
songplaycsum = songplaycsum.reset_index(drop=True).reset_index()
songplaycsum.plot('index', 'plays')
plt.legend().set_visible(False)
plt.title("Cumulative Sum of Number of Users for each Song")
plt.ylabel("Perecentage of Users")
plt.xlabel("Number of Songs")
formatter = FuncFormatter(to_percent)
plt.gca().yaxis.set_major_formatter(formatter)
plt.legend().set_visible(False)
plt.show()

print eval.groupby('user_id').count().describe()['plays']
print eval.groupby('sid').count().describe()['plays']

### Popularity Baseline Section
popbase = popularity_baseline(trainsub,omegau_train,omegau_test)
print "The popularity baseline MAP based on counts is " + str(popbase[0]) + ' and based on plays is ' + str(popbase[1])

### Artist-based Popularity Baseline Section

# Load track metadata to get artist_id
# http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/track_metadata.db
con = sqlite.connect("track_metadata.db")
with con:
    sql = "SELECT * FROM songs"
    track_metadata = psql.read_sql(sql, con)
con.close()

# Renaming columns to match other dataframes
track_metadata=track_metadata.rename(columns = {'track_id':'tid'})
track_metadata=track_metadata.rename(columns = {'song_id':'sid'})
# Subsetting track_metadata to only have songs on the song_index on the subset data
track_metadata=pd.merge(track_metadata,song_index, on='sid')

# Group by songs and sum the amount of plays, then sort in descending amount of plays
eval_songs = eval.groupby('sid').sum().reset_index().sort('plays',ascending=False)[['sid','plays']]
# Subset songs to subset while including track metadata
eval_songmeta = pd.merge(eval_songs, track_metadata, on='sid')

# Generate a list of songs for each artist_id in the order of decreasing popularity of songs
artist_group = eval_songmeta.groupby('artist_id')
artist_songdict = {}
for i in list(set(eval_songmeta.artist_id.values)):
    artist_songdict[i] = list(OrderedDict.fromkeys(artist_group.get_group(i)['song_index']))

# As one song_id can map to multiple track_id, drop all the duplicate song_ids, this is an assumption but the mapping of song_id to artist_id should be unique
track_sid = track_metadata.drop_duplicates('sid')
# Subsetting the user information based on the training set
eval_user = pd.merge(trainsub[trainsub.plays>0], track_sid, on='sid')
# Generate a list of artist_id for each user_index in order of decreasing amount of plays
user_songs = eval_user.groupby(['user_index','artist_id']).sum().reset_index()[['user_index','artist_id','plays']]
user_songs = user_songs.sort(['user_index','plays'], ascending=False)[['user_index','artist_id','plays']]

# Generate a list of song indexes in decreasing order of plays
popularsonglist = list(eval_songmeta.song_index.values)

# Run the algorithm and print the result
artist_map = artist_based(user_songs, artist_songdict, popularsonglist, omegau_test, omegau_train)
print "The MAP of artist-based popularity baseline is " + str(artist_map)



### PMF Section
# Processing M_train, row normalization, column normalization, and tfidf
rowsum = np.sum(M_train,axis=1).reshape((-1,1))
rowsum[rowsum == 0] = 1E-16
M_train_rownorm = M_train/rowsum

colsum = np.sum(M_train,axis=0).reshape((1,-1))
colsum[colsum == 0] = 1E-16
M_train_colnorm = M_train/colsum

idftrain = trainsub.copy()
idftrain.plays = 1
idf_train = idftrain.pivot(index='user_id',columns='sid', values='plays').as_matrix()
idf_train = np.nan_to_num(idf_train)
colsum = np.sum(idf_train,axis=0)
idf = np.log10(idf_train.shape[0]/colsum)
M_train_tfidf = M_train_rownorm*idf

M_train_binary = M_train.copy()
M_train_binary[M_train_binary != 0] = 1

# First PMF plot
MAP, L =  MF(M_train, 1.0, omega, omega_test, omegau_train, omegau_test, 80, 100)

plt.subplot(1,2,1)
plt.plot([0] + range(4,100,5), MAP)
plt.xlabel('Iterations')
plt.ylabel('MAP')
plt.title('MAP across iterations for default PMF')
plt.subplot(1,2,2)
plt.plot(L)
plt.xlabel('Iterations')
plt.ylabel('Log joint likelihood')
plt.title('Log joint likelihood across iterations for default PMF')
plt.show()

# Second PMF plot
plotdata = []

iter = 30
for var in [100, 10, 1, 0.1, 0.01, 0.001]:
    for d in [10, 20, 40, 80]:
        plotdata.append([0,'Default',var,d,MF2(M_train, var, omegau_train, omegau_test, d, iter)])
        plotdata.append([1,'Row-norm',var,d,MF2(M_train_rownorm, var, omegau_train, omegau_test, d, iter)])
        plotdata.append([2,'Col-norm',var,d,MF2(M_train_colnorm, var, omegau_train, omegau_test, d, iter)])
        plotdata.append([3,'Binary',var,d,MF2(M_train_binary, var, omegau_train, omegau_test, d, iter)])
        plotdata.append([4,'TF-IDF',var,d,MF2(M_train_tfidf, var, omegau_train, omegau_test, d, iter)])
            
plotdata = pd.DataFrame(plotdata,columns=['method','methodname','variance','d','MAP'])

plotdata['logvar'] = np.log10(plotdata['variance'])

groups = plotdata.sort(['d','method']).groupby('d')

n=1
for name, group in groups:
    groups2 = group.groupby('method')
    plt.subplot(2,2,n)
    n += 1
    for name2, group2 in groups2:
        plt.plot(group2.logvar, group2.MAP, label=group2.iloc[0].methodname)
        plt.title('rank d = ' + str(name))
        plt.xlabel('Log10-Variance')
        plt.ylabel('MAP')
        plt.ylim([0,0.02])
        
plt.legend(bbox_to_anchor=[-0.1, 2.3], loc='center', ncol=5)
plt.suptitle("PMF over different hyper-parameters and scaling methods", fontsize = 20)
plt.show()


### Item and user-based section
#Call item-based recommendation function
item_based_map = item_based_rec(omegau_train, omegav_train, np.shape(M_train)[1], omegau_test)
print item_based_map

#Call user-based recommendation fucntion
user_based_map = user_based_rec(omegau_train, omegav_train, np.shape(M_train)[0], omegau_test)
print user_based_map


### K-Means section
kmeans_map = rawkmeans(M_train, omegau_train, omegau_test, omegav_train, ncl=10)
print kmeans_map

### NMF section
nmf_map = NMF(M_train, omegau_train, omegau_test, iter=20, rank=25)
print nmf_map
