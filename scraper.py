import pandas as pd
import requests
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.cluster import KMeans
import random

pd.set_option('display.max_columns', None)

test_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2012-13&SeasonType=Regular%20Season&StatCategory=PTS'
r = requests.get(url=test_url).json()

#table headers
tableHeaders = r['resultSet']['headers']
#player data 
palyerData = pd.DataFrame(r['resultSet']['rowSet'], columns=tableHeaders)


df_cols = ['Year', 'Season_type'] + tableHeaders

# request headers
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Sec-Ch-Ua':'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# stacking data into one df for different years
df = pd.DataFrame(columns=df_cols)

season_types = ['Regular%20Season', 'Playoffs']
years = ['2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24'] 

#looping through and doing a concat to build one big data frame
for y in years:
    for s in season_types:
        api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season='+y+'&SeasonType='+s+'&StatCategory=PTS'
        r = requests.get(url=api_url, headers=headers).json()
        temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=tableHeaders)
        temp_df2 = pd.DataFrame({'Year':[y for i in range(len(temp_df1))],
                                'Season_type':[s for i in range(len(temp_df1))]})
        temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)
        df = pd.concat([df, temp_df3], axis=0)

        print(f'Finished Scrapping for {y} {s}.')

        lag = np.random.uniform(low=5,high=20)
        print(f'...Waiting {round(lag,1)} seconds.')

        time.sleep(lag)
print(f'Finished!')

#visualization functions



# print(df)