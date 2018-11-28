import pprint
import requests
import wikipedia as wp
import re
import settings
from pymongo.mongo_client import MongoClient
import pandas


# f"https://en.wikipedia.org/w/api.php?action=query&titles={pageid}&prop=revisions&rvprop=content&rvsection=0&format=json")
# blobtext = requests.get(f"https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages")
# print(blobtext.text)
# var titleRegex = new RegExp("<a href=\"/browse/post/\\d*/\">([^(]*) \\(");
# matchObj = re.search("birth_date\s*=\s*{{.*?\|([0-9]*?\|[0-9]*?\|[0-9]*).*?}}", r.text, flags=0)

class WordDB:
    def __init__(self):
        self.client = MongoClient(settings.HOST)
        self.db = self.client.get_database(settings.DB)
        self.lists = self.db.get_collection(settings.WORD_COL)

    def add_to_DB(self):
        with open("common_words.txt", "r") as f:
            for word in f:
                self.lists.replace_one({"word": word.split()[0].lower()}, {"word": word.split()[0].lower()},
                                       upsert=True)

    def get_word(self, word):
        return self.lists.find_one({"word": word})


class UserDB:
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
        self.lists.replace_one({"user_id": id}, {"user_id": id, "score": self.get_score()+score}, upsert=True)


class GameLogic:
    def __init__(self):
        self.w_db = WordDB()
        self.w_db.add_to_DB()
        self.user_db = UserDB()
        self.users_state_dict = {}
        self.users_info_dict = {}

    def add_user(self, id):
        self.user_db.add_to_DB(id)
        self.users_state_dict[id]="getting value"
        self.users_info_dict[id] = {"good_guesses": 0, "wrong_guesses": 0, "score": 0, "played_guesses": []}

    def get_value(self,id):
        value = wp.page("Donald Trump")
        self.users_info_dict['id']['value']=value
        return value

    def string_found(self, string1, string2):
        if re.search(r"\b" + re.escape(string1) + r"\b", string2):
            return True
        return False


    def test_word(self, word, id):
        word=word.lower()

        if self.users_state_dict[id]=="getting value":
            if word == "yes":
                self.users_state_dict[id] = "playing"
                return "Ok. Try and guess 5 main words about him!"
            elif word == "no":
                value=self.get_value()
                return f"So you heard about{value.title}?"
            else:
                return "invalid answer.... answer 'yes' or 'no'."

        value=self.users_info_dict[id]['value']
        if word in settings.LETTERS or set(word).issubset(settings.NUMBERS):
            return "Are you kidding? you can't guess numbers or letters...."

        if self.string_found(word, value.content.lower()):
            if word in self.users_info_dict[id]["played_guesses"]:
                return "Nice try. can't fool me. you used this word already"

            if self.w_db.get_word(word):
                return "C'mon,This word is way to common......"

            self.users_info_dict[id]["played_guesses"].append(word)
            self.users_info_dict[id]["good_guesses"] += 1
            self.users_info_dict[id]["score"] += settings.POINTS_PER_GOOD_GUESS
            if self.users_info_dict['id']['good_guesses'] == settings.NUM_GOOD_GUESSES:
                self.user_db.update_score(id, self.users_info_dict['id']['score'])
                return f"You win!!!!!\nYour score is\n Your score is {self.users_info_dict['id']['score']}"
            return "Way to go!"

        else:
            self.users_info_dict[id]["wrong_guesses"] += 1
            self.users_info_dict[id]["score"] += settings.POINTS_PER_WRONG_GUESS
            if self.users_info_dict['id']['wrong_guesses'] == settings.NUM_WRONG_GUESSES:
                self.user_db.update_score(id, self.users_info_dict['id']['score'])
                return f"Nah, You failed this round.\n Your score is {self.users_info_dict['id']['score']}"
            return "Nope! You're wrong."

