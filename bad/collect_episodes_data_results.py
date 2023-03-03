# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, invalid-name

import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.collect_episode_data_result import CollectGameResult


class CollectBatchResults:
    """collect bactch data results"""
    def __init__(self) -> None:
        self.results: list[CollectGameResult] = []

    def add(self, result: CollectGameResult) -> None:
        '''add'''
        self.results.append(result)

    def games_played(self) -> int:
        """games played"""
        return self.results.count()

    def get_batch_size(self) -> int:
        """get batch size"""
        batch_size: int = 0

        for ep in self.results:
            batch_size += len(ep.buffer.bayesian_actions)

        return batch_size
