import logging
import re
import os
import numpy as np

from print_plot_log.helpfunction import read_epoch_number

class Logger:
    def __init__(self, modelpath, level=logging.DEBUG):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.modelpath = modelpath
        self.filename = 'log_reward_shaping.txt' if modelpath == 'models_with_reward_shaping' else 'log_no_reward_shaping.txt'
        handler = logging.FileHandler(self.filename)
        handler.setLevel(level)
        
        self.logger.addHandler(handler)

    def log_reward(self, reward: float):
        epoch_number = read_epoch_number(self.modelpath)
        self.logger.log(logging.DEBUG, f'Rewards in Epoch {epoch_number}: {reward}')
    """
    def get_rewards_for_epoch(self, epoch: int):
        # Define the regular expression pattern to match log messages for the given epoch
        pattern = f"Rewards in Epoch {epoch}: \\[([0-9, ]*)\\]"

        # Open the log file in read mode
        with open('mylog.log', 'r') as file:
            # Loop over each line in the file
            for line in file:
                # Try to match the regular expression pattern in the line
                match = re.match(pattern, line)
                if match:
                    # If the pattern matches, extract the rewards list from the matched group
                    rewards_list = [int(x.strip()) for x in match.group(1).split(',')]
                    return rewards_list

        # If no matching log messages were found, return an empty list
        return []
    """
    def get_reward_for_epoch(self, episode):
        
        with open(self.filename, 'r') as f:
            for line in f:
                match = re.match(r'^Rewards in Epoch (\d+): ([\d\.]+)$', line)
                if match:
                    epoch = int(match.group(1))
                    reward = float(match.group(2))
                    if epoch == episode:
                        return reward

    def get_all_rewards(self):
        rewards = []
        with open(self.filename, 'r') as f:
            for line in f:
                match = re.match(r'^Rewards in Epoch \d+: ([\d\.]+)$', line)
                if match:
                    reward = float(match.group(1))
                    rewards.append(reward)
        return rewards
