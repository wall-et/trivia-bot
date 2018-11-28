import urllib2
from bs4 import BeautifulSoup
import pandas as pd

# pages2017 = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2017_Popular_pages")
# pprint.pprint(pages2017.text)



# Get the html source
html = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2017_Popular_pages")
# print(wp.page("User:West.andrew.g/2017 Popular pages").content)
df = pd.read_html(html.content)
print(df)

df.to_csv('beautifulsoup_pandas.csv', header=0, index=False, encoding='utf-8')
