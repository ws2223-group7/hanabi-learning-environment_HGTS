import matplotlib.pyplot as plt

class PlotTotalSelfPlay:
    def __init__(self, episodes_result: list, episodes: int,
                 total_reward: int, max_reward: int, perfect_games: int) -> None:
        self.episodes_result = episodes_result
        self.episodes = episodes
        self.total_reward = total_reward
        self.max_reward = max_reward
        self.perfect_games = perfect_games  

    def plot(self) -> None:
        self.plot_episodes_result()

    def plot_episodes_result(self) -> None:
        x_axis = [x for x in range(self.episodes)]
        results = [self.episodes_result[x].reward 
                   for x in range (len(self.episodes_result))]
        plt.ylabel('Rewards')
        plt.xlabel('Episodes')
        plt.plot(x_axis, results)
        plt.savefig('diagramms/test.png') 