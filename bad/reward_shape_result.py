# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, too-many-arguments, line-too-long
class RewardShapeResult:
    """reward shape result"""
    def __init__(self, lost_one_life_token: float, lost_all_life_tokens: float, discard_playable: float) -> None:
        """init"""
        self.lost_one_life_token = lost_one_life_token
        self.lost_all_life_tokens = lost_all_life_tokens
        self.discard_playable = discard_playable

    def get_sum(self) -> float:
        """sum"""
        return self.lost_all_life_tokens + self.lost_all_life_tokens + self.discard_playable
