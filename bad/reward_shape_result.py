# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, too-many-arguments, line-too-long, too-many-instance-attributes
class RewardShapeResult:
    """reward shape result"""
    def __init__(self, lost_one_life_token: float, lost_all_life_tokens: float, successfully_played_a_card: float,
                discard: float, discard_playable: float, discard_unique: float, discard_useless: float,
                hint: float, play: float
                 ) -> None:
        """init"""
        self.lost_one_life_token = lost_one_life_token
        self.lost_all_life_tokens = lost_all_life_tokens
        self.successfully_played_a_card = successfully_played_a_card
        self.discard = discard
        self.discard_playable = discard_playable
        self.discard_unique = discard_unique
        self.discard_unseless = discard_useless
        self.hint = hint
        self.play = play

    def get_sum(self) -> float:
        """sum"""
        return self.lost_all_life_tokens + self.lost_all_life_tokens + self.discard_playable
