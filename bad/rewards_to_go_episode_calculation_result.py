# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, line-too-long

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.encoding.observation import Observation


class RewardsCalculationResult:
    '''RewardsToGoEpisodeCalculationResult'''
    def __init__(self) -> None:
        self.rewards_to_go: list[float] = []
        self.game_rewards: list[float] = []
        self.actions: list[int] = []
        self.observation: list[Observation] = []

    def append(self, action: int, reward_to_go: float, game_rewards:float, observation: Observation) -> None:
        '''add'''
        self.actions.append(action)
        self.rewards_to_go.append(reward_to_go)
        self.game_rewards.append(game_rewards)
        self.observation.append(observation)
