# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, line-too-long

class TrainBatchResult:
    '''train batch result'''
    def __init__(self, loss: float, game_reward: float, rewards_to_go:float, games_played: int) -> None:
        """init"""
        self.loss = loss
        self.game_reward = game_reward
        self.rewards_to_go = rewards_to_go
        self.games_played = games_played
