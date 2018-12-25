import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.sports-reference.com/cfb/years/2017-schedule.html'

r = requests.get(url)

soup = BeautifulSoup(r.text)
table = soup.find('table', {'id': 'schedule'})
tbody = table.find('tbody')


def not_of_class_thead(class_):
    return 'thead' != class_


data_rows = tbody.find_all('tr', class_=not_of_class_thead)

include_stats = ['week_number', 'date_game', 'winner_school_name',
                 'winner_points', 'game_location', 'loser_school_name',
                 'loser_points', 'notes']
data = [[''.join(col.findAll(text=True))
         for col in row.find_all('td', {'data-stat': include_stats})]
        for row in data_rows]

df = pd.DataFrame(data, columns=include_stats)
df['date_game'] = pd.to_datetime(df['date_game'], infer_datetime_format=True)

for col in ['week_number', 'winner_points', 'loser_points']:
    df[col] = df[col].astype('int')

for team in ['winner', 'loser']:
    df[[f'{team}_rank', f'{team}_school_name']] = df[f'{team}_school_name'].str.extract(r'(?:\((\d+)\)\s)?(.*)')
df.head()
import networkx as nx

MDG = nx.MultiDiGraph()
MDG.add_edges_from(df[['loser_school_name', 'winner_school_name']].itertuples(index=False))
list(nx.dfs_tree(MDG, 'Alabama', depth_limit=2))
list(MDG.predecessors('Alabama'))
list(MDG.successors('Alabama'))
list(MDG.successors('Auburn'))
list(MDG.successors('Clemson'))
list(MDG.successors('Syracuse'))
list(nx.dfs_tree(MDG, 'Alabama'))
len(list(nx.dfs_tree(MDG, 'Alabama')))
len(MDG.nodes)
df.to_pickle('2017.pkl')
import os
os.getcwd()
