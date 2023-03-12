import sys
import os
import time

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from print_result import console_rec_agent
from Agents.htgs_rec_agent import HTGSAgent
from hanabi_learning_environment import rl_env

# from hanabi_learning_environment.agents.test_agent import HTGSAgent

AGENT_CLASSES = {'HTGSAgent': HTGSAgent}


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

        action = None
        legal_move = None
        output = False

        # Play as many games as specified in flags
        for episode in range(self.flags['num_episodes']):

            # Init Environment
            observations = self.environment.reset()

            # Init all Agent
            agents = [self.agent_class(self.agent_config)
                      for _ in range(self.flags['players'])]

            # done is bool for gameOver or Win
            game_fished = False

            episode_reward = 0

            start_time = time.time()

            # Play one game
            while not game_fished:

                # Play one round:
                for agent_id, agent in enumerate(agents):

                    # Update Observation for all Agents
                    self.update_observation(
                        observations, agents, action, agent_id, legal_move)

                    observation = observations['player_observations'][agent_id]
                    action, legal_move = agent.act(observation)

                    self.update_action(observations, agents,
                                       action, agent_id, legal_move)

                    # Ausgabe des aktuellen Spiels vor Aktion:
                    console_rec_agent.info(
                        observations, agents, agent_id, action)

                    # Make an environment step.
                    observations, reward, game_fished, unused_info = self.environment.step(
                        action)

                    episode_reward += reward

            rewards.append(episode_reward)
            total_reward += episode_reward

            # Ausgabe der Ergebnisse der Runde
            console_rec_agent.round_results(total_reward, episode,
                                            episode_reward, rewards)

        # Ausgabe des Gesamt Ergebnisses
        end_time = time.time()
        console_rec_agent.overall_results(end_time, start_time,
                                          rewards, total_reward, episode)
        return rewards

    def update_observation(self, observations, agents, action, agent_id, legal_move):
        """Updates the agents based on new observation."""
        for agent_id2, agent2 in enumerate(agents):
            observation = observations['player_observations'][agent_id2]
            agent2.update_observation(observation)

    def update_action(self, observations, agents, action, agent_id, legal_move):
        """Updates the agent's based on the action."""
        if ((action['action_type'] == 'REVEAL_COLOR'
            or action['action_type'] == 'REVEAL_RANK')
                and legal_move):

            self.decode_hint(observations, agents, agent_id, action)

        if (action['action_type'] == 'PLAY'):
            for agent3 in agents:
                agent3.nr_card_ply_since_hint += 1

    def decode_hint(self, observations, agents, agent_id, action):
        """Agent decode hint to recommanded action"""
        for agent_id2, agent2 in enumerate(agents):
            if agent_id == agent_id2:
                continue

            # Setze Observation von Spielern die hint bekommen
            agent2.observation = observations['player_observations'][agent_id2]
            agent2_hand = observations['player_observations'][agent_id2 -
                                                              1]['observed_hands'][1]
            agent2.decode_hint(action, agent2_hand)

def main():
    flags = {'players': 5, 'num_episodes': 10, 'agent_class': 'HTGSAgent'}
    runner = Runner(flags)
    runner.run()

if __name__ == "__main__":
    main()
