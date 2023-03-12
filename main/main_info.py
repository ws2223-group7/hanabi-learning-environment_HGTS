import sys
import os
import time

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from print_result import console_info_agent
from Agents.htgs_info_agent import HTGSAgentInfo
from hanabi_learning_environment import rl_env


AGENT_CLASSES = {'HTGSAgent': HTGSAgentInfo}


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
        for episode in range(self.flags['num_episodes']):
            
            episode_reward = 0
            done = False
            legal_move = None
            action = None
            

            # Set Up new Game environment
            observations = self.environment.reset()

            # Init all Agent 
            agents = self.init_agents(observations)


            # Play a Game
            start_time = time.time()
            while not done:

                # Play a Round
                for agent_id, agent in enumerate(agents):

                     # Update Agent Knowledge
                    self.update_agent(observations, agents, legal_move, action)

                    # Current Agent Action
                    action, legal_move = agent.act()

                    # Print Game Info:
                    console_info_agent.info(agents, agent_id, action)

                    # Make an environment step.
                    observations, reward, done, unused_info = self.environment.step(
                        action)

                    episode_reward += reward

            rewards.append(episode_reward)
            total_reward += episode_reward

            # Print Round Results
            console_info_agent.round_results(total_reward, episode,
                                  episode_reward, rewards)

        # Print Overall Results
        end_time = time.time()
        console_info_agent.overall_results(end_time, start_time,
                                rewards, total_reward, episode)

        return rewards
    
    def init_agents(self, observations):
        
        # Init all Agent with agent config
        agents = [self.agent_class(self.agent_config)
                    for _ in range(self.flags['players'])]

        # Init Possibility Table
        for agent_id, agent in enumerate(agents):
            observation = observations['player_observations'][agent_id]
            agent.init_table(observation)
        
        return agents
    
    def update_agent(self, observations, agents, legal_move, action):
        # Update Observation
        if legal_move:
            for agent3_idx, agent3 in enumerate(agents):
                agent3.update_tables(action)

        for agent_id2, agent2 in enumerate(agents):
            observation = observations['player_observations'][agent_id2]
            agent2.update_observation(observation)
            agent2.update_mc()
            agent2.update_poss_tables_based_on_card_knowledge()

def main():
    flags = {'players': 3, 'num_episodes': 100, 'agent_class': 'HTGSAgent'}
    runner = Runner(flags)
    runner.run()

if __name__ == "__main__":
    main()

