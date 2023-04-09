import os
import pandas as pd

from rumour_cards import CARDS
from funcs import *

if __name__ == "__main__":

    os.system("cls")

    players = add_players()
    cards_per_hand = (len(CARDS) - 3)//(len(players))
    hand = add_hand(cards_per_hand)

    rows = CARDS
    columns = players + ["Solution"]
    table = pd.DataFrame(([[-1 for c in range(len(columns))] for r in range(len(rows))]), rows, columns)
    
    for card in hand:
        table.loc[card, "Me"] = 1 # set cards in hand to 1 in table

    combos = {}
    for player in players:
        if player != "Me":
            combos[player] = []

    solution = []

    table, combos, solution = update(table, combos, solution)

    display(table, combos)

    is_solved = False
    while is_solved == False: # main loop
        for player_on_turn in players: # player turn

            table, combos = player_turn(players, player_on_turn, table, combos)

            table, combos, solution = update(table, combos, solution)
            
            display(table, combos)

            if len(solution) == 3:
                is_solved = True
                
    print()
    print("\n==================================================")
    print(f"SOLUTION FOUND: {solution}")
    print("==================================================")
    print()
