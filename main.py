from required_types import PlayerId, Action, HandInfo
from view import ChopsticksTerminalView
from model import ChopsticksGameModel, Hand, PlayerState
from enum import StrEnum
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

    def start(self):
        model = self._model
        view = self._view

        model.initialize_players()
        
        while self._check_is_game_over(model) is GameState.CONTINUE:
            curr_player = self._find_curr_player(model)
            model.update_players_hands()

            view.show_round_number(self._round_number)
            view.show_current_player(curr_player)
            view.show_all_hands(model.players_hands, curr_player)
            action = view.ask_for_action()

            curr_player_hands: list[Hand] = model.players_hands[curr_player]
            active_enemy_hands = self._get_enemy_hands(model, curr_player)

            self._round_number += 1
            active_player_hands = [h for h in curr_player_hands if h.is_active()]
            match action:
                case Action.TAP:
                    source, target = view.ask_for_tap_pair(list(active_player_hands), list(active_enemy_hands))
                    model.perform_tap(source.fingers_up, source, target)
                    model.update_players_hands()

                case Action.SPLIT:
                    source = view.ask_for_split_source(list(active_player_hands))
                    target = self._get_split_targets(curr_player_hands, source)
                    if len(target) != 0:
                        info, infos = view.ask_for_split_assignments(source, target)
                        print(info)
                        [print(inf) for inf in infos]
                        model.perform_split(info, infos)
                    else:
                        view.show_split_no_targets()
            
            # update player state each time round ends
            for player in model.players:
                player.update_player_state()
        

        match self._check_is_game_over(model):
            # winner detected
            case GameState.OVER:
                for player in model.players:
                    if player.player_state is PlayerState.ACTIVE:
                        view.show_winner(player.player_id)
                        break
            #TODO: include code for draw
            case GameState.DRAW:
                view.show_draw()
            case _:
                pass

        
    def _find_curr_player(self, model: ChopsticksGameModel) -> PlayerId:
        '''Determine the current player of a round'''
        while True:
            self._curr_player = (self._curr_player % self._n)

            if model.players[self._curr_player].player_state is PlayerState.ACTIVE:
                prev = self._curr_player
                self._curr_player += 1
                return model.players[prev].player_id

            self._curr_player += 1

    
    def _check_is_game_over(self, model: ChopsticksGameModel) -> GameState:
        '''Check if there only one active player.
        If there is only one, they're the winner and game is over'''
        active_players = 0
        for player in model.players:
            if player.player_state == PlayerState.ACTIVE:
                active_players += 1
        if active_players == 1:
            return GameState.OVER
        return GameState.CONTINUE

    def _get_enemy_hands(self, model: ChopsticksGameModel, curr_player: PlayerId) -> list[Hand]:
        '''When a player taps, it gets all the hands of the enemy players'''
        enemy_hands: list[Hand] = []
        for id, hand in model.players_hands.items():
            if id is not curr_player:
                enemy_hands.extend([h for h in hand if h.is_active()])
        return enemy_hands

    def _get_split_targets(self, curr_player_hands: list[Hand], source: HandInfo) -> list[HandInfo]:
        '''Determines which of the players hand/s can be "splitted"'''
        target: list[HandInfo] = []
        for hand in curr_player_hands:
            if hand.hand_id != source.hand_id:
                if source.fingers_up == 1 and hand.total_fingers - hand.fingers_up == 1:
                    continue
                elif hand.total_fingers - hand.fingers_up > 1:
                    target.append(hand)
        
        return target




def main():
    args = sys.argv[1:]
    n, k, m = map(int, args)

    model = ChopsticksGameModel(n, k, m)
    view = ChopsticksTerminalView()
    controller = ChopsticksGameController(n, k, m, model, view, 1)
    controller.start()



if __name__ == "__main__":
    main()
