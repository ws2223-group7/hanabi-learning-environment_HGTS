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

from hanabi_learning_environment import rl_env
from hanabi_learning_environment.agents.random_agent import RandomAgent
from hanabi_learning_environment.agents.simple_agent import SimpleAgent
### g7_BEGINN ###
from hanabi_learning_environment.agents.hatrec_agent import HatRecAgent
from hanabi_learning_environment.agents.hatinfo_agent import HatInfoAgent
from hanabi_learning_environment.rl_env import Agent

AGENT_CLASSES = {'SimpleAgent': SimpleAgent, 
                 'RandomAgent': RandomAgent, 
### g7_BEGINN ###            
                 'HatRecAgent': HatRecAgent,
                 'HatInfoAgent': HatInfoAgent}
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
    rewards = []
    
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
      
      # done is bool for gameOver or Win
      done = False

      episode_reward = 0

      ### End Init Episodes / Rounds ###

      # Play as long its not gameOver or Win
      while not done:

        # Loop over all agents 
        for agent_id, agent in enumerate(agents):
          observation = observations['player_observations'][agent_id]
          action = agent.act(observation)
          if observation['current_player'] == agent_id:
            assert action is not None
            current_player_action = action
          else:
            assert action is None

        # Make an environment step.
        print('Agent: {} action: {}'.format(observation['current_player'],
                                            current_player_action))
        
        observations, reward, done, unused_info = self.environment.step(
            current_player_action)
        
        episode_reward += reward
      rewards.append(episode_reward)
      print('Running episode: %d' % episode)
      print('Max Reward: %.3f' % max(rewards))
    return rewards


if __name__ == "__main__":
### g7_BEGINN ###    
  flags = {'players': 5, 'num_episodes': 1, 'agent_class': 'HatRecAgent'}
#  flags = {'players': 5, 'num_episodes': 1, 'agent_class': 'HatInfoAgent'}
### g7_ENDE ###  
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
  if runner.agent_class == HatRecAgent: 
    runner.run()
  elif  runner.agent_class == HatInfoAgent:
    runner.run()
  else: sys.exit('Wrong Agent Class!\n')

