# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
import pprint
import requests
import wikipedia



# f"https://en.wikipedia.org/w/api.php?action=query&titles={pageid}&prop=revisions&rvprop=content&rvsection=0&format=json")
# blobtext = requests.get(f"https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages")
# print(blobtext.text)
# var titleRegex = new RegExp("<a href=\"/browse/post/\\d*/\">([^(]*) \\(");
# matchObj = re.search("birth_date\s*=\s*{{.*?\|([0-9]*?\|[0-9]*?\|[0-9]*).*?}}", r.text, flags=0)

ny = wikipedia.page("Donald Trump")
print("title" + ny.title)
# u'New York'
# ny.url
# u'http://en.wikipedia.org/wiki/New_York'
# pprint.pprint("content------------ " + ny.content)
while False:
    word = input("word on donald")
    if word in ny.content:
        print("GO US")
    else:
        print("NOPE")
    if word == exit:
        break
# u'New York is a state in the Northeastern region of the United States. New York is the 27th-most exten'...
pprint.pprint(ny.links)
# u'1790 United States Census'

# >>> wikipedia.set_lang("fr")
# >>> wikipedia.summary("Facebook", sentences=1)
