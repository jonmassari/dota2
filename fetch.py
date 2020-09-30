# fetch.py
# Gather team data every morning at 5:00 am eastern time
# This will prevent excessive load times and allow teams to be selected from a dropdown

import requests
import os
from bs4 import BeautifulSoup
import json

rd2l_teams_soup = BeautifulSoup(requests.get("https://rd2l.gg/seasons/KrCaUz6OO/divisions/U-ZTEMOBg/teams").content, "html.parser")
teams=[]
rd2l_base= "https://rd2l.gg"
team_tds = rd2l_teams_soup.findAll("td")




# Heroes List for Hero_ID -> Hero Name
heroes={}
response=requests.get("https://api.opendota.com/api/heroes?api_key=beebcc94-9bf5-467a-bc7e-d4522ec0638f")
for hero in response.json():
    heroes.update({hero['id']:hero['localized_name']})

api_key = "&api_key=beebcc94-9bf5-467a-bc7e-d4522ec0638f"
current_patch = "?patch=46"
opendota_base = "https://api.opendota.com/api/"
heroes_footer = "/heroes" + current_patch + api_key


# Clear File before appending new teams
# This should just rename the file probably

f = open("teams.json","w")
f.write("")
f.close()

end_json = []
for team in team_tds:
    if team.a != None:

        team_link=rd2l_base + str(team.a['href'])
        team_soup = BeautifulSoup(requests.get(team_link).content, 'html.parser')
        # Get all Player Info
        players=[]
        # Get Captain from RD2L Page
        captain = team_soup.body.findAll("div", {"class", "content"})
        for item in captain:
            players.append([item.a.text, item.a['href'].replace("profile","players")])
        # Get Players from RD2L Page
        tds = team_soup.body.findAll('td')
        for item in tds:
            if item.a != None and 'profile' in item.a['href']:
                players.append([item.a.text, item.a['href'].replace("profile","players")])
        # Append Hero Data to Players Array
        for player in players:
            url = opendota_base + player[1] + heroes_footer
            response=requests.get(url)
            player.append(response.json()[0:9])
            for item in player[2]:
                item["hero"] = heroes[int(item['hero_id'])]

        # Get Recent RD2L Drafts from Captain
        matches=[]
        drafts_footer = str(players[0][1]) + "/matches?lobby_type=1&date=30&game_mode=2" + api_key
        drafts=requests.get(opendota_base+drafts_footer)
        for match in drafts.json():
            match_id=str(match['match_id'])
            match_endpoint="https://api.opendota.com/api/matches/" + match_id + "?api_key=beebcc94-9bf5-467a-bc7e-d4522ec0638f"
            match_response=requests.get(match_endpoint)
            if match_response.json()['leagueid'] == 12384:
                matches.append(match_response.json())
        team_header = team.a.text + team.span.text
        team_data = {
            'header':team_header,
            'matches':matches,
            'players':players,
            'heroes':heroes
        }
        end_json.append(team_data)
        print ("teams file")
        for item in end_json:
        	print(item['header'])
        print("\n")
with open('teams.json', 'a', encoding="utf-8") as teams_file:
    json.dump(end_json, teams_file)
