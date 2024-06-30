import requests
import time
import pandas
from riot_api import get_puuid
from data_by_position import get_data_by_position, get_all_data_by_positions
import os
import glob

api_key = ''


def get_all_summoners():
    path = 'excel files/'
    summoner_excel = os.path.join(path, '*.xlsx')
    summoner_excel_files = glob.glob(summoner_excel)
    return summoner_excel_files


def get_all_data():
    all_data = pandas.DataFrame()
    path = 'excel files'

    summoner_excel = os.path.join(path, '*.xlsx')
    summoner_excel_files = glob.glob(summoner_excel)
    for file in summoner_excel_files:
        data = pandas.read_excel(file)
        all_data = pandas.concat([all_data, data], ignore_index=True)

    all_data.to_excel('excel files/all datas/all_data.xlsx', index=False)
    get_all_data_by_positions()


def get_KDA(kills, assists, deaths):
    if deaths == 0:
        deaths = 1
    kda = (kills + assists)/deaths
    kda = round(kda, 2)
    return kda

def get_kill_Inovement_Rate(match_data, player_index):
    if 0 <= player_index < 5:
        team_index_list = [0, 1, 2, 3, 4]
    else:
        team_index_list = [5, 6, 7, 8, 9]


    player_data = match_data['info']['participants'][player_index]
    kills = player_data['kills']
    assists = player_data['assists']

    team_kills = 0
    for i in team_index_list:
        team_kills += match_data['info']['participants'][i]['kills']

    if team_kills == 0:
        team_kills = 1
    killInvolvementRate = (kills + assists)/team_kills
    killInvolvementRate = round(killInvolvementRate, 2)
    return killInvolvementRate

