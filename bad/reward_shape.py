# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, too-many-arguments, line-too-long

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment.pyhanabi import HanabiCardKnowledge, HanabiMove, HanabiMoveType, HanabiState
from hanabi_learning_environment import rl_env

class RewardShape:
    '''reward shape'''
    def __init__(self) -> None:
        self.lost_one_life_token: bool = False
        self.lost_all_life_tokens: bool = False
        self.discard_neutral: bool = False
        self.play_neutral: bool = False
        self.hint_neutral: bool = False
        self.discard_playable: bool = False
        self.discard_useless: bool = False
        self.discard_unique: bool = False

    def is_discard_playable(self, next_move: HanabiMove, hanabi_state: HanabiState) -> bool:
        """execute discard playable"""
        my_dict = next_move.to_dict()
        card_index = int(my_dict["card_index"])
        obs = hanabi_state.observation(hanabi_state.cur_player())
        card_knowledge:HanabiCardKnowledge = obs.card_knowledge()[hanabi_state.cur_player()][card_index]
        return bool(obs.card_playable_on_fireworks(card_knowledge.color(), card_knowledge.rank()))

    def execute(self, next_action:HanabiMove , hanabi_environment: rl_env.HanabiEnv) -> None:
        """execute"""
        hanabi_state = hanabi_environment.state.copy()   

        current_life_tokens = int(hanabi_state.life_tokens())
        action_type: HanabiMoveType = next_action.type()

        if action_type == HanabiMoveType.DISCARD:
            self.discard_playable = self.is_discard_playable(next_action, hanabi_state)

        hanabi_state.apply_move(next_action)

        next_life_tokens = int(hanabi_state.life_tokens())

        self.lost_one_life_token = current_life_tokens != next_life_tokens
        self.lost_all_life_tokens = current_life_tokens <= 0
