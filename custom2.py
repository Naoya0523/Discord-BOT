import random

def get_ramdom_team(members):
    if len(members) != 10:
        return False

    order = [0,1,2,3,4,5,6,7,8,9]
    random_order = random.sample(order, len(order))
    match_up = [
                ["top1", "top2"], #TOP
                ["JG1", "JG2"],   #JG
                ["MID1", "MID2"], #MID
                ["ADC1", "ADC2"], #ADC
                ["SUP1", "SUP2"]  #SUP
                                ]

    position, player_idx = 0, 0
    for index in random_order:
        match_up[position][player_idx] = members[index]
        player_idx += 1
        if player_idx == 2:
            position += 1
            player_idx = 0

    return match_up

def check_position(str_roll, players):
    score = 0
    player1 = players[0]
    player2 = players[1]

    p1_lv, p2_lv = player1[0], player2[0]
    p1_roll, p2_roll = player1[2], player2[2]

    level_diff = abs(p1_lv - p2_lv)
    if level_diff == 0:
        score += 5
    elif level_diff == 1:
        score += 2
    else:
        score += 0

    if str_roll in p1_roll:
        if str_roll == p1_roll[0]:
            score += 5
        else:
            score += 2
    elif p1_roll == "fill":
        score += 3
    else:
        score += 0

    if str_roll in p2_roll:
        if str_roll == p2_roll[0]:
            score += 5
        else:
            score += 2
    elif p2_roll == "fill":
        score += 3
    else:
        score += 0

    return score

def get_score_and_matchup(members):
    position = ["top", "jg", "mid", "sup", "adc"]
    match_up = get_ramdom_team(members)
    global_score = 0

    for idx in range(len(match_up)):
        score = check_position(position[idx], match_up[idx])
        global_score += score

    return global_score, match_up

def get_best_members(members):
    best_members = []
    roll_list = ['TOP','JG', 'MID', 'ADC', 'SUP']
    for _ in range(300000):
        score, match_up = get_score_and_matchup(members)
        if score >= 40:
            match_up.insert(0, score)
            best_members.append(match_up)
    best_members.sort(reverse=True)

    proposed_team = []
    propose_num = 1
    for team in best_members[:3]:
        team.remove(team[0])
        idx = 0
        line = f"候補{propose_num}\nLANE : TEAM1, TEAM2\n"
        for positions in team:
            player_1 = positions[0][1]
            player_2 = positions[1][1]
            line += (str(roll_list[idx]) + " : " + str(player_1) + ", " + str(player_2) + "\n")
            idx += 1
        proposed_team.append(line)
        propose_num += 1

    return proposed_team