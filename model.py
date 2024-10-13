from required_types import PlayerId, HandId, HandInfo
from view import ChopsticksTerminalView
from enum import StrEnum
from typing import Mapping
from pprint import pprint


class HandState(StrEnum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

class PlayerState(StrEnum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'


class Player:
    def __init__(self, player_id: int, total_hands: int, total_fingers: int):
        self._player_id = PlayerId(player_id)
        self._total_hands = total_hands
        self._total_fingers = total_fingers
        self._hands: list[Hand] = [] 
        self._init_finger_up = 1
        self._player_state = PlayerState.ACTIVE

    @property
    def player_id(self):
        return self._player_id

    @property
    def player_state(self):
        return self._player_state

    @property
    def hands(self):
        return self._hands

    #! only for debugging (remove it)
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
    
    # def check_state(self):
    #     for hand in self._hands:
    #         if hand._hand_state is HandState.ACTIVE:
    #             self._player_state = PlayerState.ACTIVE

    


    


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
    
    @property
    def hand_state(self) -> HandState:
        return self._hand_state

    def is_active(self) -> bool:
        if self._hand_state is HandState.ACTIVE:
            return True
        return False

    def is_inactive(self) -> bool:
        if self._hand_state is HandState.INACTIVE:
            return True
        return False

    def to(self, fingers_up: int) -> HandInfo | None:
        new_hand_info = self
        new_hand_info._fingers_up = fingers_up
        return new_hand_info
        """Return a copy of the `HandInfo` object with a new value for `fingers_up`.

        As `HandInfo` is expected to be immutable, this method can be used to
        "update" the `fingers_up` field of the existing `HandInfo` object by
        creating a _new_ object with its field values copied from the original
        except for `fingers_up` which is taken from the `fingers_up` parameter. 
        """
        ...


    def add_fingers(self, to_add: int) -> None:
        self._fingers_up = (self._fingers_up + to_add) % self._total_fingers
        if self._fingers_up == self._total_fingers or self._fingers_up == 0:
            self._hand_state = HandState.INACTIVE

    def set_fingers(self, to_change: int) -> None:
        self._fingers_up = to_change
        






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
            self._hand_id = 1
        return players
    
    def perform_tap(self, added_fingers: int, source: Hand, target: Hand) -> None:
        #! REMOVE HANDS IN VIEW KAPAG INACTIVE NA SIYA
        assert(source.hand_state is HandState.ACTIVE and target.hand_state is HandState.ACTIVE)
        if source.hand_state is HandState.ACTIVE and target.hand_state is HandState.ACTIVE:
            target.add_fingers(added_fingers)
        

    def perform_split(self, distributed_fingers: int, source: Hand, target: Hand):
        assert(source.hand_state is HandState.ACTIVE)
        
        # subtract G fingers from F (F - G)
        source.add_fingers(-distributed_fingers)

        # if inactive, set fingers up to G
        if target.hand_state is HandState.INACTIVE:
            target.set_fingers(distributed_fingers)
        # if active, simply add it but make sure na it won't get equal to or exceed
        else:
            #! CHANGE THIS
            if target.fingers_up + distributed_fingers >= self._m:
                raise Exception('split exceeded total fingers')
            target.add_fingers(distributed_fingers)
            
    