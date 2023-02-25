# pylint: disable=missing-module-docstring, wrong-import-position, no-name-in-module, unused-variable, unused-variable

import os
import random
import sys
import numpy as np
import tensorflow as tf


currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.self_play import SelfPlay
from bad.train_batches import TrainBatches
from bad.action_network import ActionNetwork

def main() -> None:
    '''main'''
    seed = 42
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

    batch_size: int = 20
    episodes_running = 100
    gamma = 0.95

    model_path = 'model'


    print(f'welcome to bad agent with tf version: {tf.__version__}')
    print(f'running {episodes_running} episodes')

    network: ActionNetwork = ActionNetwork(model_path)

    #if os.path.exists(model_path):
    #    network.load()

    train_batches = TrainBatches(network)
    training_result = train_batches.run(batch_size=batch_size, gamma=gamma)

    #network.save()

    #self_play = SelfPlay(network)
    #self_play.run(episodes_running)

    print("finish with everything")
if __name__ == "__main__":
    main()
