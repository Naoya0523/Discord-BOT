import pandas as pd
import os

def get_data_by_position(summoner_name):
    final_path = 'excel files/' + summoner_name
    os.makedirs(final_path, exist_ok=True)

    path = 'excel files/' + summoner_name + '.xlsx'
    player_data = pd.read_excel(path)

    top, jg, mid, adc, sup = 'TOP', "JUNGLE", 'MIDDLE', 'BOTTOM', 'UTILITY'
    roles = [top, jg, mid, adc, sup]

    for role in roles:
        position_data = player_data[player_data.iloc[:, 6].str.contains(role) & (player_data.iloc[:, 4] == False)]
        position_data.to_excel(f'{final_path}/{role}_{summoner_name}.xlsx', index=False)

    print(f"dumped data for each {summoner_name} position")

def get_all_data_by_positions():
    path = 'excel files/all datas/all_data.xlsx'
    roles = ['BOTTOM', 'JUNGLE', 'MIDDLE', 'TOP', 'UTILITY']

    all_data = pd.read_excel(path)
    for role in roles:
        data_by_position = all_data[all_data.iloc[:, 6].str.contains(role) & (all_data.iloc[:, 4] == False)]
        data_by_position.to_excel(f'excel files/all datas/{role}_data.xlsx', index=False)

