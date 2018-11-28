# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
import pprint
import requests
import wikipedia

# blobtext = requests.get(f"https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages")
# print(blobtext.text)
# var titleRegex = new RegExp("<a href=\"/browse/post/\\d*/\">([^(]*) \\(");
# matchObj = re.search("birth_date\s*=\s*{{.*?\|([0-9]*?\|[0-9]*?\|[0-9]*).*?}}", r.text, flags=0)

ny = wikipedia.page("Donald Trump")
print("title" + ny.title)
while False:
    word = input("word on donald")
    if word in ny.content:
        print("GO US")
    else:
        print("NOPE")
    if word == exit:
        break
pprint.pprint(ny.links)

