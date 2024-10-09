from required_types import Action
from view import ChopsticksTerminalView

'''
    N >= 2 players
    K >= 1 hands
    M >= 2 fingers each hand

    hand 
        - initially 1 finger up
        - inactive: all or no fingers up
        - active: otherwise

    player
        - inactive: all K hands are inactive

    game 
        - player 1 to N (round-robin)
        - skip inactive players


'''