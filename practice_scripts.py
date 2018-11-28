from bs4 import BeautifulSoup
import pandas as pd
import requests

# Get the html source
html = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2017_Popular_pages")
df = pd.read_html(html.content)
table_dataframe = df[2][1:]
column_names = ["Rank", "Article", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "views",
                "perc1", "perc2"]
table_dataframe.columns = column_names
# table_dataframe.to_csv('beautifulsoup_pandas.csv', index=False, header=column_names)

table_dataframe_minimal = table_dataframe[['Article','views']]
table_dataframe_minimal.to_csv('minimal_data.csv', index=False, header=['Article','views'])



# html = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2016_Popular_pages")
# df = pd.read_html(html.content)
# print(df[1][1:])
# table2 = df[1][1:]
# with open('beautifulsoup_pandas.csv', 'a') as f:
#     df.to_csv(table2, index=False, header=False)


#
# df = pd.read_csv("beautifulsoup_pandas.csv")
# print(df['Article'])

