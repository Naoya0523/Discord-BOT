
import random
import copy

def randomize_numbers():
    numbers = [0,1,2,3,4]
    random.shuffle(numbers)
    return numbers

def randomize_order(lst):
    shuffle_lst = []
    random_flag = random.shuffle([True, False])

    if random_flag:
        shuffle_lst.append(lst[1])
        shuffle_lst.append(lst[0])
        return shuffle_lst
    else:
        return lst

def normalize_lv(lv):
    if 0 <= lv <= 30:
        return 0
    elif 30 < lv <= 60:
        return 1
    else:
        return 2

def get_elements(input_line):
    try:
        input_list = input_line.split(',')

        name = input_list[0]
        lv = int(input_list[1])
        roll = input_list[2:]

        lv = normalize_lv(lv)

        return name, lv, roll

    except Exception as e:
        print(e)
        return False

def make_muchup(str_roll, input_members):
    ROLL = []
    members = copy.deepcopy(input_members)

    for player in members:
        if str_roll not in player[2]:
            continue

        if player[2][0] == str_roll:
            ROLL.append(player)
            members.remove(player)
            break

    #second player
    for player in members:
        if str_roll not in player[2]:
            continue
        else:
            if len(ROLL) == 1:
                if abs(ROLL[0][0] - player[0]) != 2:
                    ROLL.append(player)
                    members.remove(player)
                    break
            else:
                break

    #fill
    if len(ROLL) != 2:
        for player in members:
            if "fill" not in player[2]:
                continue
            else:
                ROLL.append(player)
                members.remove(player)
                if len(ROLL) != 2:
                    continue
                else:
                    break

    return ROLL, members


def get_team_members(member):
    members = sorted(member)

    TOP, members = make_muchup("top", members)
    print(TOP)
    JG, members = make_muchup("jg", members)
    print(JG)
    MID, members = make_muchup("mid", members)
    print(MID)
    ADC, members = make_muchup("adc", members)
    print(ADC)
    SUP, members = make_muchup("sup", members)
    print(SUP)

    return TOP, JG, MID, ADC, SUP

members = [[0, 'naoya', ['top', 'mid','sup']], [1, 'asdd', ['jg', 'sup','adc']], [0, 'errsa', ['top', 'mid','sup']], [1, 'sdafa', ['jg', 'adc','mid']], [2, 'sdffg', ['fill']],
           [1, 'asdfssa', ['mid', 'adc', 'sup']], [1, 'dsfffaas', ['sup', 'jg', 'adc']], [2, 'adff', ['fill']], [2, 'sdasdf', ['fill']], [2, 'poid', ['fill']]]
members2 = [[0, 'naoya', ['top', 'mid']], [1, 'nfkjg', ['jg', 'sup', 'adc']], [0, 'hufwdwj', ['top', 'mid', 'sup']], [2, 'nfufddw', ['fill']], [1, 'fddwda', ['jg', 'adc', 'mid']],
            [1, 'gyubb', ['mid', 'adc', 'sup']], [1, 'asdfffds', ['sup', 'jg', 'adc']], [2, 'fafdwun', ['fill']], [2, 'asdfa', ['fill']], [2, 'fafsf', ['fill']]]
def check_member(TOP, jg, mid, adc, sup):
    roll_list = [TOP, jg, mid, adc, sup]

    for roll in roll_list:
        if len(roll) != 2:
            return False

    return True

def get_best_team(input_members):
    candidates = []
    member = copy.deepcopy(input_members)

    for _ in range(500):
        order = randomize_numbers()
        #print(order)
        members = sorted(member)

        for num in order:
            if int(num) == 0:
                TOP, members = make_muchup("top",members)
            elif int(num) == 1:
                JG, members = make_muchup("jg",members)
            elif int(num) == 2:
                MID, members = make_muchup("mid", members)
            elif int(num) == 3:
                ADC, members = make_muchup("adc", members)
            else:
                SUP, members = make_muchup("sup", members)

        if check_member(TOP, JG, MID, ADC, SUP):
            candidates.append([TOP, JG, MID, ADC, SUP])
        else:
            pass
    return candidates

'''
teams = get_best_team(members)
for team in teams:
    print(team)
    for player in team:
        print(len(player))
'''

def select_team(members):
    teams = copy.deepcopy(get_best_team(members))
    select_teams = []

    for team in teams:
        diff_count = 0
        remove_flag = False
        for position in team:
            print(position)
            if abs(position[0][0] - position[1][0]) == 1:
                diff_count += 1
            elif abs(position[0][0] - position[1][0]) == 2:
                diff_count += 2

        if diff_count > 4:
            remove_flag = True

        if remove_flag:
            pass
        else:
            select_teams.append(team)
        print('---------------------')

    select_teams2 = []
    for team in select_teams:
        team2 = []
        for position in team:
            position2 = randomize_order(position)
            team2.append(position2)
        select_teams2.append(team2)

    '''
    for team in select_teams2:
        team_0_cost = 0
        team_1_cost = 0
        for position in team:
            team_0_cost += position[0][0]
            team_1_cost += position[1][0]
        if abs(team_1_cost - team_0_cost) >= 2:
            select_teams2.remove(team)
    '''
    return select_teams2

def get_proposed_team(members):
    match_members = select_team(members)
    match_members_name = []

    for match_member in match_members:
        team_1 = []
        team_2 = []
        for member in match_member:
            player1 = member[0][1]
            player2 = member[1][1]

            team_1.append(player1)
            team_2.append(player2)
        match_members_name.append([team_1,  team_2])

    return match_members_name[:3]

match_members = get_proposed_team(members2)
print(match_members)