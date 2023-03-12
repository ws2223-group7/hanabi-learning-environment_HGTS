# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A simple episode runner using the RL environment."""


import sys
import os
import getopt
import time
import numpy as np

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment.rl_env import Agent
from print_result import console_own_agent
from Agents.htgs_info_agent import HTGSAgent
from Agents.htgs_own_agent import HTGSAgent3P
from hanabi_learning_environment.agents.simple_agent import SimpleAgent
from hanabi_learning_environment.agents.random_agent import RandomAgent
from hanabi_learning_environment import rl_env

# Import Error
# from hanabi_learning_environment.agents.test_agent import HTGSAgent


AGENT_CLASSES = {'SimpleAgent': SimpleAgent,
                 'RandomAgent': RandomAgent,
                 'HTGSAgent': HTGSAgent,
                 'HTGSAgent3P': HTGSAgent3P}


class Runner(object):
    """Runner class."""

    def __init__(self, flags):
        """Initialize runner."""
        self.flags = flags
        self.agent_config = {'players': flags['players']}
        self.environment = rl_env.make(
            'Hanabi-Full', num_players=flags['players'])
        self.agent_class = AGENT_CLASSES[flags['agent_class']]

    def run(self):
        """Run episodes."""
        rewards = []
        total_reward = 0

        # Loop over all Episodes / Rounds
        for episode in range(flags['num_episodes']):
            ### Begin Init Episodes / Rounds ###

            #  At the Beginning of every round reset environment
            observations = self.environment.reset()

            # Init all Agent with agent config
            # Nacharbeit: Wenn in jedem spiel neue Agent erstellt werden muss
            # die Policy wo anderes gespeichert werden
            agents = [self.agent_class(self.agent_config)
                      for _ in range(self.flags['players'])]

            # Init Possibility Table
            for agent_id, agent in enumerate(agents):
                observation = observations['player_observations'][agent_id]
                agent.init_table(observation)

            # done is bool for gameOver or Win
            done = False
            episode_reward = 0

            ### End Init Episodes / Rounds ###
            # Play as long its not gameOver or Win
            round = 1
            start_time = time.time()

            # Play one game
            while not done:

                # Play one round
                for agent_id, agent in enumerate(agents):

                    # Update Observation
                    self.update_agent(observations, agents)

                    action, legal_move = agent.act(round)

                    # Update Table
                    if legal_move:
                        for agent3_idx, agent3 in enumerate(agents):
                            agent3.update_tables(action)

                    # Make an environment step.
                    observations, reward, done, unused_info = self.environment.step(
                        action)

                    episode_reward += reward

                

            rewards.append(episode_reward)
            total_reward += episode_reward

            # Ausgabe der Ergebnisse der Runde
            console_own_agent.round_results(total_reward, episode,
                                  episode_reward, rewards)

        # Ausgabe des Gesamt Ergebnisses
        end_time = time.time()
        console_own_agent.overall_results(end_time, start_time,
                                rewards, total_reward, episode)

        return rewards

    def update_agent(self, observations, agents):
        for agent_id2, agent2 in enumerate(agents):
            observation = observations['player_observations'][agent_id2]
            agent2.update_observation(observation)
            agent2.update_mc()
            agent2.update_poss_tables_based_on_card_knowledge()



if __name__ == "__main__":

    flags = {'players': 3, 'num_episodes': 150, 'agent_class': 'HTGSAgent3P'}

    runner = Runner(flags)

    if runner.agent_class == HTGSAgent3P:
        runner.run()
    else:
        sys.exit('Wrong Agent Class!\n')
