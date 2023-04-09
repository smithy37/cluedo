# Cluedo Solver
## Overview
This python program solves a game of cluedo. It is designed to be used in-game by a single player. The user inputs in-game actions and the program prints information to the user, including a table which summarises the up-to-date deductions, and combinations of potential cards held by other players.
### Table
Table symbols can be interpreted as follows:
- 0 : This player does not hold this card.
- 1 : This player does hold this card.
- \- : It is not known whether this player holds this card.
### Combinations
Combinations of cards are stored and tracked between turns. To demonstrate the value of this feature, consider a game involving the user (player A) and two other players (B and C). If B starts the rumour (WHITE, PISTOL, KITCHEN), and C shows a card to B, but not to A, then A can deduce that C holds at least one card in the rumour. If, later on in the game, it is deduced that B cannot possibly hold WHITE or PISTOL, then from the stored combination, it can be deduced that B must hold KITCHEN.
## Using the Program
### 1. Add Players
Enter the number of players, and then players' names in order of play. The user MUST enter their own name as <Me>.
### 2. Add Cards In Hand
Add cards that have been dealt to the user. Use lowercase and spaces between words e.g. <dining room>. The initial table will be printed to the user.
### 3. Main Game Loop
On each player's turn, specify whether the turn is skipped or not. If the turn is not skipped, enter the rumour and then the responses of other players. After every turn, the table and stored combinations are updated and printed to the user.
### 4. Solution
Once all 3 cards in the solution have been deduced, they are printed to the user and the program ends.