def export_excel_file(summoner_name, api_key=api_key, region='jp1', start=0, count=100):
    print('sleep 1 second to get access to riot api')
    print(f"loading {summoner_name}'s data")
    time.sleep(1)

    puuid = get_puuid(summoner_name, api_key, region)
    matches_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=430&type=normal&start={start}&count={count}&api_key={api_key}"
    matches_list = list(requests.get(matches_url).json())

    print(f'matches list length is {len(matches_list)}')

    #100試合以上データがない場合、初期のマッチはおかしなデータが返ってくるので除外する
    if 10 < len(matches_list) < 99:
        for _ in range(10):
            matches_list.remove(matches_list[len(matches_list)-1])
    elif len(matches_list) != 100:
        print("under 10 matches. you can't get accurate data")
        return

    match_data_for_excel = {}
    match_data_for_excel['matchID'] = matches_list

    summonerName = []
    summonerLevel = []
    championName = []
    kills = []
    deaths = []
    assists = []
    kda = []
    killInovementRate = []
    totalDamageDealtToChampions = []
    damageDealtToTurrets = []
    totalMinionsKilled = []
    visionScore = []
    teamPosition = []
    individualPosition = []
    win = []
    gameEndedInEarlySurrender = []
    gameDuration = []
    damage_pre_min = []
    cs_pre_min = []
    goldEarned = []
    goldEarned_pre_min = []


    load_count = 0
    start_time = time.time()
    start_time2 = time.time()
    for _match in matches_list:
        load_count += 1
        match_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{_match}/?api_key={api_key}"
        match_data = requests.get(match_url).json()

        if load_count % 10 == 0:
            end_time = time.time()
            wait_time = end_time - start_time
            wait_time = round(wait_time, 2)
            start_time = time.time()
            print(f"\033[34;1m{load_count}\033[0m match loaded    time : \033[32;1m{wait_time}\033[0m")

        if load_count % 90 == 0:
            end_time2 = time.time()
            wait_time2 = round(122 - (end_time2 - start_time2), 2)
            print(f'about 90 times send api requests. please wait \033[32;1m{wait_time2}\033[0m seconds')
            time.sleep(wait_time2)
            start_time = time.time()

        #player info
        participants = match_data['metadata']['participants']
        player_index = participants.index(puuid)
        player_data = match_data['info']['participants'][player_index]

        match_summonerName = player_data['summonerName']
        summonerName.append(match_summonerName)

        match_summonerLevel = player_data['summonerLevel']
        summonerLevel.append(match_summonerLevel)

        #bool objects
        match_gameEndedInEarlySurrender = player_data['gameEndedInEarlySurrender']
        gameEndedInEarlySurrender.append(match_gameEndedInEarlySurrender)

        match_win = player_data['win']
        win.append(match_win)

        #positions and champion objects
        match_individualPosition = player_data['individualPosition']
        individualPosition.append(match_individualPosition)

        match_champion = player_data['championName']
        championName.append(match_champion)

        match_teamPosition = player_data['teamPosition']
        teamPosition.append(match_teamPosition)

        #timestamp objects
        match_gameDuration = match_data['info']['gameDuration']
        gameDuration.append(match_gameDuration)

        #int or float objects
        match_kills = player_data['kills']
        kills.append(match_kills)

        match_assists = player_data['assists']
        assists.append(match_assists)

        match_deaths = player_data['deaths']
        deaths.append(match_deaths)

        match_totalDamageDealtToChampions = player_data['totalDamageDealtToChampions']
        totalDamageDealtToChampions.append(match_totalDamageDealtToChampions)

        match_totalMinionsKilled = player_data['totalMinionsKilled']
        totalMinionsKilled.append(match_totalMinionsKilled)

        match_visionScore = player_data['visionScore']
        visionScore.append(match_visionScore)

        match_goldEarned = player_data['goldEarned']
        goldEarned.append(match_goldEarned)

        match_damageDealtToTurrets = player_data['damageDealtToTurrets']
        damageDealtToTurrets.append(match_damageDealtToTurrets)

        match_killInovementRate = get_kill_Inovement_Rate(match_data, player_index)
        killInovementRate.append(match_killInovementRate)

        #CS/min and Damage/min and gold
        if match_gameDuration == 0:
            match_gameDuration = 1

        match_Damage_pre_min = match_totalDamageDealtToChampions/(match_gameDuration/60)
        match_Damage_pre_min = float(round(match_Damage_pre_min, 2))
        damage_pre_min.append(match_Damage_pre_min)

        match_cs_pre_min = match_totalMinionsKilled/(match_gameDuration/60)
        match_cs_pre_min = float(round(match_cs_pre_min, 2))
        cs_pre_min.append(match_cs_pre_min)

        match_goldEarned_pre_min = match_goldEarned/(match_gameDuration/60)
        match_goldEarned_pre_min = float(round(match_goldEarned_pre_min, 2))
        goldEarned_pre_min.append(match_goldEarned_pre_min)

        #KDA
        match_kda = get_KDA(match_kills, match_assists, match_deaths)
        kda.append(match_kda)

    match_data_for_excel['summonerName'] = summonerName
    match_data_for_excel['summonerLevel'] = summonerLevel
    match_data_for_excel['win'] = win
    match_data_for_excel['gameEndedInEarlySurrender'] = gameEndedInEarlySurrender
    match_data_for_excel['championName'] = championName
    match_data_for_excel['teamPosition'] = teamPosition
    match_data_for_excel['kills'] = kills
    match_data_for_excel['deaths'] = deaths
    match_data_for_excel['assists'] = assists
    match_data_for_excel['KDA'] = kda
    match_data_for_excel['killInovementRate'] = killInovementRate
    match_data_for_excel['damageDealtToTurrets'] = damageDealtToTurrets
    match_data_for_excel['visionScore'] = visionScore
    match_data_for_excel['totalMinionskilled'] = totalMinionsKilled
    match_data_for_excel['totalDamageDealtToChampions'] = totalDamageDealtToChampions
    match_data_for_excel['goldEarned'] = goldEarned
    match_data_for_excel['gameDuration'] = gameDuration
    match_data_for_excel['damage_pre_min'] = damage_pre_min
    match_data_for_excel['cs_pre_min'] = cs_pre_min
    match_data_for_excel['gold_pre_min'] = goldEarned_pre_min

    df = pandas.DataFrame(match_data_for_excel)

    path = 'excel files/' + summonerName[0] + '.xlsx'

    try:
        main_frame = pandas.read_excel(path)
        join_file = pandas.merge(df, main_frame, how='outer')
        join_file = join_file.drop_duplicates(subset='matchID', keep='first')
        join_file.to_excel(path, index=False)
        print(f'merged {summoner_name} data')
        return

    except Exception as e:
        df.to_excel(path, index=False)
        print(f"dumped {summoner_name}'s data")
        return


def get_player_stastus_and_to_excel(summoner_name):
    try:
        export_excel_file(summoner_name)
        get_data_by_position(summoner_name)
        return
    except Exception as e:
        print(e)
        return

def update_summoner_data():
    paths = get_all_summoners()
    print(paths)
    for path in paths:
        name = path.replace('excel files\\', '')
        name = name.replace('.xlsx', '')
        print(name)
        get_player_stastus_and_to_excel(name)
        time.sleep(120)