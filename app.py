
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as pe
import streamlit as st
import re

st.title("Velogames - FFUL No Espaço")

n_races = range(1,23)
teams_ids = ["6a6fe74af33f3c7472747ad28969aacb2dj","62522cbfe801a3d2f454f43c402fb0b23dp","63ff914b9d0b5515"]
dic_id = {"6a6fe74af33f3c7472747ad28969aacb2dj":"Team Reality Check","62522cbfe801a3d2f454f43c402fb0b23dp" : "Horizonte Team","63ff914b9d0b5515" : "Team Raya"}

race = []
points = []
team_id = []
date = []
cumulative = 0

for i in n_races:
    for code in teams_ids:
        ###General Request
        initial_request = requests.get("https://www.velogames.com/sixes-superclasico/2023/teamroster.php?tid={}&ga=13&st={}".format(code,i))
        soup = BeautifulSoup(initial_request.content, 'html.parser')
        
        ###Scrapping points and name
        scrap_race = soup.find("ul",class_="popular-posts")
        content_race = scrap_race.find_all('li')
        result = str(content_race[3])
        
        ###Regex of race
        pattern_Score = "<b>" + "(.+?)"  + "</b"
        score = re.search(pattern_Score,result).group(1)
        pattern_Race = "<li>" + "(.+?)"  + ":"
        Race = re.search(pattern_Race,result).group(1)

        ###Scrapping Date
        scrap_date= soup.find("div",class_="subcategories-carousel")
        content_date = scrap_date.find_all("div",class_="subcategory-item")
        date_str = str(content_date[i])

        ###Regex of date###
        pattern_date = "</b><br/>" + "(.+?)"  + " "
        date_final = re.search(pattern_date,date_str).group(1)

        ###Creating dataset###
        race.append(Race)
        points.append(score)
        team_id.append(code)
        date.append(date_final)

bd=pd.DataFrame({"ID":team_id,"Race":race,"Score":points,"Date":date})
bd.ID=bd.ID.replace(dic_id)
bd.Score = bd.Score.astype(int)
bd["Cumulative"]=bd["Score"].groupby(bd["ID"]).cumsum()
bd.Date = bd.Date.apply(lambda x : datetime.strptime(x, "%Y-%m-%d"))


graph_pontos = pe.line(data_frame = bd, x="Date", y="Cumulative",color="ID")

st.plotly_chart(graph_pontos,use_container_width=True,theme="streamlit")
