from required_types import PlayerId, HandId, Action, HandInfo
from view import ChopsticksTerminalView
from enum import StrEnum
from pprint import pprint


class HandState(StrEnum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'


class Player:
    def __init__(self, player_id: int, total_hands: int, total_fingers: int):
        self._player_id = PlayerId(player_id)
        self._total_hands = total_hands
        self._total_fingers = total_fingers
        self._hands: list[Hand] = []
        self._init_finger_up = 1

    def __repr__(self) -> str:
        print(f'{self._player_id}')
        for i in range(len(self._hands)):
            print(f'hand_id {self._hands[i].hand_id}: ({self._hands[i].fingers_up}/{self._hands[i].total_fingers})')
        return '' 


    def initialize_hands(self, hand_id: int) -> None:
        for _ in range(self._total_hands):
            h = Hand(
                HandId(hand_id),
                self._player_id, 
                self._init_finger_up, 
                self._total_fingers
            )
            hand_id += 1
            self._hands.append(h)
    


class Hand:
    def __init__(self, hand_id: HandId, player_id: PlayerId, fingers_up: int, total_fingers: int):
        self._hand_id = hand_id
        self._player_id = player_id
        self._fingers_up = fingers_up
        self._total_fingers = total_fingers
        self._hand_state = HandState.ACTIVE

    @property
    def hand_id(self) -> HandId:
        return self._hand_id

    @property
    def player_id(self) -> PlayerId:
        return self._player_id

    @property
    def fingers_up(self) -> int:
        return self._fingers_up

    @property
    def total_fingers(self) -> int:
        return self._total_fingers

    def is_active(self) -> bool:
        if self._hand_state is HandState.ACTIVE:
            return True
        return False

    def is_inactive(self) -> bool:
        if self._hand_state is HandState.INACTIVE:
            return True
        return False

    def to(self, fingers_up: int) -> HandInfo | None:
        """Return a copy of the `HandInfo` object with a new value for `fingers_up`.

        As `HandInfo` is expected to be immutable, this method can be used to
        "update" the `fingers_up` field of the existing `HandInfo` object by
        creating a _new_ object with its field values copied from the original
        except for `fingers_up` which is taken from the `fingers_up` parameter. 
        """
        ...




class ChopsticksGameModel:
    def __init__(self, n: int, k: int, m: int):
        self._n = n
        self._k = k
        self._m = m
        self._player_id = 1
        self._hand_id = 1

    def initialize_players(self) -> list[Player]:
        players: list[Player] = []
        for _ in range(self._n):
            p = Player(self._player_id, self._k, self._m)
            p.initialize_hands(self._hand_id)
            players.append(p)

            self._player_id += 1
            self._hand_id += self._k 
            print(p)
        return players
    
            
        


    