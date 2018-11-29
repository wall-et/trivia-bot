import random
import wikipedia as wp
import re
import settings
from pymongo.mongo_client import MongoClient
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
                if re.search(r"\b" + re.escape(line[0].lower()) + r"\b", settings.WIKI_EXLUDE_VALS):
                    continue
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


class fail_gifDB:
    def __init__(self):
        self.client = MongoClient(settings.HOST)
        self.db = self.client.get_database(settings.DB)
        self.lists = self.db.get_collection(settings.FAILER_GIFS_COL)

    def add_all_to_DB(self):
        with open("fail_gifs.txt", "r") as f:
            for url in f.readlines():
                self.lists.replace_one({"url": url}, {"url": url},
                                       upsert=True)

    def get_random_gif(self):
        count = self.lists.estimated_document_count()
        return self.lists.find()[random.randrange(count)]['url']
        # return self.lists.find().limit(-1).skip(random.randint(0, 12)).next()['url']


class win_gifDB:
    def __init__(self):
        self.client = MongoClient(settings.HOST)
        self.db = self.client.get_database(settings.DB)
        self.lists = self.db.get_collection(settings.WINNER_GIFS_COL)

    def add_all_to_DB(self):
        with open("win_gifs.txt", "r") as f:
            for url in f.readlines():
                self.lists.replace_one({"url": url}, {"url": url},
                                       upsert=True)

    def get_random_gif(self):
        count = self.lists.estimated_document_count()
        return self.lists.find()[random.randrange(count)]['url']


class GameLogic:
    def setup_dbs(self):
        dbnames = MongoClient(settings.HOST)[settings.DB].list_collection_names()
        if not settings.PAGE_COL in dbnames:
            self.p_db.add_all_to_DB()
        if not settings.WORD_COL in dbnames:
            self.w_db.add_all_to_DB()
        if not settings.WINNER_GIFS_COL in dbnames:
            self.wg_db.add_all_to_DB()
        if not settings.FAILER_GIFS_COL in dbnames:
            self.g_db.add_all_to_DB()

    def __init__(self):
        self.w_db = WordsDB()
        self.p_db = PagesDB()
        self.user_db = UsersDB()
        self.g_db = fail_gifDB()
        self.wg_db = win_gifDB()
        self.setup_dbs()
        self.users_info_dict = defaultdict()

    def add_user(self, id):
        self.user_db.add_to_DB(id)
        self.users_info_dict[id] = defaultdict()
        self.users_info_dict[id]['state'] = "getting value"
        self.users_info_dict[id]['good_guesses'] = 0
        self.users_info_dict[id]['wrong_guesses'] = 0
        self.users_info_dict[id]['score'] = 0
        self.users_info_dict[id]['played_guesses'] = []
        self.users_info_dict[id]['infinite_round'] = False

    def get_full_page(self, id):
        value = wp.page(self.users_info_dict[id]['page_title'])
        self.users_info_dict[id]['page_content'] = value

    def get_page_title(self, id):
        self.users_info_dict[id]['page_title'] = self.p_db.get_random_page()
        return self.users_info_dict[id]['page_title']

    def string_found(self, string1, string2):
        if re.search(r"\b" + re.escape(string1) + r"\b", string2):
            return True
        return False

    def toggle_infinte_game(self, id):
        if self.users_info_dict[id]['infinite_round']:
            self.users_info_dict[id]['infinite_round'] = False
        else:
            self.users_info_dict[id]['infinite_round'] = True

    # def test_premium(self, string1, liststr):
    #     for link in liststr:
    #         if re.search(r"\b" + re.escape(string1) + r"\b", link):
    #             self.users_info_dict[id]["played_guesses"].append(string1)
    #             return True
    #     return False

    def get_random_list_value(self, list):
        # return list[random.randrange(len(list))]
        return random.choice(list)

    def get_more_info(self, id):
        return wp.summary(self.users_info_dict[id]['page_title'], sentences=3) + '\n' + self.users_info_dict[id][
            'page_content'].url

    def test_word(self, word, id):
        word = word.lower()
        if self.users_info_dict[id]['state'] == "getting value":

            if word == "yes":
                self.users_info_dict[id]['state'] = "playing"
                self.get_full_page(id)
                return f"Ok. We've collected some Data about it.\nTry and guess {settings.NUM_GOOD_GUESSES} important words about this value!\nGive me your first guess"

            elif word == "no":
                self.get_page_title(id)
                page_title = self.users_info_dict[id]['page_title']
                return self.get_random_list_value(settings.CHOOSE_VALUE).format(page_title)
                # return f"So have you heard about {self.users_info_dict[id]['page_title']}?"
            else:
                return self.get_random_list_value(settings.INVALID_ANSWERS)

        if word in settings.LETTERS or set(word).issubset(settings.NUMBERS):
            return self.get_random_list_value(settings.NUMBERS_RESPONSES)

        split = word.split()
        for w in split:
            if w in self.users_info_dict[id]["played_guesses"]:
                return self.get_random_list_value(settings.REPEATING_GUESS)
            for k in self.users_info_dict[id]['page_title'].lower():
                if w == k:
                    return self.get_random_list_value(settings.TITLE_REPONSES)

        if self.w_db.get_word(word):
            return self.get_random_list_value(settings.COMMON_RESPONSES)

        ####### good word #########
        if self.string_found(word, self.users_info_dict[id]['page_content'].content.lower()):
            [self.users_info_dict[id]["played_guesses"].append(w) for w in split]

            # if self.test_premium(word, self.users_info_dict[id]['page_content'].links):
            #     print(" prem")
            #     self.users_info_dict[id]["score"] += settings.POINTS_PER_GOOD_GUESS*2
            # else:
            self.users_info_dict[id]["score"] += settings.POINTS_PER_GOOD_GUESS

            self.users_info_dict[id]["good_guesses"] += 1

            if self.users_info_dict[id]['good_guesses'] == settings.NUM_GOOD_GUESSES:
                print("win")
                self.user_db.update_score(id, self.users_info_dict[id]['score'])
                score1 = self.user_db.get_score(id)
                link1 = self.wg_db.get_random_gif()
                return self.get_random_list_value(settings.WIN_RESPONSES).format(score1, link1)

            score1 = settings.NUM_GOOD_GUESSES - self.users_info_dict[id]['good_guesses']
            return self.get_random_list_value(settings.SUCCESS_RESPONSES).format(score1)

        else:
            self.users_info_dict[id]["wrong_guesses"] += 1
            self.users_info_dict[id]["score"] += settings.POINTS_PER_WRONG_GUESS
            if self.users_info_dict[id]['wrong_guesses'] == settings.NUM_WRONG_GUESSES:
                self.user_db.update_score(id, self.users_info_dict[id]['score'])
                score1 = self.user_db.get_score(id)
                link1 = self.g_db.get_random_gif()
                return self.get_random_list_value(settings.LOSE_RESPONSES).format(score1, link1)
            score1 = settings.NUM_WRONG_GUESSES - self.users_info_dict[id]['wrong_guesses']
            return self.get_random_list_value(settings.FAIL_RESPONSES).format(score1)
