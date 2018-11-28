# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
import pprint
import requests
import wikipedia

# f"https://en.wikipedia.org/w/api.php?action=query&titles={pageid}&prop=revisions&rvprop=content&rvsection=0&format=json")
# blobtext = requests.get(f"https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages")
# print(blobtext.text)
# var titleRegex = new RegExp("<a href=\"/browse/post/\\d*/\">([^(]*) \\(");
# matchObj = re.search("birth_date\s*=\s*{{.*?\|([0-9]*?\|[0-9]*?\|[0-9]*).*?}}", r.text, flags=0)
def get_guessing_value():
    return "Donald Trump"


def simple_game():
    value =wikipedia.page(get_guessing_value())
    print("title " + value.title)
    while True:
        word = input(f"word on {value.title}")
        if word in value.content:
            print("Way to go!")
        else:
            print("Your wrong.....")
        if word == exit:
            break
    # pprint.pprint(value.links)

simple_game()

