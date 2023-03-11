# pylint: disable=missing-module-docstring, wrong-import-position, no-name-in-module, unused-variable, unused-variable, line-too-long, ungrouped-imports
import os
import random
import sys
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt  

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment import pyhanabi, rl_env
from bad.action_network import ActionNetwork
from bad.self_play import SelfPlay
from bad.train_epoch import TrainEpoch
from bad.constants import Constants
from bad.bad_setting import BadSetting
from print_plot_log.plot_total_train import PlotTraining
from print_plot_log.Logger import Logger

def main() -> None:
    '''main'''
    seed = 42
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    tf.keras.utils.set_random_seed(seed)  # sets seeds for base-python, numpy and tf
    tf.config.experimental.enable_op_determinism()

    bad_setting = BadSetting(batch_size= 1000, epoch_size= 2, gamma= 1.0, learning_rate=0.0001, with_reward_shaping= True)

    episodes_running: int = 100
    model_path = 'models_with_reward_shaping' if bad_setting.with_reward_shaping is True else 'models_without_reward_shaping'


    print(f'welcome to bad agent with tf version: {tf.__version__}')
    print(f'running {episodes_running} episodes')

    constants = Constants()
    players = 2
    hanabi_environment = rl_env.make(constants.environment_name, players, pyhanabi.AgentObservationType.SEER)
    network: ActionNetwork = ActionNetwork(model_path, bad_setting.learning_rate)

    if network.exists():
        network.load()

    train_epoch = TrainEpoch(network, hanabi_environment, players)

    logger = Logger(model_path)
    
    result_training = []
 
    for epoch in range(bad_setting.epoch_size):
        print('')
        print(f'running epoch: {epoch}')

        result = train_epoch.train(bad_setting)
        avg_reward = result.reward / result.games_played
        logger.log_reward(avg_reward)
        
        print(f"epoch reward: {avg_reward}")
        network.save()


    train_plot = PlotTraining()
    train_plot.plot_reward(bad_setting.with_reward_shaping)

    self_play = SelfPlay(network)
    self_play.run(episodes_running)

    print("finish with everything")


if __name__ == "__main__":
    main()