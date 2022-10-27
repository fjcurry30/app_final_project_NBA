import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')

df_oringin1 = pd.read_csv('all_seasons.csv')
df_oringin2 = df_oringin1.drop(['num', 'oreb_pct', 'dreb_pct', 'usg_pct', 'ts_pct', 'ast_pct'], axis=1)
df_oringin3 = df_oringin2[df_oringin2.draft_number != 'Undrafted']
df_oringin3['draft_number'] = df_oringin3['draft_number'].apply(lambda x : int(x))
df_oringin3['age'] = df_oringin3['age'].apply(lambda x : int(x))
df_oringin3['draft_round'] = df_oringin3['draft_round'].apply(lambda x : int(x))
df_oringin3['draft_year'] = df_oringin3['draft_year'].apply(lambda x : int(x))
df_oringin4 = df_oringin3.sort_values(['draft_round', 'draft_number'], ascending=[True, True])
df = df_oringin3.sort_values(['draft_round', 'draft_number'], ascending=[True, True])


st.title('MISY225 Final Project Based On NBA PLAYERS')
st.write('Group members: *Haotian Lan*, *Yuzhuo Xie*') 

a = df['draft_year'].tolist()
b = list(set(a))
c = sorted(b)
latest_year = df[df.draft_year != 'Undrafted'].draft_year.max()

d = df['team_abbreviation'].tolist()
e = list(set(d))

st.subheader('The chart below is sorted by drafted rounds and numbers by default')

form = st.form("name_form")
name_filter = form.text_input('Name (enter ALL to reset)', 'ALL')
form.form_submit_button("Apply")

if name_filter != 'ALL':
    df = df[df.player_name == name_filter]

year_filter = st.sidebar.multiselect('Select one year you want to check', c, latest_year)
if len(year_filter) >= 2:
    df = df[df.draft_year.isin(year_filter)].sort_values(['draft_year', 'draft_round', 'draft_number'], ascending=[False, True, True])
else:
    df = df[df.draft_year.isin(year_filter)]

team_abbreviation_filter = st.sidebar.multiselect('Select one team you want to check', e, e)
df = df[df.team_abbreviation.isin(team_abbreviation_filter)]


form = st.sidebar.form("nationality_form")
nationality_filter = form.text_input('Nation (enter ALL to reset)', 'ALL')
form.form_submit_button("Apply")

if nationality_filter != 'ALL':
    df = df[df.country == nationality_filter]

st.write(df)

st.subheader('Line chart of the average age of each year:')
fig, ax = plt.subplots()
df_averge_age = df_oringin4.groupby('draft_year')['age'].sum() / df_oringin4.draft_year.value_counts()
df_averge_age.plot(ax=ax, linestyle='solid', marker='o', color='green')
ax.set_xlabel('Year')
ax.set_ylabel('Averge Age')
'Question'
st.text('Does the NBA Draft have anything to do with age?')
'Conclusion'
st.text('This line chart has some erro. As you can see there are missing data from 1964 to 1975.\nBesides, there is only one data for year 1963 which makes the average age inaccurate.\nBut, it is easy for us to find that  NBA draft picks get younger and younger!!!')
st.pyplot(fig)

st.subheader('Line chart average points scored by NBA rookies each year:')
fig, ax = plt.subplots()
df_averge_pts = df_oringin4.groupby('draft_year')['pts'].sum() / df_oringin4.draft_year.value_counts()
df_averge_pts.plot(ax=ax, linestyle='dotted', marker='s', color='blue')
ax.set_xlabel('Year')
ax.set_ylabel('Averge Points')
'Conclusion'
st.text('From the chart below, we can see that before 1982, NBA rookies\' averages generally had lower scores.\nEspecially in 1979, the average scores of NBA rookies reached a minimum of 0.6 points.\nThe average scores of NBA rookies increased sharply in 1982, and has remained between 7 and 11 points since 1982.\nWe can see from this chart that the average score of NBA rookies has continued to improve over time, which can also indirectly indicate that the basketball training system is becoming more and more mature.\nMost people have also improved their basketball skills.')
st.pyplot(fig)


st.subheader('Bar chart of the percentage of NBA rookies from the United States each year:')
fig, ax = plt.subplots()
df_1 = df_oringin4[df_oringin4.country == 'USA']
df_2 = df_1.draft_year.value_counts() / df_oringin4.draft_year.value_counts()
df_2.plot.bar(ax=ax, color='red')
'Conclusion'
st.text('The y axis of the bar chart shows the percentage of NBA rookies from the United States per year, and the x axis shows the year.\nIn general, a large percentage of NBA rookies each year are from the United States.\nBut in recent years, NBA rookies have become more multinational than in previous decades, with more players from abroad entering the NBA draft.')
st.pyplot(fig)


st.subheader('Box chart of the percentage of NBA rookies from the United States each year:')
minmum = df_oringin4.draft_year.min() 
maximum = df_oringin4.draft_year.max()
fig, ax = plt.subplots()
pop_year_filter = st.slider('Select one year you want to check', 1963, 2021, 2021)
df_year = df_oringin4[df_oringin4.draft_year == pop_year_filter]
df_year.player_height.plot.box(ax=ax)
'Question'
st.text('At what height range are you more likely to be drafted by the NBA?')
'Conclusion'
st.text('According to the box chart below, we can see that most players drafted by the NBA are in the range of 195cm to 206cm in 2021.\nThe average height is about 201cm in 2021.\nAccording to the annual box chart, we find an interesting phenomenon.\nThe average player drafted in the NBA every year is about two meters tall. This shows that in the NBA, which has the highest level of basketball in the world, two-meter players are preferred')
st.pyplot(fig)

st.subheader('Bar chart of the height of the top pick in the NBA draft each year:')
fig, ax = plt.subplots()
df_number_one = df_oringin4.sort_values(['draft_year'], ascending=[True])[(df_oringin4.draft_round == 1) & (df_oringin4.draft_number == 1)]
df_every_number_one = df_number_one.drop_duplicates(subset='player_name', keep='first')
df_every_number_one.player_height.plot.bar(ax=ax, color='red')
ax.set_xticklabels(df_every_number_one.draft_year)
ax.set_xlabel('Top pick in the NBA draft every year')
ax.set_ylabel('Height')
'Question'
st.text('In the previous question, we found that the average NBA draft player is about two meters tall.\nDoes the height of the top NBA draft pick each year also prove this phenomenon?')
'Conclusion'
st.text('According to the bar chart below, we can see that the height of the NBA top draft pick every year is about two meters.\nFew top NBA draft pick are shorter than 2 meters.\nIt also confirms what we already suspected -- that the NBA prefers players who are about two feet tall')
st.pyplot(fig)

st.subheader('Bar chart of the net rating of the top pick in the NBA draft each year:')
fig, ax = plt.subplots()
df_every_number_one.net_rating.plot.bar(ax=ax, color='green')
ax.set_xticklabels(df_every_number_one.draft_year)
ax.set_xlabel('Top pick in the NBA draft every year')
ax.set_ylabel('Height')
'Conclusion'
st.text('As the NBA is the best basketball league in the world, we all take it for granted that the top pick in the NBA draft each year will give us amazing performance.\nBut when we look at the bar chart below, we are surprised to find that nearly half of the top pick in the NBA draft have poor performance.\nIt also tells us that being the top pick in the NBA draft every year doesn\'t always mean being No. 1. Just as an old saying goes, \"There is a universe outside everyone.\"')
st.pyplot(fig)