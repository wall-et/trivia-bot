import csv

from bs4 import BeautifulSoup
import pandas as pd
import requests

# Get the html source
html17 = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2017_Popular_pages")
df17 = pd.read_html(html17.content)
table_dataframe17 = df17[2][1:]
column_names17 = ["Rank", "Article", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "views",
                  "perc1", "perc2"]
table_dataframe17.columns = column_names17
# table_dataframe.to_csv('beautifulsoup_pandas.csv', index=False, header=column_names)

table_dataframe_minimal17 = table_dataframe17[['Article', 'views']]
table_dataframe_minimal17.to_csv('minimal_data.csv', index=False, header=['Article', 'views'])

html16 = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2016_Popular_pages")
df16 = pd.read_html(html16.content)
table_dataframe16 = df16[1][1:]
column_names16 = ["Rank", "Article", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "views",
                  "perc1", "perc2"]
table_dataframe16.columns = column_names16
table_dataframe_minimal16 = table_dataframe16[['Article', 'views']]
# print(table_dataframe_minimal16)

with open('minimal_data.csv', 'a', encoding='utf-8') as f:
    table_dataframe_minimal16.to_csv(f, header=None, index=False)

# with open("minimal_data.csv", "r", encoding='utf-8') as f:
#     reader = csv.reader(f, delimiter=",")
#     for i, line in enumerate(reader):
#         print('line[{}] = {}'.format(i, line))