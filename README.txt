The following are pieces of information you need to include:
What option did you pick (1, 2, or 3)
1

What does it do? 1-3 sentences
Compare the popularity of each movie by retweets and return the most common word used in those tweets.

Why does it exist / what can you use it for
Comparing the popularity between 3 movies, "Guardians of the Galaxy Vol. 2", "Star Wars: The Force Awakens", "Spider-Man: Homecoming"

With (any input?), what does it output when run
No inputs. Movies are set by default. It outputs a text file of summary and a database.

Does it create a database? 
Yes.

How do you run it?
1 line description / example of how to run the correct file.
Make sure you have pip, python, and sql installed. Run the "206_project.py" file.

What are its dependencies? You should list these with bulletpoints.
Any modules to install with pip ?
-unittest
-itertools
-collections
-tweepy
-twitter_info
-json
-sqlite3
-codecs
-sys
-re
-requests

Any particular files you have to have? (e.g. your own twitter_info.py file with certain specifications?
-twitter_info.py

What files are included? Another bulletpoint list.
-README.txt (Readme instructions file)
-final_project_db.db(sample of database tables)
-output.txt(sample of output text file)

Each function
-tweetsearch(query)
takes in a twitter search query word(required) and caches search data

-tweetuser(query)
takes in a twitter user search query word(required) and caches user data

-omdbsearch(query)
takes in a movie search query word(required) and caches movie data from OMDB

-wordcounter(strtext)
takes in a string(required) and returns a dictionary of word count.


Each class
-Movie()
required input: none
optional input: name = "", director = "", IMDB_rating= "0", cast = "", langcount = 0
it is suggested to make a optional inpupts as they are very likely to cause errors otherwise.

Datamanipulation
Counter class from Collections module used, used to make a simple dictionary of the most commonly used words in a list of tweets. It's useful because I do not have to lines of code after code to loop through each word.

Database creation
OMDBdb
data from OMDB
rows:
IMDBid STRING PRIMARY KEY, Title TEXT, Director TEXT, Language_Count INTEGER, Rating TEXT, Actors TEXT

Tweet_Searchdb
data from Twitter search
rows:
tweet_id string PRIMARY KEY, search_term TEXT, text TEXT, user_id TEXT, screen_name TEXT, retweets INTEGER

Tweet_Usersdb
data from Twitter user search
rows:
user_id STRING PRIMARY KEY, screen_name TEXT, num_favs INTEGER, description TEXT

Why did you choose to do this project?
Because I was interested in the recent relase of movies.