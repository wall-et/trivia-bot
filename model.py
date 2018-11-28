# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
import pprint
import requests
import wikipedia

# f"https://en.wikipedia.org/w/api.php?action=query&titles={pageid}&prop=revisions&rvprop=content&rvsection=0&format=json")
# blobtext = requests.get(f"https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages")
# print(blobtext.text)
# var titleRegex = new RegExp("<a href=\"/browse/post/\\d*/\">([^(]*) \\(");
# matchObj = re.search("birth_date\s*=\s*{{.*?\|([0-9]*?\|[0-9]*?\|[0-9]*).*?}}", r.text, flags=0)
NUM_WRONG_GUESSES = 3
NUM_GOOD_GUESSES = 5
POINTS_PER_GOOD_GUESS = 1
POINTS_PER_WRONG_GUESS = -1


def get_guessing_value():
    return "Donald Trump"


def one_round():
    current_good_guesses = 0
    current_wrong_guesses = 0
    player_score = 0
    value = wikipedia.page(get_guessing_value())
    print("current title " + value.title)

    while current_wrong_guesses < NUM_WRONG_GUESSES:
        word = input(f"guess a word on {value.title}\n")

        if f"{word}" in value.content:
            print("Way to go!")
            current_good_guesses += 1
            player_score += POINTS_PER_GOOD_GUESS
        else:
            print("Nope! You're wrong.")
            current_wrong_guesses += 1
            player_score += POINTS_PER_WRONG_GUESS
        if current_good_guesses == NUM_GOOD_GUESSES:
            print(f"You win!!!!!\nYour score is {player_score}")
            break
        if current_wrong_guesses == NUM_WRONG_GUESSES:
            print(f"Nah, You failed this round.\nYour score is {player_score}")
            break


one_round()
