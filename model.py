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


class Storage:
    def __init__(self, host, db, col):
        self.client = MongoClient(host)
        self.db = self.client.get_database(db)
        self.lists = self.db.get_collection(col)

    def add_item(self, word):
        self.lists.replace_one({"word": word}, {"word": word}, upsert=True)

    def get_item(self, word):
        return self.lists.find_one({"word": word})


class WordDB:
    def __init__(self):
        self.storage = Storage(settings.HOST, settings.DB, settings.WORD_COL)

    def add_to_DB(self):
        with open("common_words.txt", "r") as f:
            for word in f:
                # splitted = line.split()
                # if len(splitted) > 0:
                #     for word in splitted:
                self.storage.add_item(word.split()[0])

    def get_word(self,word):
        return self.storage.get_item(word)


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
            word = input(f"guess a word on {value.title}\n")

            if self.string_found(word, value.content.lower()):
                if word in played_guesses:
                    print("Nice try. can't fool me. you used this word already")
                    continue

                if self.w_db.get_word(word):
                    print("C'mon,This word is way to common......")
                    continue

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


game=GameLogic()
game.one_round()


