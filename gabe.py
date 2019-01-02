import re
import requests


#  Change this to be the bracket you want to get character data from

bracketURL = "https://smash.gg/tournament/battle-arena-melbourne-10/events/wii-u-singles/brackets/259927/575722"


# ugly stuff below


def getURLParams(url):
		urlInfo = re.match('https?://smash.gg/tournament/(?P<tournament>.+)/events?/(?P<event>.+)/brackets/\d+/(?P<phaseID>\d+)', url).groupdict()
		[tournament, event, phaseID] = urlInfo['tournament'], urlInfo['event'], urlInfo['phaseID']
		return tournament, event, phaseID

[tournament, event, phaseID] = getURLParams(bracketURL)

json 	= requests.get("https://api.smash.gg/phase_group/%s?expand[]=sets&expand[]=seeds&expand[]=character" % phaseID).json()


players = {}
matches = {}
chars = {}

seeds 	= json['entities']['seeds']
sets 	= json['entities']['sets']

characters = json['entities']['character']

# 1=> Single Elim, 2=> Double Elim, 3=> Round Robin
groupType = int(json['entities']['groups']['groupTypeId'])

# Gets the characterIDs smash.gg uses for whatever game (e.g. for Rivals Zetterburn is characterID 184)
for character in characters:
	characterID 	= character['id']
	characterName	= character['name']

	chars[characterID] = characterName
#Ties the playerIDs used in bracket to actual player names
for player in seeds:
	playerID 		= int(player['entrantId'])
	playerSeed 		= int(player['seedNum'])
	playerFinalRank	= 99999999

	if not playerID in players:
		info 		= list(player['mutations']['players'].values())[0]
		playerName 	= info['gamerTag']
		state 		= info['state']
		country 	= info['country']

		players[playerID] = {	'playerName': playerName, 'playerSeed': playerSeed, 'playerFinalRank': playerFinalRank,
								'state': state, 'country': country}
#Goes through all the sets in the bracket and gets the character data
for match in sets:
	matchID = match['id']

	if not matchID in matches:
		if match['entrant1Id'] != None and match['entrant2Id'] != None and match['winnerId'] != None and match['loserId'] != None:
			player1ID		= match['entrant1Id']
			player1Name		= players[player1ID]['playerName']
			player1Char		= "-"
			if  'entrant1CharacterIds' in match:
				player1Char		= chars[int(match['entrant1CharacterIds'][0])]

			player2ID		= match['entrant2Id']
			player2Name		= players[player2ID]['playerName']
			player2Char		= "-"
			if  'entrant2CharacterIds' in match:
				player2Char		= chars[int(match['entrant2CharacterIds'][0])]

			time			= match['completedAt']
	
			matches[matchID] = {'player1Name': player1Name, 'player2Name': player2Name, 'player1Char': player1Char, 'player2Char': player2Char, 'time': time}

out = list(matches.values())
out.sort(key=lambda x: x['time'])
for val in out:
	p1 	= val['player1Name']
	p1C = val['player1Char']
	p2 	= val['player2Name']
	p2C = val['player2Char']
	print("%s,%s,%s,%s" % (p1, p1C, p2, p2C) )