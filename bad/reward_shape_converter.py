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

        lost_one_life_token = -10 if reward_shape.lost_one_life_token is True else 1
        lost_all_life_tokens: float = -50 if reward_shape.lost_all_life_tokens is True else 1
        discard_playable: float = -10 if reward_shape.discard_playable is True else 0

        return RewardShapeResult(lost_one_life_token, lost_all_life_tokens, discard_playable)
