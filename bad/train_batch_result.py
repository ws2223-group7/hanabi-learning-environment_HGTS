# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods

class TrainBatchResult:
    '''train batch result'''
    def __init__(self, loss: float, reward: float) -> None:
        self.loss = loss
        self.reward = reward
