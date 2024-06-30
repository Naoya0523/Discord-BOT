import pandas as pd

def get_data_by_position(summoner_name, role):
    try:
        path = f"excel files/{summoner_name}/{role}_{summoner_name}.xlsx"
        role_data = pd.read_excel(path)
    except Exception as e:
        print(e)
        print("check summoner name and role")
        return

    return role_data


def average(data, value):
    return (data[value].sum())/len(data[value])


def win_rate(data):
    count = 0
    for win in data['win']:
        if win :
            count += 1
        else:
            pass
    return count/len(data['win'])


def get_MMR_TOP(summoner_name):
    data = get_data_by_position(summoner_name, 'TOP')

    if len(data) <= 3:
        return 0

    kda = average(data, 'KDA') * 2
    visionScore = average(data, 'visionScore') * 1
    damge = average(data, 'damage_pre_min') * 0.01
    damage_turrets = average(data, 'damageDealtToTurrets') * 0.007
    killInovementRate = average(data, 'killInovementRate') * 50

    MMR = kda  + visionScore + damge + damage_turrets + killInovementRate
    return MMR


def get_MMR_JUNGLE(summoner_name):
    data = get_data_by_position(summoner_name, 'JUNGLE')

    if len(data) <= 3:
        return 0

    kda = average(data, 'KDA') * 2
    visionScore = average(data, 'visionScore') * 1.5
    damage = average(data, 'damage_pre_min') * 0.01
    damage_turrets = average(data, 'damageDealtToTurrets') * 0.005
    killInovementRate = average(data, 'killInovementRate') * 60

    MMR = kda + visionScore + damage + damage_turrets + killInovementRate
    return MMR


def get_MMR_MIDDLE(summoner_name):
    data = get_data_by_position(summoner_name, 'MIDDLE')

    if len(data) <= 3:
        return 0

    kda = average(data, 'KDA') * 2
    visionScore = average(data, 'visionScore') * 1
    damage = average(data, 'damage_pre_min') * 0.01
    damage_turrets = average(data, 'damageDealtToTurrets') * 0.005
    killInovementRate = average(data, 'killInovementRate') * 60

    MMR = kda + visionScore + damage + damage_turrets + killInovementRate
    return MMR


def get_MMR_BOTTOM(summoner_name):
    data = get_data_by_position(summoner_name, 'BOTTOM')

    if len(data) <= 3:
        return 0

    kda = average(data, 'KDA') * 2
    damage = average(data, 'damage_pre_min') * 0.02
    visionScore = average(data, 'visionScore') * 1
    damage_turrets = average(data, 'damageDealtToTurrets') * 0.006
    killInovementRate = average(data, 'killInovementRate') * 60

    MMR = kda + damage + visionScore + damage_turrets + killInovementRate
    return MMR


def get_MMR_UTILITY(summoner_name):
    data = get_data_by_position(summoner_name, 'UTILITY')

    if len(data) <= 3:
        return 0

    kda = average(data, 'KDA') * 2
    visionScore = average(data, 'visionScore') * 1.5
    damage = average(data, 'damage_pre_min') * 0.005
    damage_turrets = average(data, 'damageDealtToTurrets') * 0.005
    killInovementRate = average(data, 'killInovementRate') * 60

    MMR = kda + visionScore + damage + damage_turrets + killInovementRate
    return MMR


def get_MMR(summoner_name):
    TOP = get_MMR_TOP(summoner_name)
    JG = get_MMR_JUNGLE(summoner_name)
    MID = get_MMR_MIDDLE(summoner_name)
    ADC = get_MMR_BOTTOM(summoner_name)
    SUP = get_MMR_UTILITY(summoner_name)

    print(f'summonerName,  top,   jg,   mid,   adc,   sup')
    print(f'{summoner_name}, {round(TOP, 2)}, {round(JG, 2)}, {round(MID, 2)}, {round(ADC, 2)}, {round(SUP, 2)}')

    return {'top':TOP, 'jg':JG, 'mid':MID, 'adc':ADC, 'sup':SUP}
