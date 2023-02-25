# pylint: disable=missing-module-docstring, wrong-import-position, no-member, no-name-in-module, too-few-public-methods, line-too-long, ungrouped-imports
import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment import rl_env
from hanabi_learning_environment.pyhanabi import HanabiMove
from bad.action_network import ActionNetwork
from bad.encoding.observationconverter import ObservationConverter
from bad.set_extra_observation import SetExtraObservation
from bad.buffer import Buffer
from bad.collect_episode_data_result import CollectEpisodeDataResult
from bad.reward_shape import RewardShape

class CollectEpisodeData:
    '''train episode'''
    def __init__(self, hanabi_observation:dict, hanabi_environment: rl_env.HanabiEnv, \
         network: ActionNetwork) -> None:
        self.hanabi_observation = hanabi_observation
        self.hanabi_environment = hanabi_environment
        self.network = network

    def get_reward_shape(self, next_move: HanabiMove) -> RewardShape:
        '''get reward shape'''
        rewardshape = RewardShape()
        rewardshape.execute(next_move, self.hanabi_environment)
        return rewardshape

    def collect(self) \
         -> CollectEpisodeDataResult:
        '''train within an environment'''

        copied_state = self.hanabi_environment.state.copy()

        buffer = Buffer()

        self.hanabi_environment.state = copied_state.copy()
        # one more move because of no-action move on the beginning
        #fake an action that does not exists
        max_moves: int = self.hanabi_environment.game.max_moves() + 1
        max_actions = max_moves + 1 # 0 index based

        seo = SetExtraObservation()
        seo.set_extra_observation(self.hanabi_observation, max_moves, max_actions, \
            self.hanabi_environment.state.legal_moves_int())

        observation_converter: ObservationConverter = ObservationConverter()
        observation = observation_converter.convert(self.hanabi_observation)

        done = False
        while not done:

            bad = self.network.get_action(observation)
            bad_result = bad.decode_action()
            next_action = bad_result.sampled_action
            hanabi_move = self.hanabi_environment.game.get_move(next_action)
            reward_shape = self.get_reward_shape(hanabi_move)

            observation_after_step, reward, done, _ = self.hanabi_environment.step(next_action)

            buffer.append(self.hanabi_observation, observation, bad_result, reward, hanabi_move, reward_shape)

            seo.set_extra_observation(observation_after_step, next_action, max_actions, \
                self.hanabi_environment.state.legal_moves_int())

            observation = observation_converter.convert(observation_after_step)
            self.hanabi_observation = observation_after_step

        return CollectEpisodeDataResult(buffer)
