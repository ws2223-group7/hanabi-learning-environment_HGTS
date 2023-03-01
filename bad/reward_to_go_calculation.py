# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, line-too-long, consider-using-enumerate

import sys
import os
import numpy as np

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.collect_episodes_data_results import CollectEpisodesDataResults
from bad.rewards_to_go_episode_calculation_result import RewardsToGoEpisodeCalculationResult
from bad.rewards_to_go_calculation_result import RewardsToGoCalculationResult
from bad.reward_shape_converter import RewardShapeConverter
from bad.buffer import Buffer

class RewardToGoCalculation:
    ''''calculate reward to go'''
    def __init__(self, gamma: float) -> None:
        self.gamma = gamma

    def calculate(self, buffer: Buffer, result: RewardsToGoEpisodeCalculationResult) -> None:
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

            result.append(bayesian_actions.sampled_action, bayesian_actions.categorical.log_prob(bayesian_actions.sampled_action).numpy(), discounted_reward_to_go, observation)

    def run(self,collected_episode_results: CollectEpisodesDataResults) -> RewardsToGoCalculationResult:
        '''run'''

        episodes_result = RewardsToGoCalculationResult()

        for episode_result in collected_episode_results.results:
            ep_result = RewardsToGoEpisodeCalculationResult()
            episodes_result.append(ep_result)

            buffer = episode_result.buffer
            self.calculate(buffer, ep_result)

        return episodes_result
