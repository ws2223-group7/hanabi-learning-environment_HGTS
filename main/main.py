# pylint: disable=missing-module-docstring, wrong-import-position, no-name-in-module, unused-variable, unused-variable, line-too-long, ungrouped-imports
import os
import random
import sys
import numpy as np
import tensorflow as tf

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment import pyhanabi, rl_env
from bad.action_network import ActionNetwork
from bad.self_play import SelfPlay
from bad.train_epoch import TrainEpoch
from bad.constants import Constants

def main() -> None:
    '''main'''
    seed = 42
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    tf.keras.utils.set_random_seed(seed)  # sets seeds for base-python, numpy and tf
    tf.config.experimental.enable_op_determinism()

    batch_size: int = 1000
    epoch_size: int = 1

    episodes_running: int = 10
    gamma: float = 1.0

    model_path = 'model'


    print(f'welcome to bad agent with tf version: {tf.__version__}')
    print(f'running {episodes_running} episodes')

    constants = Constants()
    players = 2
    hanabi_environment = rl_env.make(constants.environment_name, players, pyhanabi.AgentObservationType.SEER)
    network: ActionNetwork = ActionNetwork(model_path)

    #if os.path.exists(model_path):
    #    network.load()

    train_epoch = TrainEpoch(network, hanabi_environment, players)

    for epoch in range(epoch_size):
        print('')
        print(f'running epoch: {epoch}')

        result = train_epoch.train(batch_size, gamma)
        print(f"epoch reward: {result.reward / result.games_played}")

    #network.save()

    self_play = SelfPlay(network)
    self_play.run(episodes_running)

    print("finish with everything")


if __name__ == "__main__":
    main()
