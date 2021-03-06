###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest
import itertools
import collections
import tweepy
import twitter_info
import json
import sqlite3
import codecs
import sys
import re
import requests
# Begin filling in instructions....



# Set up twitter info so that you can use tweepy like a cool kid.
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Get that encoding problem solved.
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

# Make a cache file.
CACHE_FNAME = "final_project_cache.json"
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {"Tweet_search":{}, "Tweet_user":{}, "OMDB_search":{}}

# Write a function to cache searh results from Twitter
def tweetsearch(query):
    iden = "tweeter_search_" + query
    if iden in CACHE_DICTION["Tweet_search"]:
        print("========== Using cached data for the movie, " + query + " on Twitter.")
        ret = CACHE_DICTION["Tweet_search"][iden]
        return ret
    else:
        print("========== Data missing for the movie, " + query + " on Twitter.")
        print("========== Caching now.")
        ret = api.search(query)
        CACHE_DICTION["Tweet_search"][iden] = ret
        codecfile = codecs.open(CACHE_FNAME,'w')
        codecfile.write(json.dumps(CACHE_DICTION))
        codecfile.close()
        return ret

# Write a function to cache user searh results from Twitter
def tweetuser(query):
    iden = "tweeter_user_" + query
    if iden in CACHE_DICTION["Tweet_user"]:
        print("========== Using cached data for the user, " + query + " on Twitter.")
        ret = CACHE_DICTION["Tweet_user"][iden]
        return ret
    else:
        print("========== Data missing for the user, @" + query + " on Twitter.")
        print("========== Caching now.")
        ret = api.get_user(query)
        CACHE_DICTION["Tweet_user"][iden] = ret
        codecfile = codecs.open(CACHE_FNAME,'w')
        codecfile.write(json.dumps(CACHE_DICTION))
        codecfile.close()
        return ret

# Write a function to cache Movie searh results from OMDB
def omdbsearch(query):
    iden = "omdb_search_" + query
    if iden in CACHE_DICTION["OMDB_search"]:
        print("========== Using cached data for the movie, " + query + " on OMDB.")
        ret = CACHE_DICTION["OMDB_search"][iden]
        return ret
    else:
        print("========== Data missing for the movie, " + query + " on OMDB.")
        print("========== Caching now.")
        resp = requests.get("http://www.omdbapi.com/?", params = {"t":query})
        ret = json.loads(resp.text)
        CACHE_DICTION["OMDB_search"][iden] = ret
        codecfile = codecs.open(CACHE_FNAME,'w')
        codecfile.write(json.dumps(CACHE_DICTION))
        codecfile.close()
        return ret

# Run it a couple times so that there is data to put in the table.

tweetuser("UMich")
tweetsearch("Guardians of the Galaxy Vol. 2")
omdbsearch("Guardians of the Galaxy Vol. 2")
tweetsearch("Star Wars Star Wars: The Force Awakens")
omdbsearch("Star Wars: The Force Awakens")


# Create a database for this project that will hold all the cached data.
# Refer to the plan document for the structure of the tables.
conn = sqlite3.connect('final_project_db.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweet_Searchdb')

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweet_Searchdb (tweet_id string PRIMARY KEY, '
table_spec += 'search_term TEXT, text TEXT, user_id TEXT, retweets INTEGER)'
cur.execute(table_spec)
statement1 = 'INSERT INTO Tweet_Searchdb VALUES (?,?,?,?,?)'
for searchres in CACHE_DICTION["Tweet_search"]:
    for tweets in CACHE_DICTION["Tweet_search"][searchres]["statuses"]:
        cur.execute(statement1, (tweets["id_str"], CACHE_DICTION["Tweet_search"][searchres]["search_metadata"]["query"], tweets["text"], tweets["user"]["id_str"], tweets["retweet_count"]))

cur.execute('DROP TABLE IF EXISTS Tweet_Usersdb')

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweet_Usersdb (user_id STRING PRIMARY KEY, '
table_spec += 'screen_name TEXT, num_favs INTEGER, description TEXT)'
cur.execute(table_spec)
statement2 = 'INSERT INTO Tweet_Usersdb VALUES (?,?,?,?)'
for searchres in CACHE_DICTION["Tweet_user"]:
    cur.execute(statement2, (CACHE_DICTION["Tweet_user"][searchres]["id"], CACHE_DICTION["Tweet_user"][searchres]["screen_name"], CACHE_DICTION["Tweet_user"][searchres]["favourites_count"], CACHE_DICTION["Tweet_user"][searchres]["description"]))

cur.execute('DROP TABLE IF EXISTS OMDBdb')
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'OMDBdb (IMDBid STRING PRIMARY KEY, '
table_spec += 'Title TEXT, Director TEXT, Language_Count INTEGER, Rating TEXT, Actors TEXT)'
cur.execute(table_spec)
statement3 = 'INSERT INTO OMDBdb VALUES (?,?,?,?,?,?)'
for searchres in CACHE_DICTION["OMDB_search"]:
    cur.execute(statement3, (CACHE_DICTION["OMDB_search"][searchres]["imdbID"],CACHE_DICTION["OMDB_search"][searchres]["Title"],CACHE_DICTION["OMDB_search"][searchres]["Director"],len(CACHE_DICTION["OMDB_search"][searchres]["Language"]),CACHE_DICTION["OMDB_search"][searchres]["imdbRating"],CACHE_DICTION["OMDB_search"][searchres]["Actors"]))


conn.commit()

# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class Task(unittest.TestCase):
    # def test_langcount1(self):
    #     titanic = Movie("Titanic")
    #     self.assertEqual(type(titanic.langcount()), type(0))
    # def test_langcount2(self):
    #     titanic = Movie("Titanic")
    #     self.assertEqual(titanic.langcount(), 2)
    # def test_topbillfinder1(self):
    #     titanic = Movie("Titanic")
    #     self.assertEqual(type(titanic.topbillfinder()), type("a"))
    # def test_topbillfinder2(self):
    #     titanic = Movie("Titanic")
    #     self.assertEqual(titanic.topbillfinder(), "Leonardo DiCaprio")
    # def test_counter1(self):
    #     self.assertEqual(type(wordcounter), type(collections.Counter(a=0)))
    # def test_counter2(self):
    #     self.assertEqual(type(wordcounter_dic["a"]), type(0))
    def test_Movies1(self):
        conn = sqlite3.connect('final_project_db.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM OMDBdb');
        result = cur.fetchall()
        self.assertTrue(len(result)==2)
        conn.close()
    def test_Movies2(self):
        conn = sqlite3.connect('final_project_db.db')
        cur = conn.cursor()
        cur.execute('SELECT director FROM OMDBdb');
        result = cur.fetchall()
        self.assertEqual(type(result[0][0]), type("Alfred Hitchcock"))
        conn.close()
        

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
    unittest.main(verbosity=2)