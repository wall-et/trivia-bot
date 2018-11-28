import pprint
import random

import requests
import wikipedia as wp
import re
import settings
from pymongo.mongo_client import MongoClient
import pandas
import csv
from collections import defaultdict


class PagesDB:
    def __init__(self):
        self.client = MongoClient(settings.HOST)
        self.db = self.client.get_database(settings.DB)
        self.lists = self.db.get_collection(settings.PAGE_COL)

    def add_all_to_DB(self):
        with open("minimal_data.csv", "r", encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=",")
            for i, line in enumerate(reader):
                # print('line[{}] = {}'.format(i, line))
                self.lists.replace_one({"title": line[0].lower()}, {"title": line[0].lower()}, upsert=True)

    def get_page(self, word):
        return self.lists.find_one({"title": word})

    def get_random_page(self):
        count = self.lists.estimated_document_count()
        return self.lists.find()[random.randrange(count)]['title']


class WordsDB:
    def __init__(self):
        self.client = MongoClient(settings.HOST)
        self.db = self.client.get_database(settings.DB)
        self.lists = self.db.get_collection(settings.WORD_COL)

    def add_all_to_DB(self):
        with open("common_words.txt", "r") as f:
            for word in f:
                self.lists.replace_one({"word": word.split()[0].lower()}, {"word": word.split()[0].lower()},
                                       upsert=True)

    def get_word(self, word):
        return self.lists.find_one({"word": word})


class UsersDB:
    def __init__(self):
        self.client = MongoClient(settings.HOST)
        self.db = self.client.get_database(settings.DB)
        self.lists = self.db.get_collection(settings.USER_COL)

    def add_to_DB(self, id):
        if not self.lists.find_one({"user_id": id}):
            self.lists.insert_one({"user_id": id, "score": 0})

    def get_score(self, id):
        user = self.lists.find_one({"user_id": id})
        score = user['score']
        return score

    def update_score(self, id, score):
        self.lists.replace_one({"user_id": id}, {"user_id": id, "score": self.get_score(id) + score}, upsert=True)


class GameLogic:
    def setup_dbs(self):
        dbnames=MongoClient(settings.HOST)[settings.DB].collection_names()
        if not settings.PAGE_COL in dbnames:
            self.p_db.add_all_to_DB()
        if not settings.WORD_COL in dbnames:
            self.w_db.add_all_to_DB()

    def __init__(self):
        self.w_db = WordsDB()
        # self.w_db.add_all_to_DB()
        self.p_db = PagesDB()
        # self.p_db.add_all_to_DB()
        self.user_db = UsersDB()
        self.setup_dbs()
        self.users_info_dict = defaultdict()


    def add_user(self, id):
        self.user_db.add_to_DB(id)
        # self.users_state_dict[id] = "getting value"
        # self.users_info_dict[id] = {"good_guesses": 0, "wrong_guesses": 0, "score": 0, "played_guesses": []}

        self.users_info_dict[id] = defaultdict()
        self.users_info_dict[id]['state'] = "getting value"
        self.users_info_dict[id]['good_guesses'] = 0
        self.users_info_dict[id]['wrong_guesses'] = 0
        self.users_info_dict[id]['score'] = 0
        self.users_info_dict[id]['played_guesses'] = []


    def get_full_page(self, id):
        value = wp.page(self.users_info_dict[id]['page_title'])
        self.users_info_dict[id]['page_content'] = value

    def get_page_title(self,id):
        self.users_info_dict[id]['page_title'] = self.p_db.get_random_page()
        return self.users_info_dict[id]['page_title']

    def string_found(self, string1, string2):
        if re.search(r"\b" + re.escape(string1) + r"\b", string2):
            return True
        return False

    def test_word(self, word, id):
        word = word.lower()

        if self.users_info_dict[id]['state'] == "getting value":
            if word == "yes":
                self.users_info_dict[id]['state'] = "playing"
                self.get_full_page(id)
                return "Ok. Try and guess 5 main words about it!"

            elif word == "no":
                self.get_page_title(id)
                return f"So have you heard about {self.users_info_dict[id]['page_title']}?"
            else:
                return "invalid answer.... answer 'yes' or 'no'."

        if self.users_info_dict[id]['state'] == "failed":
            if word == "yes":
                self.users_info_dict[id]['state'] = "getting value"
                return wp.summary(self.users_info_dict[id]['page_title'],sentences=3)
            elif word == "no":
                self.users_info_dict[id]['state']="getting value"
                return
            else:
                return "invalid answer.... answer 'yes' or 'no'."


        if word in settings.LETTERS or set(word).issubset(settings.NUMBERS):
            return "Are you kidding? you can't guess numbers or letters...."


        if word in self.users_info_dict[id]['page_title'].lower():
            return "hey, enter words about it...."

        if self.string_found(word, self.users_info_dict[id]['page_content'].content.lower()):
            split = word.split()

            for w in split:
                if w in self.users_info_dict[id]["played_guesses"]:
                    return "Nice try. can't fool me. you used this word already"

            if self.w_db.get_word(word):
                return "C'mon,This word is way too common......"

            [self.users_info_dict[id]["played_guesses"].append(w) for w in split]
            self.users_info_dict[id]["good_guesses"] += 1
            self.users_info_dict[id]["score"] += settings.POINTS_PER_GOOD_GUESS
            if self.users_info_dict[id]['good_guesses'] == settings.NUM_GOOD_GUESSES:
                self.user_db.update_score(id, self.users_info_dict[id]['score'])
                return f"You win!!!!!\nYour score is {self.user_db.get_score(id)}"
            return f"Way to go! you'l win in {settings.NUM_GOOD_GUESSES -self.users_info_dict[id]['good_guesses']} guesses"

        else:
            self.users_info_dict[id]["wrong_guesses"] += 1
            self.users_info_dict[id]["score"] += settings.POINTS_PER_WRONG_GUESS
            if self.users_info_dict[id]['wrong_guesses'] == settings.NUM_WRONG_GUESSES:
                self.user_db.update_score(id, self.users_info_dict[id]['score'])
                self.users_info_dict[id]['state'] = "failed"
                return f"Nah, You failed this round.\n Your score is {self.user_db.get_score(id)}\n would you like to here about this subject?"
            return f"Nope! You're wrong. tries left: {settings.NUM_WRONG_GUESSES -self.users_info_dict[id]['wrong_guesses']}"
