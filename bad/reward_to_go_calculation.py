# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, line-too-long, consider-using-enumerate, unused-variable

import sys
import os
import numpy as np

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.collect_batch_results import CollectBatchResults
from bad.rewards_to_go_episode_calculation_result import RewardsCalculationResult
from bad.rewards_to_go_calculation_result import RewardsToGoCalculationResult
from bad.reward_shape_converter import RewardShapeConverter
from bad.game_buffer import GameBuffer

class RewardToGoCalculation:
    ''''calculate reward to go'''
    def __init__(self, gamma: float) -> None:
        self.gamma = gamma

    def calculate(self, buffer: GameBuffer, result: RewardsCalculationResult) -> None:
        ''''calculate episode'''

        reward_shape_converter = RewardShapeConverter()

        for index in range(len(buffer.bayesian_actions)): # über jede aktion (pro spiel)
            reward_shape = reward_shape_converter.convert(buffer.reward_shapes[index])
            # hier rewards verändern
            reward_vom_hanabi_framework = float(np.sum(buffer.rewards[index:]))
            reward_vom_reward_shaping = 0.0 # reward_shape.get_sum()

            reward_to_go = reward_vom_hanabi_framework + reward_vom_reward_shaping
            discounted_reward_to_go = reward_to_go * np.power(self.gamma, index + 1)
            observation = buffer.observation[index]
            bayesian_actions = buffer.bayesian_actions[index]

            result.append(bayesian_actions.sampled_action, discounted_reward_to_go, reward_vom_hanabi_framework, observation)

    def execute(self,collected_batch_results: CollectBatchResults) -> RewardsToGoCalculationResult:
        """execute"""
        episodes_result = RewardsToGoCalculationResult(collected_batch_results.get_games_played())

        for batch_result in collected_batch_results.results:
            reward_calculation_result = RewardsCalculationResult()
            episodes_result.append(reward_calculation_result)

            buffer = batch_result.buffer
            self.calculate(buffer, reward_calculation_result)

        return episodes_result
