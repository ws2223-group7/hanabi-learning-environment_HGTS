# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, invalid-name
import sys
import os
import numpy as np


currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.rewards_to_go_episode_calculation_result import RewardsCalculationResult
from bad.baseline import Baseline

class RewardsToGoCalculationResult:
    """RewardToGoCalculationResult"""
    def __init__(self, games_played) -> None:
        self.results: list[RewardsCalculationResult] = []
        self.games_played = games_played

    def append(self, result: RewardsCalculationResult):
        '''append'''
        self.results.append(result)

    def get_games_played(self) -> int:
        """get games played"""
        return self.games_played

    def get_batch_size(self) -> int:
        """get n"""
        batch_size: int = 0

        for ep in self.results:
            batch_size += len(ep.actions)

        return batch_size

    def get_rewards_to_go(self) -> np.ndarray:
        """get rewards"""
        total = np.empty(0, float)

        for res in self.results:
            total = np.append(total, res.rewards_to_go)

        return total

    def get_baseline(self) -> Baseline:
        """get baseline"""
        rewards = self.get_rewards_to_go()
        return Baseline(rewards.mean(), rewards.std())

    def get_rewards_to_go_sum(self) -> float:
        """get rewards to go sum"""
        rewards = self.get_rewards_to_go()

        return rewards.sum()

    def get_game_rewards(self) -> np.ndarray:
        """get game rewards"""
        total = np.empty(0, float)

        for res in self.results:
            total = np.append(total, res.game_rewards)

        return total

    def get_game_rewards_sum(self) -> float:
        """get game reward"""
        rewards = self.get_game_rewards()
        return rewards.sum()
