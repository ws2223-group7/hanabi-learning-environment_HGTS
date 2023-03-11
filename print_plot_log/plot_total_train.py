import os
import sys

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from print_plot_log.Logger import Logger
import matplotlib.pyplot as plt

class PlotTraining:
    def plot(self, reward_shaping: bool) -> None:
        self.plot_reward(reward_shaping)

    def plot_reward(self, reward_shaping: bool) -> None:
        
        if reward_shaping:
            logger = Logger('models_with_reward_shaping')
        else:
            logger = Logger('models_without_reward_shaping')

        results = logger.get_all_rewards()
        x_axis = [x for x in range(len(results))]

        plt.ylabel('Rewards  pro Epoche')
        plt.xlabel('Epoche')
        plt.title('Rewards during Training')
        plt.plot(x_axis, results)
        plt.savefig('diagramms/Train.png')


def main():
    plot_training = PlotTraining()
    plot_training.plot_reward()


if __name__ == "__main__":
    main()
