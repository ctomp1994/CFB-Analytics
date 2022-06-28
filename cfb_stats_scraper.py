# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 17:05:08 2019

@author: charl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import requests
import time

start_time = time.time()


url = 'http://www.cfbstats.com/'
page = requests.get(url)
pagetext = page.text

team = []
teams = pd.read_excel(r'C:\Users\charl\Desktop\KSDM Analytics\College Football\2018-2019\Teams.xlsx')
team = teams['Team'].tolist()


soup = bs(pagetext, 'html.parser')

    
team_site = []
team_num =[]
for link in soup.find_all('a'):
    x = link.get('href')
    if "/2020/team/" in x and "/index.html" in x:
        z = x[:-11]
        z1 = z[11:]
        team_num.append(z1)
        y = "http://www.cfbstats.com"+x
        team_site.append(y)

team_site.pop(0)
team_num.pop(0)

team_offense_site = []
i = 0
for i in range(0,len(team_site)):
    x = team_site[i]
    z = x[:-10] + "total/offense/gamelog.html"
    team_offense_site.append(z)
    
team_defense_site = []
i = 0
for i in range(0,len(team_site)):
    x = team_site[i]
    z = x[:-10] + "total/defense/gamelog.html"
    team_defense_site.append(z)

team_turnover_site = []
i = 0
for i in range(0,len(team_site)):
    x = team_site[i]
    z = x[:-10] + "turnovermargin/gamelog.html"
    team_turnover_site.append(z)
    
years = ['2013','2014','2015','2016','2017','2018','2019','2020']

i = 0
offense_year =[]
defense_year =[]
turnover_year = []
o_array = []
d_array = []
t_array =[]
for i in range(0, len(team_offense_site)):
    x = 0
    sub = []
    sub1 = []
    sub2 = []
    for x in range(0, len(years)):
        z = team_offense_site[i].replace('2020',years[x])
        y = team_defense_site[i].replace('2020',years[x])
        t = team_turnover_site[i].replace('2020',years[x])
        time.sleep(.3)
        req1 = requests.get(z)
        
        #req2 = requests.get(y)
        if req1.status_code == 2000:
            #offense_year.append(z)
            sub.append(z)
            #y = z.replace('offense','defense')            
            #defense_year.append(y)
            sub1.append(y)
            sub2.append(t)            
    o_array.append(sub)
    d_array.append(sub1)
    t_array.append(sub2)

o_dict = {}
d_dict = {}
t_dict = {}

i = 0
for i in range(0, len(team)):
    o_dict[team[i]] = o_array[i]
    d_dict[team[i]] = d_array[i]
    t_dict[team[i]] = t_array[i]

z1 =[]
for teams, site in o_dict.items():
    z = 'df_'+str(teams)
    i = 0
    for i in range(0, len(site)):
        url_x = site[i]
        page = requests.get(url_x)
        pagetext = page.text
        soup1 = bs(pagetext, 'html.parser')
        table = soup1.find_all('table')
        df = pd.read_html(str(table), header = 0)
        df1 = df[0]
        df1 = df1.dropna(subset =['Result'])
        df1 = df1[:-1]
        team_col = []
        for index, rows in df1.iterrows():
            team_col.append(teams)
        df1['Team'] = team_col
        z1.append(df1)
        
z2=[]        
for teams, site in d_dict.items():
    z = 'df_'+str(teams)    
    i = 0
    for i in range(0, len(site)):
        url_x = site[i]
        page = requests.get(url_x)
        pagetext = page.text
        soup1 = bs(pagetext, 'html.parser')
        table = soup1.find_all('table')
        df = pd.read_html(str(table), header = 0)
        df1 = df[0]
        df1 = df1.dropna(subset =['Result'])
        df1 = df1[:-1]
        team_col = []
        for index, rows in df1.iterrows():
            team_col.append(teams)
        df1['Team'] = team_col
        z2.append(df1)


z3=[]        
for teams, site in t_dict.items():
    z = 'df_'+str(teams)    
    i = 0
    for i in range(0, len(site)):
        url_x = site[i]
        page = requests.get(url_x)
        pagetext = page.text
        soup1 = bs(pagetext, 'html.parser')
        table = soup1.find_all('table')
        df = pd.read_html(str(table), header = 0)
        df1 = df[0]
        df1 = df1.dropna(subset =['Result'])
        df1 = df1[:-1]
        team_col = []
        for index, rows in df1.iterrows():
            team_col.append(teams)
        df1['Team'] = team_col
        z3.append(df1)                
    
i = 0
merge_o =[]
merge_d =[]
merge_t =[]

temp=[]
temp1=[]
temp2=[]
for i in range(1, len(z1)):
    if z1[i]['Team'].any()==z1[i-1]['Team'].any():
        temp.append(z1[i-1])
        temp1.append(z2[i-1])
        temp2.append(z3[i-1])
    else:
        temp.append(z1[i-1])
        temp1.append(z2[i-1])
        temp2.append(z3[i-1])
        df_o = pd.concat(temp)
        df_d = pd.concat(temp1)
        df_t = pd.concat(temp2)
        df_d.rename(columns={"Rush Yards":"Rush Yards Allowed","Pass Yards":"Pass Yards Allowed",
                                              "Plays":"Plays Allowed", "Total Yards":"Total Yards Allowed", "Yards/Play":"Yards/Play Allowed"},
                                              inplace = True)
        merge_o.append(df_o)
        merge_d.append(df_d)
        merge_t.append(df_t)
        temp = []
        temp1=[]
        temp2=[]
      

i = 0
merge_list = []
for i in range(0, len(merge_o)):
    j = 0
    for j in range(0, len(merge_d)):   
        if merge_o[i]['Team'].any() == merge_d[j]['Team'].any():
            merge_df = pd.merge(merge_o[i], merge_d[j], on = ['Date','Team','Surface','Result','Opponent'])
            new = merge_df["Result"].str.split("-", n=1, expand = True)
            merge_df["Team Score"] = new[0].str[1:]
            merge_df["Opponent Score"] = new[1]
            merge_df.drop(columns = ["Result"], inplace = True)
            merge_list.append(merge_df)

i = 0
final_merge_list = []
for i in range(0, len(merge_list)):
    y = 0
    for y in range(0, len(merge_t)):
        if merge_list[i]['Team'].any() == merge_t[y]['Team'].any():
            final_merge = pd.merge(merge_list[i], merge_t[y], on = ['Date','Team','Surface'])
            final_merge.drop(columns = ["Result","Opponent_y"],inplace=True)
            final_merge_list.append(final_merge)



            
for i in range(0, len(final_merge_list)):
    y = final_merge_list[i]['Team'].iloc[0]
    z = r'C:\Users\charl\Desktop\KSDM Analytics\College Football\Stats\%s.csv'%y
    export = final_merge_list[i].to_csv(z)

print("--- %s seconds ---" % (time.time() - start_time))
#dfx = final_merge_list[90]       
#dfx.set_index('Date', inplace=True)
#dfx.plot(subplots=True)
#plt.title(final_merge_list[90])
#plt.show

#for team in merge_list:
#    dfp = team
#    dfp.set_index('Date', inplace = True)
#    dfp.plot(subplots=True)
#    plt.show()