
from custom2 import get_ramdom_team
from average_score import get_MMR

def extract_unique_lists(lists):
    seen = set()
    result = []

    for sublist in lists:
        first_value = sublist[0]
        if first_value not in seen:
            result.append(sublist)
            seen.add(first_value)

    return result


def get_player_stats(player_info):
    player_info = player_info.split(",")

    player_name = player_info[0]
    position = player_info[1:]

    return player_name, position

def get_role_score(str_role, roles, priority_MMR):
    if priority_MMR:
        role_score = 0
        role_bias = 0
    else:
        role_score = 800
        role_bias = 250

    for role in roles:
        if role == str_role:
            return role_score
        elif role == 'fill':
            return role_score
        else:
            role_score -= role_bias

    return 0

def get_score_by_position(str_role, players, priority_MMR):
    score = 0
    if priority_MMR:
        MMR_bias = 20
    else:
        MMR_bias = 2

    P1 = players[0]
    P2 = players[1]

    P1_role, p2_role = P1['position'], P2['position']
    P1_MMR, P2_MMR = P1['MMR'], P2['MMR']

    P1_role_score = get_role_score(str_role, P1_role, priority_MMR)
    p2_role_score = get_role_score(str_role, p2_role, priority_MMR)
    score += (P1_role_score + p2_role_score)

    if (P1_MMR[str_role] == 0) or (P2_MMR[str_role] == 0):
        return -500

    MMR_diff = abs(P1_MMR[str_role] - P2_MMR[str_role])
    score -= (MMR_diff * MMR_bias)

    return score

def get_score_and_matchup(members, priority_MMR):
    positions = ['top', 'jg', 'mid', 'adc', 'sup']
    match_up = get_ramdom_team(members)
    global_score = 0

    for idx in range(len(match_up)):
        score = get_score_by_position(positions[idx], match_up[idx], priority_MMR)
        global_score += score

    team1_mmr, team2_mmr = 0, 0
    idx = 0

    for position in match_up:
        player1_mmr = position[0]['MMR'][positions[idx]]
        team1_mmr += player1_mmr

        player2_mmr = position[1]['MMR'][positions[idx]]
        team2_mmr += player2_mmr
        idx += 1
    diff = abs(team1_mmr - team2_mmr)
    global_score -= diff

    return global_score, match_up

def get_best_matchup(members):

    roles = ['top', 'jg', 'mid', 'adc', 'sup']
    best_matchup = []
    for _ in range(500000):
        score, matchup = get_score_and_matchup(members, priority_MMR=False)
        if score >= 7000:
            matchup.insert(0, score)
            best_matchup.append(matchup)
    best_matchup = sorted(best_matchup, key=lambda x: x[0], reverse=True)
    best_matchup = extract_unique_lists(best_matchup)[:2]

    best_matchup2 = []
    for _ in range(500000):
        score, matchup = get_score_and_matchup(members, priority_MMR=True)
        if score >= -1000:
            matchup.insert(0, score)
            best_matchup2.append(matchup)
    best_matchup2 = sorted(best_matchup2, key=lambda x: x[0], reverse=True)
    best_matchup2 = extract_unique_lists(best_matchup2)[:2]

    best_matchup.append(best_matchup2[0])
    best_matchup.append(best_matchup2[1])

    proposed_team = []
    num = 1
    for team in best_matchup:
        team1_mmr = 0
        team2_mmr = 0
        diff = []
        team_score = int(team[0])
        team.remove(team[0])
        idx = 0
        line = f'候補{num} スコア：{team_score}\nlane : TEAM1, TEAM2, MMR DIFF\n'
        for position in team:
            player1 = position[0]['name']
            player1_mmr = position[0]['MMR'][roles[idx]]
            team1_mmr += player1_mmr

            player2 = position[1]['name']
            player2_mmr = position[1]['MMR'][roles[idx]]
            team2_mmr += player2_mmr

            mmr_diff = int(abs(player1_mmr - player2_mmr))
            diff.append(mmr_diff)
            line += (str(roles[idx]) + " : " + str(player1) + ", " + str(player2) + ", " + str(mmr_diff) + "\n")
            idx += 1

        line += f'MMR : {int(team1_mmr)}, {int(team2_mmr)}, {int(abs(team1_mmr - team2_mmr))}\n'
        if max(diff) > 20:
            line += 'MMRの差が大きいレーンがあります。\n'

        proposed_team.append(line)
        num += 1

    return proposed_team

member = [{'name':'nintendonaoya', 'position':['top','fill'], 'MMR':get_MMR('nintendonaoya')},
          {'name':'mushiba648', 'position':['sup', 'top', 'mid'], 'MMR':get_MMR('mushiba648')},
          {'name':'awirge', 'position':['sup', 'jg'], 'MMR':get_MMR('awirge')},
          {'name':'azukibar81968', 'position':['mid', 'jg', 'top'], 'MMR':get_MMR('azukibar81968')},
          {'name':'camoncy', 'position':['jg', 'mid', 'adc'],'MMR':get_MMR('camoncy')},
          {'name':'clipclop', 'position':['fill'], 'MMR':get_MMR('clipclop')},
          {'name':'implatton', 'position':['mid', 'adc', 'sup'], 'MMR':get_MMR('implatton')},
          {'name':'はなみず87', 'position':['adc', 'top'], 'MMR':get_MMR('はなみず87')},
          {'name':'lettuce222', 'position':['mid', 'adc'], 'MMR':get_MMR('lettuce222')},
          {'name':'kaiso1225', 'position':['top', 'sup', 'mid'], 'MMR':get_MMR('kaiso1225')},
          ]

matchup = get_best_matchup(member)
for match in matchup:
    print(match)