# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, consider-using-enumerate, line-too-long, line-too-long
class TrainEpochResult:
    """train epoch result"""
    def __init__(self, loss: float, reward: float, games_played: int) -> None:
        self.loss = loss
        self.reward = reward
        self.games_played = games_played
