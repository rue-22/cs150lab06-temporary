from required_types import PlayerId, HandId, Action, HandInfo
from view import ChopsticksTerminalView
from model import ChopsticksGameModel, Hand, PlayerState
import sys
from collections.abc import Sequence

class ChopsticksGameController:
    def __init__(self, n: int, k: int, m: int, model: ChopsticksGameModel, view: ChopsticksTerminalView):
        self._n = n
        self._k = k
        self._m = m
        self._model = model
        self._view = view

    def start(self):
        model = self._model
        view = self._view

        playerslist = model.initialize_players()
        round = 1
        indexlist = [i for i in range(len(playerslist))]
        nextindex = indexlist[0]
        current : PlayerId = playerslist[nextindex].player_id
        playerandhand : dict[PlayerId, list[Hand]] = {}

        for player in playerslist:
            currid = player.player_id
            playerandhand[currid] = player.hands
        
        while True:
            current = playerslist[nextindex].player_id
            view.clear_screen()
            print(playerslist[nextindex].player_id, playerslist[nextindex].check_state())
            view.show_round_number(round)
            view.show_all_hands(playerandhand, current)

            action = view.ask_for_action()

            match action:
                case Action.TAP:
                    for currplayer in playerslist:
                        if currplayer.player_id == current:
                            sourceplayer = currplayer
                    sources = sourceplayer.hands
                    otherhands = []
                    for otherplayer in playerslist:
                        if otherplayer.player_id != current:
                            for hand in otherplayer.hands:
                                otherhands.append(hand)
                    targets = otherhands
                    source, target = view.ask_for_tap_pair(sources, targets)
                    model.perform_tap(source.fingers_up, source, target)
                case Action.SPLIT:
                    for currplayer in playerslist:
                        if currplayer.player_id == current:
                            sourceplayer = currplayer
                    sources = sourceplayer.hands
                    if sources:
                        source = view.ask_for_split_source(sources)
                        targethands = []
                        for hand in sources:
                            if hand.hand_id != source.hand_id:
                                targethands.append(hand)
                        targets = targethands
                        new_source, new_targets = view.ask_for_split_assignments(source, targets)
            
            
            
            round+=1
            
            nextindex = nextindex + 1 if nextindex + 1 in indexlist else indexlist[0]
            if playerslist[nextindex].check_state() == PlayerState.INACTIVE:
                nextindex += 1
            
            if round == 10:
                break


        print('here at start')



def main():
    args = sys.argv[1:]
    n, k, m = map(int, args)

    model = ChopsticksGameModel(n, k, m)
    view = ChopsticksTerminalView()
    controller = ChopsticksGameController(n, k, m, model, view)
    controller.start()


     


if __name__ == "__main__":
    main()

