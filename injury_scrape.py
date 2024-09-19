import bs4
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import pandas as pd
import itertools
from ast import literal_eval
import ast
import math
import re
import matplotlib.pyplot as plt
from difflib import SequenceMatcher
from collections import Counter
import collections
import copy

import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)
urls_list = []

def create_list_urls(urls):
    
    for y in range(2023,2024):
        #create regular season urls
        for w in range(1,3):
            urls.append('https://www.nfl.com/injuries/league/' + str(y) + '/reg' + str(w))
        
        #create post season urls
        for i in range(1,4):
            urls.append('https://www.nfl.com/injuries/league/' + str(y) + '/post' + str(i))

        #create pro season urls
        urls.append('https://www.nfl.com/injuries/league/' + str(y) + '/pro1')    
            

    
def injury_data(url_list):
    all_players = []
    df_list = []
    df = pd.DataFrame()

    for i in url_list:
        print('Injuries from ' + i)
        curr_season = re.search("\d\d\d\d", i).group()
        try:
            alpha = requests.get(i)
            beta = bs4.BeautifulSoup(alpha.text)
            tables = beta.findAll("table")
            teams = beta.findAll("div", class_="d3-o-section-sub-title")
            idx = 0
            for table in tables:
                if table.findParent("table") is None:
                    tbody = table.find("tbody")
                    for tr in tbody:
                        try:
                            td = tr.find_all("td") 
                            rows = [tr.text.strip() for tr in td if tr is not None and len(tr) > 0]
                            for i in rows:
                                df_list.append(i) #at the player level
                            df_list.append(curr_season)
                            df_list.append(teams[idx].find("span").text)
                            all_players.append(copy.copy(df_list))
                            df_list = []
                    
                        except:
                            print("Didnt find element in tr")
                idx += 1        
        except:
            print("Error with url: " + i)
        print(len(all_players))
    return all_players
        

    # players_df['data'] = all_players
    # df['data'] = df_list
    # df = df[
    #     (df['data'].str.contains('Out'))
    #      | (df['data'].str.contains('Questionable'))
    #      ]
    # #df['year'] = str(year)

    # return df
        
create_list_urls(urls_list)
players_df = pd.DataFrame(injury_data(urls_list), columns = ['Player', 'Position', 'Injury', 'Practice', 'GameStatus', 'Season', 'Team'])
injury_counts = players_df.groupby(['Player', 'Season', 'Position', 'Injury']).size().unstack(fill_value=0).reset_index()
practice_counts = players_df.groupby(['Player', 'Season', 'Position', 'Practice']).size().unstack(fill_value=0).reset_index()
status_counts = players_df.groupby(['Player', 'Season', 'Position', 'GameStatus']).size().unstack(fill_value=0).reset_index()



print("Complete")


#concat all dfs
df1 = injury_data(url_list_2012,'2012')
df2 = injury_data(url_list_2013,'2013')
df3 = injury_data(url_list_2014,'2014')
df4 = injury_data(url_list_2015,'2015')
df5 = injury_data(url_list_2016,'2016')
df6 = injury_data(url_list_2017,'2017')
df7 = injury_data(url_list_2018,'2018')
df8 = injury_data(url_list_2019,'2019')
df9 = injury_data(url_list_2020,'2020')
df10 = injury_data(url_list_2021,'2021')
df11 = injury_data(url_list_2022,'2022')

df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11], ignore_index=True)

display('semi raw data:', df.shape)

# create row number col
df['row_number'] = df.sort_values(['data','year'], ascending=[True,True]) \
             .groupby(['year']) \
             .cumcount() + 1
display('df with rownumber:', df.sort_values(by=['row_number','year'],ascending=True).head())

#create group by per year per injury status
group_df = df.groupby(['data','year'])['row_number'].agg('count').reset_index()
group_df.columns = ['data','year','count_players']
display('grouped df shape:', group_df.shape)
display('groupd data:', group_df.head())

#show fig
fig = px.line(group_df
              ,x='year'
              ,y='count_players'
              ,color='data'
              ,text='count_players'
              ,template='plotly_dark'
              ,height=500
              ,title='Injury Data Through First 10 Weeks per Year'
             )
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

#all data no breakdown
group_df1 = group_df.groupby('year')['count_players'].agg('sum').reset_index()
group_df1.columns = ['year','count_players']
fig1 = px.bar(group_df1
              ,x='year'
              ,y='count_players'
              ,text='count_players'
              ,template='plotly_dark'
              ,height=300
              ,title='Injury Data Through First 10 Weeks per Year'
             )
fig1.update_xaxes(showgrid=False)
fig1.update_yaxes(showgrid=False)

end_time = datetime.now()
print('Script Completed. ','Duration: {}'.format(end_time - start_time))

fig.show()
fig1.show()