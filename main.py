import datetime
import requests
from bs4 import BeautifulSoup
import re
import time
import json
from flask import Flask, render_template, url_for, redirect, flash
from forms import RD2LForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e4e895d495ab39301b88457d72968508'

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    form = RD2LForm()
    if form.validate_on_submit():
        flash('Scout em and route em', 'success')
        return redirect(url_for('root'))
    return render_template('home.html', title='Home', form=form)

@app.route('/rd2l', methods=['GET','POST'])
def root():
    form = RD2LForm()
    if form.validate_on_submit():
        with open('teams.json','r', encoding='utf-8') as teams_file:
            team_json = json.load(teams_file)
            for team_data in team_json:
                if team_data['header'] == form.team_select.data:
                    return render_template('scout.html', form=form, players=team_data['players'], matches=team_data['matches'], header=team_data['header'], heroes=team_data['heroes'] )
    else:
        return render_template('scout.html', form=form)
    
    """
    players=[]
    heroes={}
    matches=[]
    form = RD2LForm()

    response=requests.get("https://api.opendota.com/api/heroes?api_key=beebcc94-9bf5-467a-bc7e-d4522ec0638f")
    for hero in response.json():
        heroes.update({hero['id']:hero['localized_name']})

    api_key = "&api_key=beebcc94-9bf5-467a-bc7e-d4522ec0638f"
    current_patch = "?patch=46"
    opendota_base = "https://api.opendota.com/api/"
    heroes_footer = "/heroes" + current_patch + api_key
    
    
    if form.validate_on_submit():
        team_link = form.rd2l_url.data
        team_page = requests.get(team_link)
        soup = BeautifulSoup(team_page.content, 'html.parser')

        # Get Captain from RD2L Page
        captain = soup.body.findAll("div", {"class", "content"})
        for item in captain:
            players.append([item.a.text, item.a['href'].replace("profile","players")])

        # Get Players from RD2L Page
        tds = soup.body.findAll('td')
        for item in tds:
            if item.a != None and 'profile' in item.a['href']:
                players.append([item.a.text, item.a['href'].replace("profile","players")])
            else:
                # Append Hero Data to Players Array
                for player in players:
                    url = opendota_base + player[1] + heroes_footer
                    response=requests.get(url)
                    player.append(response.json()[0:9])
                    for item in player[2]:
                        item["hero"] = heroes[int(item['hero_id'])]

        # Get Recent RD2L Drafts from Captain
        drafts_footer = str(players[0][1]) + "/matches?lobby_type=1&date=30&game_mode=2" + api_key
        drafts=requests.get(opendota_base+drafts_footer)
        for match in drafts.json():
            match_id=str(match['match_id'])
            match_endpoint="https://api.opendota.com/api/matches/" + match_id + "?api_key=beebcc94-9bf5-467a-bc7e-d4522ec0638f"
            match_response=requests.get(match_endpoint)
            if match_response.json()['leagueid'] == 12384:
                matches.append(match_response.json())
    return render_template('scout.html', players=players, heroes=heroes, form=form, matches=matches)
    """

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)