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


def get_guessing_value():
    return "Donald Trump"


def simple_game():
    current_good_guesses = 0
    current_wrong_guesses = 0
    value = wikipedia.page(get_guessing_value())
    print("title " + value.title)
    while current_wrong_guesses < NUM_WRONG_GUESSES:
        word = input(f"word on {value.title}:")
        if word in value.content:
            print("Way to go!")
            current_good_guesses += 1
        else:
            print("Your wrong.....")
            current_wrong_guesses += 1
        if current_good_guesses==NUM_GOOD_GUESSES:
            print("You win!!!!!")
            break


    # pprint.pprint(value.links)


simple_game()
