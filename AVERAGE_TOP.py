import os
import glob
import pandas as pd
import numpy as np

def get_all_summoners():
    path = 'excel files/'
    summoner_excel = os.path.join(path, '*.xlsx')
    summoner_excel_files = glob.glob(summoner_excel)
    summoner_names = []
    for path in summoner_excel_files:
        name = path.replace('excel files\\', '')
        name = name.replace('.xlsx', '')
        summoner_names.append(name)

    return summoner_names

def average(list:list) -> float:
    if len(list) <= 0:
        return 0.0
    else:
        return sum(list)/len(list)

def dump_top_datas():
    summoner_names = get_all_summoners()
    all_data = [[0,0,0] for _ in range(len(summoner_names))]
    #print(all_data)
    idx = 0
    for summoner in summoner_names:
        path = f'excel files/{summoner}/TOP_{summoner}.xlsx'
        top_data = pd.read_excel(path)

        damage_pre_min = top_data['damage_pre_min']
        gold_pre_min = top_data['gold_pre_min']
        average_kda = top_data['KDA']
        average_damgage = average(damage_pre_min)
        average_gold = average(gold_pre_min)
        average_kda = average(average_kda)

        all_data[idx][0] = average_damgage
        all_data[idx][1] = average_gold
        all_data[idx][2] = average_kda
        idx += 1

    all_data = np.array(all_data)
    return all_data

data = dump_top_datas()
from clustering import kmeans
kmeans(3, data)