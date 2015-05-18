# Code to load up data from the various datasets available as required

import sqlite3 as sqlite
import pandas as pd
import pandas.io.sql as psql

# http://www.kaggle.com/c/msdchallenge/data
f = open("kaggle_visible_evaluation_triplets.txt", 'rb')
eval = pd.read_csv(f,sep='\t',header = None, names = ['user_id','sid','plays'])

# http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_tracks.txt
f = open("unique_tracks.txt", 'rb')
unique_tracks = pd.read_csv(f,sep='<SEP>', header = None, names = ['tid', 'sid', 'artist_name', 'song_title'])

# http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_artists.txt
f = open("unique_artists.txt", 'rb')
unique_artists = pd.read_csv(f,sep='<SEP>',header = None, names = ['artist_id', 'artist_mbid', 'tid', 'artist_name'])

# http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/tracks_per_year.txt
f = open("tracks_per_year.txt", 'rb')
tracks_per_year = pd.read_csv(f,sep='<SEP>', header = None, names =['year','tid', 'artist_name', 'song_title'])

# http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/artist_location.txt
f = open("unique_location.txt", 'rb')
artist_location = pd.read_csv(f,sep='<SEP>', header = None, names = ['artist_id', 'latitude', 'longitude', 'artist_name', 'location'])

# http://www.ee.columbia.edu/~thierry/artist_similarity.db
con = sqlite.connect("artist_similarity.db")
with con:
    sql = "SELECT * FROM similarity"
    artist_sim = psql.read_sql(sql, con)
con.close()

# http://www.ee.columbia.edu/~thierry/artist_term.db
con = sqlite.connect("artist_term.db")
with con:
    sql = "SELECT * FROM artist_mbtag"
    artist_mbtag = psql.read_sql(sql, con)
    sql = "SELECT * FROM artist_term"
    artist_term = psql.read_sql(sql, con)
con.close()

# http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/track_metadata.db
con = sqlite.connect("track_metadata.db")
with con:
    sql = "SELECT * FROM songs"
    track_metadata = psql.read_sql(sql, con)
con.close()

# http://labrosa.ee.columbia.edu/millionsong/sites/default/files/lastfm/lastfm_tags.db
# tag values indicate popularity of the tags on last.fm as a whole
con = sqlite.connect("lastfm_tags.db")
with con:
    sql = "SELECT tags.tag, tids.tid, tid_tag.val FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID"
    lastfm_tags = psql.read_sql(sql, con)
con.close()

# http://labrosa.ee.columbia.edu/millionsong/sites/default/files/lastfm/lastfm_similars.db
# Similarity data from lastfm, the dest contains songs that consider the tid as similar while the src contains songs where tid considers as similar
con = sqlite.connect("lastfm_similars.db")
with con:
    sql = "SELECT * FROM similars_dest"
    lastfm_dest = psql.read_sql(sql, con)
    sql = "SELECT * FROM similars_src"
    lastfm_src = psql.read_sql(sql, con)
con.close()
