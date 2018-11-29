
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


html15 = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2015_Popular_pages")
df15 = pd.read_html(html15.content)
table_dataframe15 = df15[1][1:]
column_names15 = ["Rank", "Article", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "views",
                  "perc1", "perc2"]
table_dataframe15.columns = column_names15
table_dataframe_minimal15 = table_dataframe15[['Article', 'views']]
# print(table_dataframe_minimal16)

with open('minimal_data.csv', 'a', encoding='utf-8') as f:
    table_dataframe_minimal15.to_csv(f, header=None, index=False)



html14 = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2014_Popular_pages")
df14 = pd.read_html(html14.content)
table_dataframe14 = df14[1][1:]
column_names14 = ["Rank", "Article", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "views",
                  "perc1",]
table_dataframe14.columns = column_names14
table_dataframe_minimal14 = table_dataframe14[['Article', 'views']]
# print(table_dataframe_minimal16)

with open('minimal_data.csv', 'a', encoding='utf-8') as f:
    table_dataframe_minimal14.to_csv(f, header=None, index=False)


html13 = requests.get(f"https://en.wikipedia.org/wiki/User:West.andrew.g/2013_popular_pages")
df13 = pd.read_html(html13.content)
# print(df13[1])
table_dataframe13 = df13[1][1:]
column_names13 = ["Rank", "Article", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "views",]
table_dataframe13.columns = column_names13
table_dataframe_minimal13 = table_dataframe13[['Article', 'views']]
# print(table_dataframe_minimal16)

with open('minimal_data.csv', 'a', encoding='utf-8') as f:
    table_dataframe_minimal13.to_csv(f, header=None, index=False)
