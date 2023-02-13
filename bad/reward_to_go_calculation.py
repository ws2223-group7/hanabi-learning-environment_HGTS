# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, line-too-long

import sys
import os
import numpy as np


currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.collect_episodes_data_results import CollectEpisodesDataResults
from bad.rewards_to_go_episode_calculation_result import RewardsToGoEpisodeCalculationResult
from bad.rewards_to_go_calculation_result import RewardsToGoCalculationResult
from bad.buffer import Buffer

class RewardToGoCalculation:
    ''''calculate reward to go'''
    def __init__(self, gamma: float) -> None:
        self.gamma = gamma

    def calculate_episode(self, buffer: Buffer, result: RewardsToGoEpisodeCalculationResult) -> None:
        ''''calculate episode'''

        for index in range(len(buffer.actions)): # über jede aktion (pro spiel)
            reward_to_go = float(np.sum(buffer.rewards[index:]))
            discounted_reward_to_go = reward_to_go * np.power(self.gamma, index + 1)

            action = buffer.actions[index]
            log_prob = action.categorical.log_prob(action.sampled_action)
            observation = buffer.observation[index]
            # loss calculation
            current_loss = -(discounted_reward_to_go * float(log_prob.numpy()))

            result.append(discounted_reward_to_go, current_loss, observation)

    def run(self,collected_episode_results: CollectEpisodesDataResults) -> RewardsToGoCalculationResult:
        '''run'''

        episodes_result = RewardsToGoCalculationResult()

        for episode_result in collected_episode_results.results:
            ep_result = RewardsToGoEpisodeCalculationResult()
            episodes_result.append(ep_result)

            buffer = episode_result.buffer
            self.calculate_episode(buffer, ep_result)

        return episodes_result
