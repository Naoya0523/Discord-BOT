import requests
import time

#RiotのAPIキー
api_key = ''

def get_puuid(summoner_name, api_key=api_key, region="jp1"):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    data = requests.get(url)
    player_info = data.json()
    puuid = player_info['puuid']
    return puuid

def get_win_rate(win_or_lose):
    win_count = 0
    for win in win_or_lose:
        if win:
            win_count += 1
        else:
            pass

    win_rate = win_count/len(win_or_lose)
    return win_rate

def get_average_scores(summoner_name,api_key=api_key, region="jp1", start=0, count=10):
    print("sleep 1 sec")
    time.sleep(1)

    puuid = get_puuid(summoner_name, api_key, region)
    matches_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=normal&start={start}&count={count}&api_key={api_key}"
    respons = requests.get(matches_url)
    if respons.status_code == 200:
        print('scucces')
        matches_number_list = respons.json()
    else:
        print('error')
        return

    _match = matches_number_list[0]
    match_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{_match}/?api_key={api_key}"
    respons = requests.get(match_url)
    if respons.status_code == 200:
        print('match loaded')
        match_data = respons.json()
    else:
        print('match error')
        return

    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)

    if 0 <= player_index < 5:
        team_index_list = [0, 1, 2, 3, 4]
    else:
        team_index_list = [5, 6, 7, 8, 9]


    player_data = match_data['info']['participants'][player_index]
    kills = player_data['kills']
    print(f'kills = {kills}')
    assists = player_data['assists']
    print(f'assists = {assists}')

    team_kills = 0
    for i in team_index_list:
        team_kills += match_data['info']['participants'][i]['kills']

    killInvolvementRate = (kills + assists)/team_kills
    print(killInvolvementRate)