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

    def add_to_DB(self,id):
        self.lists.replace_one({"user_id": id}, {"user_id": id, "score": 0}, upsert=True)

    def get_score(self, id):
        user=self.lists.find_one({"user_id": id})
        score=user['score']
        return score

    def update_score(self,id,score):
        self.lists.replace_one({"user_id": id}, {"user_id": id, "score": score}, upsert=True)


class GameLogic:
    def __init__(self):
        self.player_score = 0
        self.w_db = WordDB()
        self.w_db.add_to_DB()

    def string_found(self, string1, string2):
        if re.search(r"\b" + re.escape(string1) + r"\b", string2):
            return True
        return False

    def get_guessing_value(self, ):
        return "Donald Trump"

    def one_round(self):
        current_good_guesses = 0
        current_wrong_guesses = 0

        played_guesses = []
        value = wp.page(self.get_guessing_value())
        print("current title " + value.title)

        while current_wrong_guesses < settings.NUM_WRONG_GUESSES:
            word = input(f"guess a word on {value.title}\n").lower()

            if word in settings.LETTERS or set(word).issubset(settings.NUMBERS):
                print("Are you kidding? you can't guess numbers or letters....")
                continue

            if self.string_found(word, value.content.lower()):
                if word in played_guesses:
                    print("Nice try. can't fool me. you used this word already")
                    continue

                # if self.w_db.get_word(word) or word.isdecimal() or set(word).issubset(numbers) or set(word).issubset(letters):
                #     print("C'mon,This word is way to common......")
                #     continue

                played_guesses.append(word)
                print("Way to go!")
                current_good_guesses += 1
                self.player_score += settings.POINTS_PER_GOOD_GUESS
            else:
                print("Nope! You're wrong.")
                current_wrong_guesses += 1
                self.player_score += settings.POINTS_PER_WRONG_GUESS
            if current_good_guesses == settings.NUM_GOOD_GUESSES:
                print(f"You win!!!!!\nYour score is {self.player_score}")
                break
            if current_wrong_guesses == settings.NUM_WRONG_GUESSES:
                print(f"Nah, You failed this round.\nYour score is {self.player_score}")
                break



