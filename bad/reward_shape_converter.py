# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, too-many-arguments, line-too-long

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.reward_shape_result import RewardShapeResult
from bad.reward_shape import RewardShape

class RewardShapeConverter:
    """reward shape converter"""
    def convert(self, reward_shape: RewardShape) -> RewardShapeResult:
        """convert"""

        lost_one_life_token = 0 if reward_shape.lost_one_life_token is True else 1
        lost_all_life_tokens: float = -50 if reward_shape.lost_all_life_tokens is True else 1
        successfully_played_a_card: float = 5 if reward_shape.successfully_played_a_card is True else 0

        discard: float = 0 if reward_shape.discard is True else 0
        discard_playable: float = 0 if reward_shape.discard_playable is None else -10 if reward_shape.discard_playable is True else 5
        discard_unique: float = 0 if reward_shape.discard_unique is None else -10 if reward_shape.discard_unique is True else 5
        discard_useless: float = 0 if reward_shape.discard_useless is None else 10 if reward_shape.discard_useless is True else -5

        hint: float = 0.1 if reward_shape.hint is True else 0
        play: float = 0.5 if reward_shape.play is True else 0

        return RewardShapeResult(lost_one_life_token= lost_one_life_token,
                                 lost_all_life_tokens= lost_all_life_tokens,
                                 successfully_played_a_card= successfully_played_a_card,
                                 discard= discard,
                                 discard_playable= discard_playable,
                                 discard_unique= discard_unique,
                                 discard_useless= discard_useless,
                                 hint= hint,
                                 play= play
                                 )
