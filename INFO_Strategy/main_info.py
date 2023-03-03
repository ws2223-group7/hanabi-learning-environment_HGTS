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
from INFO_Strategy import console
from htgs_info_agent import HTGSAgent
from hanabi_learning_environment.agents.simple_agent import SimpleAgent
from hanabi_learning_environment.agents.random_agent import RandomAgent
from hanabi_learning_environment import rl_env

# Import Error
# from hanabi_learning_environment.agents.test_agent import HTGSAgent


AGENT_CLASSES = {'SimpleAgent': SimpleAgent,
                 'RandomAgent': RandomAgent,
                 'HTGSAgent': HTGSAgent}


class Runner(object):
    """Runner class."""

    def __init__(self, flags):
        """Initialize runner."""
        self.flags = flags
        self.agent_config = {'players': self.flags['players']}
        self.environment = rl_env.make(
            'Hanabi-Full', num_players=self.flags['players'])
        self.agent_class = AGENT_CLASSES[self.flags['agent_class']]

    def run(self):
        """Run episodes."""
        rewards = []
        total_reward = 0

        # Loop over all Episodes / Rounds
        for episode in range(self.flags['num_episodes']):
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
            while not done:

                # Loop over all agents
                for agent_id, agent in enumerate(agents):

                    # Update Observation
                    for agent_id2, agent2 in enumerate(agents):
                        observation = observations['player_observations'][agent_id2]
                        agent2.update_observation(observation)
                        agent2.update_mc()
                        agent2.update_poss_tables_based_on_card_knowledge()

                    action = agent.act(round)

                    # Prüfe ob es sich um eine Legale Aktion handelt
                    # Es ist machmal (warum auch immer) nicht erlaubt zu discarden
                    # Um einen absturtz zu vermeiden wird hier
                    legal_move = True
                    if (action not in agent.observation['legal_moves']):
                        legal_move = False
                        found = False
                        for act_idx, act in enumerate(agent.observation['legal_moves']):
                            if act['action_type'] == 'REVEAL_COLOR' or act['action_type'] == 'REVEAL_RANK':
                                action = agent.observation['legal_moves'][act_idx]
                                found = True

                        if found == False:
                            action = agent.observation['legal_moves'][act_idx]

                    # Ausgabe des aktuellen Spiels vor Aktion:
                    # console.info(agents, agent_id, action)

                    # Update Table
                    if legal_move:
                        for agent3_idx, agent3 in enumerate(agents):
                            agent3.update_tables(action)

                    # Make an environment step.
                    observations, reward, done, unused_info = self.environment.step(
                        action)

                    episode_reward += reward

                round += 1

            rewards.append(episode_reward)
            total_reward += episode_reward

            # Ausgabe der Ergebnisse der Runde
            console.round_results(total_reward, episode,
                                  episode_reward, rewards)

        # Ausgabe des Gesamt Ergebnisses
        end_time = time.time()
        console.overall_results(end_time, start_time,
                                rewards, total_reward, episode)

        return rewards

def main():
    flags = {'players': 5, 'num_episodes': 5, 'agent_class': 'HTGSAgent'}

    runner = Runner(flags)

    if runner.agent_class == HTGSAgent:
        runner.run()
    else:
        sys.exit('Wrong Agent Class!\n')

if __name__ == "__main__":
    main()
