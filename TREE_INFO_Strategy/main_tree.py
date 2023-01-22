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

from __future__ import print_function

import sys
import getopt
import math

from hanabi_learning_environment import rl_env
from hanabi_learning_environment.agents.random_agent import RandomAgent
from hanabi_learning_environment.agents.simple_agent import SimpleAgent



# Import Error
# from hanabi_learning_environment.agents.test_agent import HTGSAgent 
from htgs_tree_agent import HTGSTreeAgent



from hanabi_learning_environment.rl_env import Agent

AGENT_CLASSES = {'SimpleAgent': SimpleAgent, 
                 'RandomAgent': RandomAgent, 
### g7_BEGINN ###            
                 'HTGSTreeAgent': HTGSTreeAgent}
### g7_ENDE ###   
#          
class Runner(object):
  """Runner class."""

  def __init__(self, flags):
    """Initialize runner."""
    self.flags = flags
    self.agent_config = {'players': flags['players']}
    self.environment = rl_env.make('Hanabi-Full', num_players=flags['players'])
    self.agent_class = AGENT_CLASSES[flags['agent_class']]

  def run(self):
    """Run episodes."""
    episodesTS=10
    breadth = 10
    tree_depth = math.log(episodesTS,breadth)

    outer_rewards = []
    total_outer_reward = 0
    
    # Loop over all Episodes / Rounds 

    outer_score = [0] * 26

    for episode in range(self.flags['num_episodes']):
      # Outer loop over num_episodes
      total_inner_reward = 0
      inner_rewards = []
      inner_score_vec = [0]*26
      outer_episode_reward = 0

      # Inner loop for Tree Search
      for episodeTS in range(episodesTS):
        ### Begin Init Episodes / Rounds ###
        inner_score_vec = [0]*26

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
        ### End Init Episodes / Rounds ###
        # Play as long its not gameOver or Win
        round = 1
        inner_episode_reward = 0
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
                
            countt = 0 
            
            # Update Table
            if legal_move:
              for agent3 in agents: 
                agent3.update_tables(action)

            # Make an environment step.
            observations, inner_reward, done, unused_info = self.environment.step(action)

            inner_episode_reward += inner_reward
            
          round += 1
        inner_rewards.append(inner_episode_reward)
        total_inner_reward += inner_episode_reward
        inner_score_vec[inner_episode_reward]+= 1
#        print('Total inner Reward:  %d' % total_inner_reward)
#        print('Running inner episode: %d' % episodeTS)
#        print('Episode inner Reward:  %d' % inner_episode_reward)
      print('Max  inner Reward: %.3f' % max(inner_rewards))
#      print('Avg. inner Reward: %.3f' % (total_inner_reward/(episodeTS+1)))
      print('TREE-INFO-INNER----')
      print(inner_rewards)
      print('Running outer episode: %d' % episode)
      outer_episode_reward = func_MinMax(0,0,True,inner_rewards,tree_depth, breadth)
      print('Episode outer Reward:  %d' % outer_episode_reward)
      outer_rewards.append(outer_episode_reward)
      outer_score[outer_episode_reward]+= 1
      total_outer_reward += outer_episode_reward
    print('Max  outer Reward: %.3f' % max(outer_rewards))
    print('Avg. outer Reward: %.3f' % (total_outer_reward/(episode+1)))
    print('Total outer Reward:  %d' % total_outer_reward)
    print('Running outer episode: %d' % episode)
    print(outer_score)
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


if __name__ == "__main__":
 
  flags = {'players': 4, 'num_episodes': 30, 'agent_class': 'HTGSTreeAgent'}

  runner = Runner(flags)
  
  if runner.agent_class == HTGSTreeAgent: 
    runner.run()
  else: sys.exit('Wrong Agent Class!\n')

  