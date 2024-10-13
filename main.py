from required_types import PlayerId, HandId, Action, HandInfo
from view import ChopsticksTerminalView
from model import ChopsticksGameModel, Player, Hand, PlayerState
from enum import StrEnum
from typing import Sequence
import sys

class GameState(StrEnum):
    CONTINUE = 'Continue'
    OVER = 'Over'
    DRAW = 'Draw'

class ChopsticksGameController:
    def __init__(self, n: int, k: int, m: int, model: ChopsticksGameModel, view: ChopsticksTerminalView, starting_player: int):
        self._n = n
        self._k = k
        self._m = m
        self._model = model
        self._view = view
        self._round_number = 1
        self._curr_player = starting_player - 1
        self._players = []

    def start(self):
        model = self._model
        view = self._view

        self._players = model.initialize_players()
        
        while self.check_is_game_over() is GameState.CONTINUE:
            curr_player = self._find_curr_player()
            print(f"dkada {curr_player}")

            view.show_round_number(self._round_number)
            view.show_current_player(curr_player)
            player_hands = {player.player_id: player.hands for player in self._players}
            view.show_all_hands(player_hands, curr_player)
            action = view.ask_for_action()

            curr_player_hands: Sequence[HandInfo] = player_hands[curr_player]
            enemy_hands: Sequence[HandInfo] = []
            for id, hand in player_hands.items():
                if id is not curr_player:
                    enemy_hands.extend(hand)

            self._round_number += 1
            match action:
                case Action.TAP:
                    source, target = view.ask_for_tap_pair(list(curr_player_hands), list(enemy_hands))
                    model.perform_tap(source.fingers_up, source, target)
                    player_hands = {player.player_id: player.hands for player in self._players}

                case Action.SPLIT:
                    print('split')
            
            # update player state each time round ends
            for player in self._players:
                player.update_player_state()
        

        # game is over (WINNER detected)
        if self.check_is_game_over() is GameState.OVER:
            for player in self._players:
                if player.player_state is PlayerState.ACTIVE:
                    view.show_winner(player.player_id)
                    break

        #! NO CODE YET - game is over (DRAW)
            
        
    def _find_curr_player(self) -> PlayerId:
        while True:
            self._curr_player = (self._curr_player % self._n)
            
            if self._players[self._curr_player].player_state is PlayerState.ACTIVE:
                prev = self._curr_player
                self._curr_player += 1
                return self._players[prev].player_id

            self._curr_player += 1


                
            
        

    
    def check_is_game_over(self) -> GameState:
        count = 0
        for player in self._players:
            if player.player_state == PlayerState.ACTIVE:
                count += 1
        if count == 1:
            return GameState.OVER
        return GameState.CONTINUE



def main():
    args = sys.argv[1:]
    n, k, m = map(int, args)

    model = ChopsticksGameModel(n, k, m)
    view = ChopsticksTerminalView()
    controller = ChopsticksGameController(n, k, m, model, view, 1)
    controller.start()


     


if __name__ == "__main__":
    main()
