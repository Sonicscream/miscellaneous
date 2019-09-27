from socket import *

def query(ip, port):
	connection = socket(AF_INET, SOCK_DGRAM)

	payload = '\\query'.encode()
	connection.sendto(payload,(ip,port))

	result = connection.recvfrom(10240)[0]

	resultList = result.decode("utf-8","ignore").split('\\')
	resultList.pop(0) # Split creates an empty useless '' at 0


	""" What it looks like when it comes in after splitting before popping
	['', hostname',	'CRYPTOCLOVER.CC',
	'gamever', '01.00.10.0621',
	'hostport', '',
	'maxplayers', '16',
	'password', '0',
	'mapname', 'Bloodgulch',
	'dedicated', '1',
	'gamemode', 'openplaying',
	'game_classic', '1',
	'numplayers', '16',
	'gametype', 'CTF',
	'teamplay', '1',
	'gamevariant', 'cc_infinite_ctf',
	'fraglimit', '1000000',
	'player_flags', '1263534084,1094',
	'game_flags', '65',
	'player_0', 'namehere', 'player_1', '...'
	'score_0', '2', 'score_1', ...
	'ping_0', '123', 'ping_1', ...
	'team_0', '1', 'team_1', ...
	'team_t0', 'Red', 'team_t1', 'Blue',
	'score_t0', '2', 'score_t1', '1',
	'final', '',
	'queryid', '1.1']
	"""

	resultDict = {}
	for i in range(len(resultList)):
		if i % 2:
			continue
		resultDict[resultList[i]] = resultList[i+1]

	data = {}
	players = {}
	for key, value in resultDict.items():
		if key == 'hostname':
			data['name'] = value
		elif key == 'gamever':
			data['version'] = value
		elif key == 'password':
			data['passwordEnabled'] = value
		elif key == 'maxplayers':
			data['playersMax'] = value
		elif key == 'mapname':
			data['map'] = value
		elif key == 'numplayers':
			data['playersCurrent'] = value
		elif key == 'gametype':
			data['mode'] = value
		elif key == 'teamplay':
			data['teamsEnabled'] = value
		elif key == 'score_t0':	# Red team score
			if not 'teamRed' in data:
				data['teamRed'] = {}
			data['teamRed']['score'] = value
		elif key == 'score_t1':	# Blue team score
			if not 'teamBlue' in data:
				data['teamBlue'] = {}
			data['teamBlue']['score'] = value
		elif key[0:7] == 'player_' and len(key) <= 9:
			ID = key[7:]
			Name = value
			if not ID in players:
				players[ID] = {}
			players[ID]['name'] = Name
			continue
		elif key[0:6] == 'score_':
			ID = key[6:]
			if ID[0] == 't':
				continue
			Score = value
			if not ID in players:
				players[ID] = {}
			players[ID]['score'] = Score
			continue
		elif key[0:5] == 'ping_':
			ID = key[5:]
			Ping = value
			if not ID in players:
				players[ID] = {}
			players[ID]['ping'] = Ping
			continue
		elif key[0:5] == 'team_':
			ID = key[5:]
			if ID[0] == 't':
				continue
			Team = value
			if not ID in players:
				players[ID] = {}
			players[ID]['team'] = Team
			continue
	data['players'] = players
	return data


result = query('147.135.79.54',10000)
for key, value in result['players'].items():
	print(key + ' : ' + value['name'])
