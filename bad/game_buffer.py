# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, too-many-arguments, ungrouped-imports, line-too-long

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.bayesian_action_result import BayesianActionResult
from bad.encoding.observation import Observation
from hanabi_learning_environment.pyhanabi import HanabiMove
from bad.reward_shape import RewardShape

class GameBuffer:
    '''buffer'''
    def __init__(self) -> None:
        self.hanabi_observation: list[dict] = []
        self.observation: list[Observation] = []
        self.bayesian_actions: list[BayesianActionResult] = []
        self.rewards: list[int] = []
        self.moves: list[HanabiMove] = []
        self.reward_shapes: list[RewardShape] =  []

    def append(self, hanabi_observation: dict, observation: Observation, \
    action_result: BayesianActionResult, reward: int, move: HanabiMove, reward_shape: RewardShape) -> None:
        '''add'''
        self.hanabi_observation.append(hanabi_observation)
        self.observation.append(observation)
        self.bayesian_actions.append(action_result)
        self.rewards.append(reward)
        self.moves.append(move)
        self.reward_shapes.append(reward_shape)
