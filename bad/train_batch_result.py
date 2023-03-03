# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods

class TrainBatchResult:
    '''train batch result'''
    def __init__(self, loss: float, game_reward: float, rewards_to_go:float) -> None:
        self.loss = loss
        self.game_reward = game_reward
        self.rewards_to_go = rewards_to_go
