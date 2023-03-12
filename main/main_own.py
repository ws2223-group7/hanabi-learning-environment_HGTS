import sys
import os
import getopt
import time
import numpy as np

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from print_result import console_own_agent
from Agents.htgs_own_agent import HTGSAgentOwn
from hanabi_learning_environment import rl_env


AGENT_CLASSES = {'HTGSAgent3P': HTGSAgentOwn}


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

        # Loop over all Episodes / Games
        for episode in range(self.flags['num_episodes']):
            ### Begin Init Episodes / Rounds ###

            #  At the Beginning of every round reset environment
            observations = self.environment.reset()

            # Init all Agent with agent config
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
            start_time = time.time()

            # Play one game
            while not done:

                # Play one round
                for agent_id, agent in enumerate(agents):

                    # Update Observation
                    self.update_agent(observations, agents)

                    action, legal_move = agent.act()

                    # Update Table
                    if legal_move:
                        for agent3_idx, agent3 in enumerate(agents):
                            agent3.update_tables(action)
                    
                    # Print Game State
                    console_own_agent.info(agents, agent_id, action)

                    # Make an environment step.
                    observations, reward, done, unused_info = self.environment.step(
                        action)

                    episode_reward += reward

            rewards.append(episode_reward)
            total_reward += episode_reward

            # Print Results of the Round
            console_own_agent.round_results(total_reward, episode,
                                            episode_reward, rewards)

        # Print Results over all Rounds
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


def main():
    flags = {'players': 3, 'num_episodes': 10, 'agent_class': 'HTGSAgent3P'}
    runner = Runner(flags)
    runner.run()

if __name__ == "__main__":
    main()