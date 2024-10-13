from required_types import PlayerId, HandId, HandInfo
from enum import StrEnum


class HandState(StrEnum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

class PlayerState(StrEnum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'


class Player:
    def __init__(self, player_id: int, total_hands: int, total_fingers: int, init_fingers: int):
        self._player_id = PlayerId(player_id)
        self._total_hands = total_hands
        self._total_fingers = total_fingers
        self.hands: list[Hand] = [] 
        self._init_finger_up = init_fingers 
        self._player_state = PlayerState.ACTIVE

    @property
    def player_id(self):
        return self._player_id

    @property
    def player_state(self):
        return self._player_state

    # @property
    # def hands(self):
    #     return self._hands

    #! only for debugging (remove it)
    def __repr__(self) -> str:
        print(f'{self._player_id}')
        for i in range(len(self.hands)):
            print(f'hand_id {self.hands[i].hand_id}: ({self.hands[i].fingers_up}/{self.hands[i].total_fingers})')
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
            self.hands.append(h)
    
    def update_player_state(self) -> None:
        for hand in self.hands:
            if hand.is_active():
                self._player_state = PlayerState.ACTIVE
                return
        self._player_state = PlayerState.INACTIVE


class Hand:
    def __init__(self, hand_id: HandId, player_id: PlayerId, fingers_up: int, total_fingers: int):
        self._hand_id = hand_id
        self._player_id = player_id
        self._fingers_up = fingers_up
        self._total_fingers = total_fingers

    #! only for debugging (remove it)
    def __repr__(self) -> str:
        print(f'Player {self._player_id} - Hand {self._hand_id}')
        print(f'hand_id {self.hand_id}: ({self.fingers_up}/{self.total_fingers})')
        return '' 

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
    
    # @property
    # def hand_state(self) -> HandState:
    #     return self._hand_state

    def is_active(self) -> bool:
        # if self._hand_state is HandState.ACTIVE:
        #     return True
        # return False
        if self._fingers_up < self._total_fingers and self._fingers_up != 0:
            return True
        return False

    def is_inactive(self) -> bool:
        # if self._hand_state is HandState.INACTIVE:
        #     return True
        # return False
        if self._fingers_up == self._total_fingers or self._fingers_up == 0:
            return True
        return False

    def to(self, fingers_up: int) -> HandInfo | None:
        if 0 <= fingers_up < self.total_fingers:
            return Hand(
                hand_id=self.hand_id,
                player_id=self.player_id,
                fingers_up=fingers_up,
                total_fingers=self.total_fingers,
            )
        return None

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
        self._players = []
        self._players_hands: dict[PlayerId, list[Hand]] = {}

    @property
    def players(self):
        return self._players

    @property
    def players_hands(self):
        return self._players_hands

    def initialize_players(self) -> None:
        players: list[Player] = []
        for _ in range(self._n):
            p = Player(self._player_id, self._k, self._m, 1)
            p.initialize_hands(self._hand_id)
            players.append(p)

            self._player_id += 1
            self._hand_id = 1
        self._players = players
        self.update_players_hands()
    
    def perform_tap(self, added_fingers: int, source: Hand, target: Hand) -> None:
        assert(source.is_active() and target.is_active())
        if source.is_active() and target.is_active():
            target.add_fingers(added_fingers)
        
    def perform_split(self, source: HandInfo, targets: list[HandInfo]):
        new_source = source.to(source.fingers_up)
        assert new_source is not None
        for player in self._players:
            if player.player_id == source.player_id:
                for i, hand in enumerate(player.hands):
                    if hand.hand_id == new_source.hand_id:
                        player.hands[i] = Hand(
                            hand_id=new_source.hand_id,
                            player_id=new_source.player_id,
                            fingers_up=new_source.fingers_up,
                            total_fingers=new_source.total_fingers
                        )

        for target in targets:
            new_target = target.to(target.fingers_up)
            assert(new_target is not None)
            for player in self._players:
                if player.player_id == new_target.player_id:
                    for i, hand in enumerate(player.hands):
                        if hand.hand_id == new_target.hand_id:
                            player.hands[i] = Hand(
                                hand_id=new_target.hand_id,
                                player_id=new_target.player_id,
                                fingers_up=new_target.fingers_up,
                                total_fingers=new_target.total_fingers
                            )

        self.update_players_hands()

    def update_players_hands(self):
        self._players_hands = {player.player_id: player.hands for player in self._players}