# pylint: disable=missing-module-docstring, wrong-import-position, ungrouped-imports, too-few-public-methods, consider-using-enumerate, line-too-long, line-too-long, too-many-function-args

class BadSetting:
    """bad setting"""
    def __init__(self, with_reward_shaping: bool, batch_size:int, epoch_size: int, gamma:float, learning_rate: float) -> None:
        """init"""
        self.epoch_size = epoch_size
        self.with_reward_shaping = with_reward_shaping
        self.batch_size: int = batch_size
        self.gamma: float = gamma
        self.learning_rate = learning_rate
