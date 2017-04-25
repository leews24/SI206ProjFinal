## Your name:
## The option you've chosen: 2

# Put import statements you expect to need here!

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



# Write your test cases here.

class Task(unittest.TestCase):
    def test_langcount1(self):
        titanic = Movie("Titanic")
        self.assertEqual(type(titanic.langcount()), type(0))
    def test_langcount2(self):
        titanic = Movie("Titanic")
        self.assertEqual(titanic.langcount(), 2)
    def test_topbillfinder1(self):
        titanic = Movie("Titanic")
        self.assertEqual(type(titanic.topbillfinder()), type("a"))
    def test_topbillfinder2(self):
        titanic = Movie("Titanic")
        self.assertEqual(titanic.topbillfinder(), "Leonardo DiCaprio")
    def test_counter1(self):
        self.assertEqual(type(wordcounter), type(collections.Counter(a=0)))
    def test_counter2(self):
        self.assertEqual(type(wordcounter_dic["a"]), type(0))
    def test_Movies1(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Movies');
        result = cur.fetchall()
        self.assertTrue(len(result)==3)
        conn.close()
    def test_Movies2(self):
        conn = sqlite3.connect('movies.db')
        cur = conn.cursor()
        cur.execute('SELECT director FROM Movies');
        result = cur.fetchall()
        self.assertEqual(type(result[0]), type("Alfred Hitchcock"))
        conn.close()
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
## Remember to invoke all your tests...