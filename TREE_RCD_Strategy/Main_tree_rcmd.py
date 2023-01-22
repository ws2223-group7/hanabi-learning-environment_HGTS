from __future__ import print_function

import sys
import os
import getopt
import math

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment import rl_env
from hanabi_learning_environment.agents.random_agent import RandomAgent
from hanabi_learning_environment.agents.simple_agent import SimpleAgent

# from hanabi_learning_environment.agents.test_agent import HTGSAgent 
from htgs_tree_rcmd_agent import HTGS_TREE_RCMDAgent

AGENT_CLASSES = {'HTGS_TREE_RCMDAgent' : HTGS_TREE_RCMDAgent}
          
class Runner(object):
  """Runner class."""

  def __init__(self, flags):
    """Initialize runner."""
    self.flags = flags
    self.agent_config = {'players': flags['players']}
    self.environment = rl_env.make('Hanabi-Full', num_players=flags['players'])
    self.agent_class = AGENT_CLASSES[flags['agent_class']]

  def run(self):
    episodesTS=10
    breadth = 10
    tree_depth = math.log(episodesTS,breadth)

    total_outer_reward = 0
    outer_rewards = []
    outer_score_vec = [0]*26

    for episode in range(self.flags['num_episodes']):
      # Outer loop over num_episodes
      total_inner_reward = 0
      inner_rewards = []
      inner_score_vec = [0]*26
      outer_episode_reward = 0

      # Inner loop for Tree Search
      for episodeTS in range(episodesTS):
        observations = self.environment.reset() 
        agents = [self.agent_class(self.agent_config)
                  for _ in range(self.flags['players'])]
        done = False
        inner_episode_reward = 0
        while not done:
          for agent_id, agent in enumerate(agents):
            observation = observations['player_observations'][agent_id]
            action = agent.act(observation)
            legal_move = True
            if (action not in agent.observation['legal_moves']):
              legal_move = False
              found = False
              for act_idx, act in enumerate (agent.observation['legal_moves']): 
                  if act['action_type'] == 'REVEAL_COLOR' or act['action_type'] == 'REVEAL_RANK':
                    action = agent.observation['legal_moves'][act_idx]
                    found = True 
              if found == False:
                action = agent.observation['legal_moves'][act_idx]               
            # If hint is given calculate the corresponding hat  
            if (action['action_type'] == 'REVEAL_COLOR' 
              or action['action_type'] == 'REVEAL_RANK'):
              for agent_id2, agent2 in enumerate(agents):
                if agent_id == agent_id2:
                  continue 
                agent2.observation = observations['player_observations'][agent_id2]
                agent2_hand = observations['player_observations'][agent_id2-1]['observed_hands'][1]
                if legal_move:
                  agent2.decode_hint(action, agent2_hand)
            if (action['action_type'] == 'PLAY'):
              for agent3 in agents:
                agent3.nr_card_ply_since_hint += 1
            if observation['current_player'] == agent_id:
              assert action is not None
              current_player_action = action
            else:
              assert action is None
            observations, inner_reward, done, unused_info = self.environment.step(
                current_player_action)
            inner_episode_reward += inner_reward
        inner_rewards.append(inner_episode_reward)
        total_inner_reward += inner_episode_reward
        inner_score_vec[inner_episode_reward]+= 1
#        print('Running inner episode: %d' % episodeTS)
#        print('Inner episode Reward:  %d' % inner_episode_reward)
#        print('Max  inner Reward: %.3f' % max(inner_rewards))
#        print('Avg. inner Reward: %.3f' % (total_inner_reward/(episodeTS+1)))
#        print('RCMD-TREE-INNER----')
      print('INFO-TREE-OUTER----')
      print(inner_rewards)
      print('Running outer episode: %d' % episode)
      outer_episode_reward = func_MinMax(0,0,True,inner_rewards,tree_depth, breadth)
      print('Episode outer Reward:  %d' % outer_episode_reward)
      outer_rewards.append(outer_episode_reward)
      outer_score_vec[outer_episode_reward]+= 1
      total_outer_reward += outer_episode_reward
    print('Max  outer Reward: %.3f' % max(outer_rewards))
    print('Avg. outer Reward: %.3f' % (total_outer_reward/(episode+1)))
    print('Total outer Reward:  %d' % total_outer_reward)
    print('Running outer episode: %d' % episode)
    print(outer_score_vec)
    return

def func_MinMax(current_depth, node_value, max_turn, score, target_depth, breadth):
    vec = []
    if(current_depth == target_depth): 
        return score[node_value]
    if(max_turn):
#        print("max_turn: {} current_depth {} node_value {} target_depth {}".format(max_turn, current_depth,node_value, target_depth) )
        for i in range(breadth):
          vec.append(func_MinMax(current_depth+1, node_value*2+i, False, score, target_depth, breadth))
        return max(vec)
    else:
#        print("min_turn: {} current_depth {} node_value {} target_depth {}".format(max_turn, current_depth,node_value, target_depth) )
        for i in range(breadth):
          vec.append(func_MinMax(current_depth+1, node_value*2+i, True, score, target_depth ,breadth))
        return min(vec)


def main():
  flags = {'players': 4, 'num_episodes': 100, 'agent_class': 'HTGS_TREE_RCMDAgent'}
  options, arguments = getopt.getopt(sys.argv[1:], '',
                                     ['players=',
                                      'num_episodes=',
                                      'agent_class='])
  if arguments:
    sys.exit('usage: rl_env_example.py [options]\n'
             '--players       number of players in the game.\n'
             '--num_episodes  number of game episodes to run.\n'
             '--agent_class   {}'.format(' or '.join(AGENT_CLASSES.keys())))
  for flag, value in options:
    flag = flag[2:]  # Strip leading --.
    flags[flag] = type(flags[flag])(value)
  runner = Runner(flags)
  if runner.agent_class == HTGS_TREE_RCMDAgent: 
    runner.run()
  else: sys.exit('Wrong Agent Class!\n')

if __name__ == "__main__":
  main()

  