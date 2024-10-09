from required_types import PlayerId, HandId, Action, HandInfo
from view import ChopsticksTerminalView
from model import ChopsticksGameModel
import sys

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
