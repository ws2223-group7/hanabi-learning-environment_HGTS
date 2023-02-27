# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, consider-using-enumerate, line-too-long, line-too-long
class TrainEpochResult:
    """train epoch result"""
    def __init__(self, loss: float) -> None:
        self.loss = loss
