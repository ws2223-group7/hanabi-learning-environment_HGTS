# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, invalid-name
import sys
import os
import numpy as np


currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.rewards_to_go_episode_calculation_result import RewardsToGoEpisodeCalculationResult
from bad.baseline import Baseline

class RewardsToGoCalculationResult:
    '''RewardToGoCalculationResult'''
    def __init__(self) -> None:
        self.results: list[RewardsToGoEpisodeCalculationResult] = []

    def append(self, result: RewardsToGoEpisodeCalculationResult):
        '''append'''
        self.results.append(result)

    def get_batch_size(self) -> int:
        '''get n'''
        batch_size: int = 0

        for ep in self.results:
            batch_size += len(ep.actions)

        return batch_size

    def get_baseline(self) -> Baseline:
        """get baseline"""
        total = np.empty(0, float)

        for res in self.results:
            total = np.append(total, res.rewards_to_go)

        return Baseline(total.mean(), total.std())
