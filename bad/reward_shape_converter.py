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
        return RewardShapeResult(reward_shape.is_legal_action)
