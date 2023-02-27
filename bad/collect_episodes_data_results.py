# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, invalid-name

import sys
import os
import numpy as np

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from bad.collect_episode_data_result import CollectEpisodeDataResult


class CollectEpisodesDataResults:
    '''collect episode data results'''
    def __init__(self) -> None:
        self.results: list[CollectEpisodeDataResult] = []

    def add(self, result: CollectEpisodeDataResult) -> None:
        '''add'''
        self.results.append(result)

    def get_batch_size(self) -> int:
        '''get n'''
        batch_size: int = 0

        for ep in self.results:
            batch_size += len(ep.buffer.actions)

        return batch_size
