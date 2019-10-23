from html.parser import HTMLParser

from flask import Flask, render_template, jsonify, request  # import objects from the Flask model
from lxml import html
import requests

# Create the application instance
app = Flask(__name__)

# Url declaration
reg_url = 'https://www.metacritic.com/game/playstation-4'


# Opens up connection and grab headers
# req = request(url=reg_url, headers=headers)
def get_map_games_scores():
    result = requests.get(reg_url, headers={'user-agent': 'Mac Firefox', 'Accept': 'html/text'})

    tree = html.fromstring(result.text)
    games = tree.xpath('//td[@class="clamp-summary-wrap"]//a//h3')
    scores = tree.xpath('//td[@class="clamp-summary-wrap"]//div[@class="clamp-score-wrap"]/a/div')
    result = dict()
    for i in range(len(games)):
        result[(games[i].text).strip()] = int((scores[i].text).strip())
    return result

# Create a URL route in our application for "/"
@app.route('/games', methods=['GET'])
def get_all_scores():  # This function returns top PS4 games on metacritic
    knowledge = get_map_games_scores()
    result = []
    for game, score in knowledge.items():
        result.append({'title':game,'score':score})
    return str(result)
    # Create a URL route in our application for "/"
@app.route('/games/<string:query>', methods=['GET'])
def get_game_score(query=None):
    knowledge = get_map_games_scores()
    query_format = html.unicode(query)
    if query_format not in knowledge:
        return "404"
    result = {'game': query_format, 'score':knowledge[query]}
    return result

#   if request.method == 'GET':
#  	attempted_game = request.td['clamp-summary-wrap']
# 	if attempted_game == "attempted_game":
#		return redirect(url_for('game'))
#    	div.a.title.h3
# return jsonify({'message' : 'It works!'})
def main():
    app.run(port=5000, debug=True)
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    main()