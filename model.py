# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
import pprint
import requests
import wikipedia
import re
import settings
# f"https://en.wikipedia.org/w/api.php?action=query&titles={pageid}&prop=revisions&rvprop=content&rvsection=0&format=json")
# blobtext = requests.get(f"https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages")
# print(blobtext.text)
# var titleRegex = new RegExp("<a href=\"/browse/post/\\d*/\">([^(]*) \\(");
# matchObj = re.search("birth_date\s*=\s*{{.*?\|([0-9]*?\|[0-9]*?\|[0-9]*).*?}}", r.text, flags=0)

def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False


def get_guessing_value():
    return "Donald Trump"


def one_round():
    current_good_guesses = 0
    current_wrong_guesses = 0
    player_score = 0
    played_guesses = []
    value = wikipedia.page(get_guessing_value())
    print("current title " + value.title)

    while current_wrong_guesses < settings.NUM_WRONG_GUESSES:
        word = input(f"guess a word on {value.title}\n")

        if string_found(word, value.content):
            if word in played_guesses:
                print("Nice try. can't fool me. you used this word already")
                continue
            played_guesses.append(word)
            print("Way to go!")
            current_good_guesses += 1
            player_score += settings.POINTS_PER_GOOD_GUESS
        else:
            print("Nope! You're wrong.")
            current_wrong_guesses += 1
            player_score += settings.POINTS_PER_WRONG_GUESS
        if current_good_guesses == settings.NUM_GOOD_GUESSES:
            print(f"You win!!!!!\nYour score is {player_score}")
            break
        if current_wrong_guesses == settings.NUM_WRONG_GUESSES:
            print(f"Nah, You failed this round.\nYour score is {player_score}")
            break


one_round()
