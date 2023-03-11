import matplotlib.pyplot as plt

class PlotTotalSelfPlay:
    def __init__(self, result_traning) -> None:
        self.result_traning = result_traning

    def plot(self) -> None:
        self.plot_reward()

    def plot_reward(self) -> None:
        x_axis = [x for x in range(len(self.result_traning))]
        results = [self.result_traning[x].reward 
                   for x in range (len(self.result_traning))]
        plt.ylabel('Rewards  pro Epoche')
        plt.xlabel('Epoche')
        plt.title('Rewards during Training')
        plt.plot(x_axis, results)
        plt.savefig('diagramms/Train.png') 