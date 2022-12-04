import pandas as pd


data = pd.read_csv("international_matches.csv")
data = data[["home_team","away_team","home_team_result","date"]]

#Any draws break the winning streak of both teams involved
#Draws perceived as losses by both sides
data.insert(column="away_team_result",loc=3,value="Lose")
data.loc[data["home_team_result"] == "Lose", 'away_team_result'] = 'Win' 
data.loc[data["home_team_result"] == "Draw", 'home_team_result'] = 'Lose'

#Split data to home and away, rename to standardize
awayData = data[["away_team","away_team_result","date"]]
awayData = awayData.rename(columns={"away_team": "team", "away_team_result": "result"})
homeData = data[["home_team","home_team_result","date"]]
homeData = homeData.rename(columns={"home_team": "team", "home_team_result": "result"})

#Create one dataset treating each team separately with team, result, and date
data = pd.concat([homeData,awayData])

#Sort table by team name with each team's matches in chronological order
data = data.sort_values(by = ['team', 'date'], ascending = [True, True])

#Increment streak counter for each consecutive matching value
data['streak'] = data['result'].groupby((data['result'] != data.groupby(['team'])['result'].shift()).cumsum()).cumcount() + 1

#Override all losses to have a streak of 0
data.loc[data["result"] == "Lose", 'streak'] = 0 

#Sort table by team name with each team's win streaks listed highest first
data = data.sort_values(by = ["team", "streak"], ascending = [True, False])

#Drop duplicates based on team name, keeping only first entry which contains highest streak by our previous sorting step
data = data.drop_duplicates(subset="team")

#Sort table by team name with each team's win streaks listed highest first
data = data.sort_values(by = ["streak"], ascending = [False])
print(data.iloc[0]['team'])

print('%.2f' % data['streak'].mean())

#Output to easily review all data
data.to_csv("output.csv")