# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, too-many-arguments, line-too-long

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment.pyhanabi import HanabiMove
from hanabi_learning_environment import rl_env

class RewardShape:
    '''reward shape'''
    def __init__(self) -> None:
        self.is_legal_action: bool = False
        self.lost_one_life_token: bool = False
        self.discard_neutral: bool = False
        self.play_neutral: bool = False
        self.hint_neutral: bool = False
        self.discard_playable: bool = False
        self.discard_useless: bool = False
        self.discard_unique: bool = False

    def execute(self, next_move:HanabiMove , hanabi_environment: rl_env.HanabiEnv) -> None:
        """execute"""
        hanabi_state = hanabi_environment.state.copy()
        self.is_legal_action = hanabi_state.move_is_legal(next_move)
