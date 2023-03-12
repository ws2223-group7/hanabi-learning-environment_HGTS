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
import os
import getopt

import numpy as np 
import time 

import numpy as np 
import time 

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment import rl_env


# from hanabi_learning_environment.agents.test_agent import HTGSAgent 
from Agents.htgs_agent import HTGSAgent

AGENT_CLASSES = {'HTGSAgent' : HTGSAgent}
       
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
    total_reward = 0

    output = False

    if output: datei = open('HAT_log.txt','w')
    
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
      
          
      # done is bool for gameOver or Win
      done = False

      episode_reward = 0
      if output: self.env_out(datei,'S',agents,observations,0,None,episode_reward)
      

      ### End Init Episodes / Rounds ###

      # Play as long its not gameOver or Win
      print("\n\n\n------------------------------ New Episode -------------------------")
      start_time = time.time() 
      start_time = time.time() 
      while not done:

        # Loop over all agents 
        for agent_id, agent in enumerate(agents):
          observation = observations['player_observations'][agent_id]
          action, legal_move = agent.act(observation)
          
          
          # If hint is given calculate the corresponding hat  
          if ((action['action_type'] == 'REVEAL_COLOR' 
             or action['action_type'] == 'REVEAL_RANK')
             and legal_move):
            
            self.decode_hint(observations, agents, agent_id, action)
             

          
          if (action['action_type'] == 'PLAY'):
            for agent3 in agents:
              agent3.nr_card_ply_since_hint += 1

          
          # Make an environment step.
          observations, reward, done, unused_info = self.environment.step(
              action)

          episode_reward += reward
          
          
      rewards.append(episode_reward)
      total_reward += episode_reward
      print("Total Reward ", total_reward)
      print('Running episode: %d' % episode)
      print('Max  Reward: %.3f' % max(rewards))
      print('Avg. Reward: ', format(total_reward/(episode+1),'.3f'))
      if output: datei.close()
    
    end_time = time.time()
    print("Laufzeit pro Runde")
    print((end_time - start_time) / 100) 
    st_dev = np.std(rewards)
    print("Standardabweichung")
    print(st_dev)
    print("Durchschnitt")
    print(total_reward/(episode+1))
    
    end_time = time.time()
    print("Laufzeit pro Runde")
    print((end_time - start_time) / 100) 
    st_dev = np.std(rewards)
    print("Standardabweichung")
    print(st_dev)
    print("Durchschnitt")
    print(total_reward/(episode+1))
    return rewards
    
  def decode_hint(self, observations, agents, agent_id, action):
    """Agent decode hint to recommanded action"""
    for agent_id2, agent2 in enumerate(agents):
      if agent_id == agent_id2:
        continue 

      # Setze Observation von Spielern die hint bekommen    
      agent2.observation = observations['player_observations'][agent_id2]
      agent2_hand = observations['player_observations'][agent_id2-1]['observed_hands'][1]
      agent2.decode_hint(action, agent2_hand)

def main():
  flags = {'players': 2, 'num_episodes': 10, 'agent_class': 'HTGSAgent'}
  runner = Runner(flags)

  runner.run()


if __name__ == "__main__":
  main()

  