import random


war_cnt = 0
i = 0
multi_war = 0
max_war = 0
wars = []


def create_cards():
    """
    Creates a deck of 52 cards and shuffles them.
    :returns: list of shuffled cards
    """

    cards = list(range(2, 15)) * 4
    random.shuffle(cards)
    return cards


def pass_out(player_names):
    """
    Passes out cards to three players
    Returns a dictionary of players' cards
    """
    all_player_cards = {player: [] for player in player_names}
    cards_mod = 52 % len(player_names)
    cards = create_cards()[: 52 - cards_mod]  # removes last card from play
    while cards:
        for player in player_names:
            all_player_cards[player].append(cards.pop())
    return all_player_cards


def card_pop(player_cards):
    if len(player_cards) > 0:
        card = player_cards.pop()
        return card
    else:
        return 0


def compare(all_player_cards, player_names):
    """
    Takes in 3 lists of player cards.
    Pops the first value and compares.
    Returns the 3 popped values and the max value of the 3 cards.
    """
    compare_list = [card_pop(all_player_cards[i]) for i in player_names]
    highest_card = max(compare_list)
    return compare_list, highest_card


def clean_list(compare_list):
    return [i for i in compare_list if i > 1]


def no_ties(compare_list, highest_card, player_names, accumulated_cards=[]):
    """
    How to distribute the winner of the round's cards if there are no ties.
    """
    total_cards = compare_list + accumulated_cards
    winner = player_names[compare_list.index(highest_card)]
    clean_cards = clean_list(total_cards)
    all_players_cards[winner].extend(clean_cards)


def war(compare_list, highest_card, player_names, prev_war_cards=[]):
    """
    The players who are at war should accumulate 3 cards each.
    Then compare the 4th card to see who wins all accumulated cards
    and the compared 4th cards.
    e.g. P1 vs P2
    P1 [3, 6, 7], 10
    P2 [4, 9, 14] 12
    P2 would win all of P1's cards and take back P2's accumulated cards
    and the war comparison cards
    P2's list would be extended by [3,6,7,10] + [4,9,14,12]
    """
    accumulated_cards = []
    new_compare_list = []
    for idx, val in enumerate(compare_list):
        player_pos = player_names[idx]
        if val != highest_card:
            accumulated_cards.extend([0, 0, 0])
            new_compare_list.append(0)
        else:
            for _ in range(3):
                accumulated_cards.append(card_pop(all_players_cards[player_pos]))
            new_compare_list.append(card_pop(all_players_cards[player_pos]))
    total_cards = prev_war_cards + compare_list + accumulated_cards
    new_highest_card = max(new_compare_list)
    distribute_winner(new_compare_list, new_highest_card, player_names, total_cards)


def distribute_winner(compare_list, highest_card, player_names, accumulated_cards=[]):
    global max_war
    if compare_list.count(highest_card) > 1:
        global war_cnt
        war_cnt += 1
        if accumulated_cards:
            global multi_war
            multi_war += 1
        # global max_war
        max_war += 1
        war(compare_list, highest_card, player_names, accumulated_cards)
    else:
        global wars
        # global max_war
        wars.append(max_war)
        no_ties(compare_list, highest_card, player_names, accumulated_cards)
        max_war = 0


num_players = 0
while (2 > num_players) or (num_players > 52):
    player_input = input("How many players? (Input between 2 and 52 inclusive) ")
    try:
        num_players = int(player_input)
    except ValueError:
        print("Please input a valid number between 2 and 52 inclusive.")
        num_players = 0

player_names = []
for i in range(num_players):
    name = None
    while not name:
        name = input(f"What is the name of player {i+1}? ")
    player_names.append(name)

all_players_cards = pass_out(player_names)
all_players_triggers = {player: True for player in player_names}
rankings = []

while True:
    compare_list, highest_card = compare(all_players_cards, player_names)
    distribute_winner(compare_list, highest_card, player_names)
    i += 1
    max_card_len = 52 - (52 % len(player_names))
    value_lens = [len(value) for value in all_players_cards.values()]
    for key, value in all_players_cards.items():
        if (len(value) == 0) and all_players_triggers[key]:
            print(f"\n{key} was knocked out on round {i}!")
            rankings.append(key)
            all_players_triggers[key] = False
    if max_card_len in value_lens:
        break
for key, value in all_players_cards.items():
    if len(value) == (52 - (52 % len(player_names))):
        print("")
        print("=====================================")
        print(f"The winner is {key}!")
        print("=====================================")
        print("")

print("The losers:")
for idx, val in enumerate(reversed(rankings)):
    print(f"Rank {idx+2}: {val}")

print("")
print(f"The game took {i} turns to finish.")
print(f"There were {war_cnt} wars.")
print(f"There were {multi_war} multi-wars.")
print(f"The longest war lasted {max(wars)} rounds.")
