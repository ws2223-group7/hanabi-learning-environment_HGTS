# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, too-many-arguments, line-too-long, broad-exception-raised, too-many-instance-attributes

import sys
import os
from typing import Optional

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment.pyhanabi import HanabiCard, HanabiMove, HanabiMoveType, HanabiState
from hanabi_learning_environment import rl_env

class RewardShape:
    '''reward shape'''
    def __init__(self) -> None:
        self.lost_one_life_token: bool = False
        self.lost_all_life_tokens: bool = False
        self.successfully_played_a_card: bool = False

        self.discard: bool = False
        self.discard_playable: Optional[bool] = None
        self.discard_useless: Optional[bool] = None
        self.discard_unique: Optional[bool] = None

        self.play: bool = False
        self.hint: bool = False

    def get_observation_by_state(self, hanabi_state: HanabiState):
        """get observation by state"""
        return hanabi_state.observation(hanabi_state.cur_player())

    def get_card(self, next_move: HanabiMove, hanabi_state: HanabiState) -> HanabiCard:
        """get card knowledge on discarding"""
        my_dict = next_move.to_dict()
        card_index = int(my_dict["card_index"])
        card:HanabiCard = hanabi_state.player_hands()[hanabi_state.cur_player()][card_index]
        return card

    def is_discard_playable(self, next_move: HanabiMove, hanabi_state: HanabiState) -> bool:
        """execute discard playable"""
        observation = self.get_observation_by_state(hanabi_state)
        card = self.get_card(next_move, hanabi_state)
        return bool(observation.card_playable_on_fireworks(card.color(), card.rank()))

    def is_discard_useless(self, next_move: HanabiMove, hanabi_state: HanabiState) -> bool:
        """is discard useless"""
        observation = self.get_observation_by_state(hanabi_state)
        card = self.get_card(next_move, hanabi_state)
        firework = int(observation.fireworks()[card.color()])
        rank = card.one_plus_rank()
        if rank is None:
            raise Exception("rank must have a value")

        return firework >= rank

    def is_discard_unique(self, next_move: HanabiMove, hanabi_state: HanabiState) -> bool:
        """is discard unique"""
        card = self.get_card(next_move, hanabi_state)
        rank = card.one_plus_rank()
        if rank is None:
            raise Exception("rank must have a value")

        return rank == 5

    def execute(self, next_action:HanabiMove , hanabi_environment: rl_env.HanabiEnv) -> None:
        """execute"""
        hanabi_state = hanabi_environment.state.copy()

        current_life_tokens = int(hanabi_state.life_tokens())
        action_type: HanabiMoveType = next_action.type()

        self.discard = action_type == HanabiMoveType.DISCARD
        self.play = action_type == HanabiMoveType.PLAY
        self.hint = action_type == HanabiMoveType.REVEAL_COLOR | HanabiMoveType.REVEAL_RANK

        if action_type == HanabiMoveType.DISCARD:
            self.discard_playable = self.is_discard_playable(next_action, hanabi_state)
            self.discard_useless = self.is_discard_useless(next_action, hanabi_state)
            self.discard_unique = self.is_discard_unique(next_action, hanabi_state)

        hanabi_state.apply_move(next_action)

        next_life_tokens = int(hanabi_state.life_tokens())

        self.lost_one_life_token = current_life_tokens != next_life_tokens
        self.lost_all_life_tokens = current_life_tokens <= 0
        self.successfully_played_a_card = not self.lost_all_life_tokens
