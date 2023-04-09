import os
import copy

from rumour_cards import GUESTS, WEAPONS, ROOMS, CARDS

def add_players():

    n = int(input("Number of players: "))

    players = []
    for p in range(n):
        players.append(input(f"Player {p + 1}: ")) # enter "Me" to add yourself
    
    return players

def add_hand(cards_per_hand):
    hand = []
    print("\nEnter cards in hand:")
    for c in range(cards_per_hand):
        while True:
            card = input(f"Card {c + 1}: ")
            if card in CARDS:
                hand.append(card)
                break
            else:
                print("Invalid card.")
                
    return hand

def display(table, combos):
    table = table.replace(-1, "-")

    #os.system("cls")
    print("\n")
    print(table)
    print()
    print(combos)
    print("\n")

def update_array(array, max_ones, max_zeros):
    array = array.to_numpy()
    if -1 in array:
        if (array == 1).sum() == max_ones:
            array = (array == 1).astype(int) # if max number of 1s in row -> mark remaining elements as 0
        elif (array == 0).sum() == max_zeros:
            array = (array != 0).astype(int) # if max number of 0s in row -> mark remaining element as 1
    return array

def update(table, combos, solution):

    cards_per_hand = (len(CARDS) - 3)//(len(table.columns) - 1)

    while True:

        start_table = table.copy()
        start_combos = combos.copy()

        for row in table.index:
            table.loc[row] = update_array(table.loc[row], 1, len(table.columns) - 1)

        for column in table.columns:
            if column == "Solution":
                break
            table[column] = update_array(table.loc[:, column], cards_per_hand, len(table.index) - cards_per_hand)

        table.iloc[:len(GUESTS), -1] = update_array(table.iloc[:len(GUESTS), -1], 1, len(GUESTS) - 1)
        table.iloc[len(GUESTS):-len(ROOMS), -1] = update_array(table.iloc[len(GUESTS):-len(ROOMS), -1], 1, len(WEAPONS) - 1)
        table.iloc[-len(ROOMS):, -1] = update_array(table.iloc[-len(ROOMS):, -1], 1, len(ROOMS) - 1)

        while True:
            new_combos = {}
            for player in combos:
                if player != "Me":
                    new_combos[player] = []

                for combo in combos[player]:
                    if len(combo) == 1:
                        table.loc[combo[0], player] = 1
                    else:
                        flag = 0
                        for card in combo:
                            if table.loc[card, player] == 1:
                                flag = 0
                                break
                            elif table.loc[card, player] == -1:
                                flag = 1

                        if flag == 1:
                            new_combos[player].append([])
                            for card in combo:
                                if table.loc[card, player] == -1:
                                    new_combos[player][-1].append(card)

            if new_combos == combos:
                combos = copy.deepcopy(new_combos)
                break
            else:
                combos = copy.deepcopy(new_combos)

        solution = []
        for card in CARDS:
            if table.loc[card, "Solution"] == 1:
                solution.append(card)

        if ((table.to_numpy() == start_table.to_numpy()).all()) & (combos == start_combos):
            break

    return table, combos, solution

def input_card(category_str, category_cards):
    while True:
        user_card = input(f"Input {category_str}: ")
        if user_card in category_cards:
            return user_card
        else:
            print("Invalid input.")

def player_turn(players, player_on_turn, table, combos):

    if player_on_turn == "Me":
        turn_str = "Your turn. Skip? (y/n) "
    else:
        turn_str = f"{player_on_turn}'s turn. Skip? (y/n) "
        
    while True:
        print()
        skip_turn = input(turn_str)
        if skip_turn == "y":
            return table, combos
        elif skip_turn == "n":
            break
        else:
            print("Invalid input.")        

    print()
    rumour_guest = input_card("guest", GUESTS)
    rumour_weapon = input_card("weapon", WEAPONS)
    rumour_room = input_card("room", ROOMS)
    rumour = [rumour_guest, rumour_weapon, rumour_room]
    print()
    #print(f"\nRumour: {rumour}")

    for i in range(players.index(player_on_turn) + 1, players.index(player_on_turn) + 1 + len(players)):
        asked_player = players[i % len(players)]

        if asked_player == "Me":
            show_card_str = "Did you show a card? (y/n) "
        else:
            show_card_str = f"Did {asked_player} show a card? (y/n) "

        while True:
            is_card_shown = input(show_card_str)
            if is_card_shown in ("y", "n"):
                break
            else:
                print("Invalid input.")

        if is_card_shown == "y":
            if asked_player != "Me":
                if player_on_turn == "Me":
                    shown_card = input("Which card was shown? ")
                    table.loc[shown_card, asked_player] = 1
                else:
                    combos[asked_player].append(rumour)
            break
        elif is_card_shown == "n":
            for card in rumour:
                table.loc[card, asked_player] = 0

    return table, combos
