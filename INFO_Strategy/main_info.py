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
import time
import numpy as np

from hanabi_learning_environment import rl_env
from hanabi_learning_environment.agents.random_agent import RandomAgent
from hanabi_learning_environment.agents.simple_agent import SimpleAgent



# Import Error
# from hanabi_learning_environment.agents.test_agent import HTGSAgent 
from htgs_info_agent import HTGSAgent



from hanabi_learning_environment.rl_env import Agent

AGENT_CLASSES = {'SimpleAgent': SimpleAgent, 
                 'RandomAgent': RandomAgent, 
### g7_BEGINN ###            
                 'HTGSAgent' : HTGSAgent}
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
    total_reward = 0

    output = False

    if output: datei = open('HAT_log.txt','w')
    
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
      if output: self.env_out(datei,'S',agents,observations,
                              0,None,episode_reward)
      

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
               
          #print(round)
          countt = 0 
          """
          print("\nLegal DISCARD Round {}".format(round))
          for move in agent.observation['legal_moves']:
            if move['action_type'] == 'DISCARD':
              print(move)
              countt += 1
          
          if (countt != len(agent.observation['observed_hands'][0])):
            print()
          """
          # Ausgabe des aktuellen Spiels vor Aktion:
          if output: self.env_out(datei,'V',agents,
                                  observations,episode,
                                  action,episode_reward)
          
          """
          print("\n---------------------------------------------------------------------------------------------------------")
          print("\n---------------------------------------------------------------------------------------------------------")
          print("\nRound {}".format(round))
          print("Current Player {}".format(agent_id))
          num_tokens = agents[0].observation['information_tokens']
          print("\n Information Tokens {}".format(num_tokens))
          print("\nAction Player {}".format(agent_id))
          print(action)
          print("\nFirework")
          print(agents[0].observation['fireworks'])
          print("\nDiscard Pile")
          print(agents[0].observation['discard_pile'])
          print("\n Mc")
          print(agents[0].mc)
          print("\nCardknowledge")
          cardknowledge_agent0 = agents[0].observation['card_knowledge'][0]
          cardknowledge_agent1 = agents[0].observation['card_knowledge'][1]
          cardknowledge_agent2 = agents[0].observation['card_knowledge'][2]
          cardknowledge_agent3 = agents[0].observation['card_knowledge'][3]
          cardknowledge_agent4 = agents[0].observation['card_knowledge'][4]
          print(cardknowledge_agent0)
          print(cardknowledge_agent1)
          print(cardknowledge_agent2)
          print(cardknowledge_agent3)
          print(cardknowledge_agent4)
          

          print("---------------------------------------------------------------------------------------------------------")
          print("\n\nPlayer 0")
          print("\n Player Hand")
          print(agents[4].observation['observed_hands'][1])
          target_card, target_idx = agents[0].get_target_card(0)
          print("\nTarget Index{}".format(target_idx))
          print("\nPoss Table Target Card")
          poss_table0 = agents[0].table[0][0]
          poss_table1 = agents[0].table[0][1]
          poss_table2 = agents[0].table[0][2]
          poss_table3 = agents[0].table[0][3]
          poss_tables = [poss_table0, poss_table1, poss_table2, poss_table3]
          print(poss_table0)
          print(poss_table1)
          print(poss_table2)
          print(poss_table3)
          print("\nPart Table Target Card")
          print(agents[0].table.get_part_table(agents[0].observation, poss_tables[target_idx]))
          print("\nOwn Hat")
          print(agents[4].cal_other_hat(1))

          print("-------------------------------------------------------------------------------------------------------------")

          print("\n\nPlayer 1")
          print("\n Player Hand")
          print(agents[0].observation['observed_hands'][1])
          print("\nTarget Index")
          target_card, target_idx = agents[1].get_target_card(0)
          print(target_idx)
          print("\nPoss Table Target Card")
          poss_table0 = agents[0].table[1][0]
          poss_table1 = agents[0].table[1][1]
          poss_table2 = agents[0].table[1][2]
          poss_table3 = agents[0].table[1][3]
          poss_tables = [poss_table0, poss_table1, poss_table2, poss_table3]
          print(poss_table0)
          print(poss_table1)
          print(poss_table2)
          print(poss_table3)
          print("\nPart Table Target Card")
          print(agents[0].table.get_part_table(agents[0].observation, poss_tables[target_idx]))
          print("\nOwn Hat {}".format(agents[0].cal_other_hat(1)))

          print("-------------------------------------------------------------------------------------------------------------")

          print("\n\nPlayer 2")
          print("\n Player Hand")
          print(agents[0].observation['observed_hands'][2])
          print("\nTarget Index")
          target_card, target_idx = agents[2].get_target_card(0)
          print(target_idx)
          print("\nPoss Table Target Card")
          poss_table0 = agents[0].table[2][0]
          poss_table1 = agents[0].table[2][1]
          poss_table2 = agents[0].table[2][2]
          poss_table3 = agents[0].table[2][3]
          poss_tables = [poss_table0, poss_table1, poss_table2, poss_table3]
          print(poss_table0)
          print(poss_table1)
          print(poss_table2)
          print(poss_table3)
          print("\nPart Table Target Card")
          print(agents[0].table.get_part_table(agents[0].observation, poss_tables[target_idx]))
          print("\nOwn Hat {}".format(agents[0].cal_other_hat(2)))

          print("-------------------------------------------------------------------------------------------------------------")

          print("\n\nPlayer 3")
          print("\n Player Hand")
          print(agents[0].observation['observed_hands'][3])
          print("\nTarget Index")
          target_card, target_idx = agents[3].get_target_card(0)
          print(target_idx)
          print("\nPoss Table Target Card")
          poss_table0 = agents[0].table[3][0]
          poss_table1 = agents[0].table[3][1]
          poss_table2 = agents[0].table[3][2]
          poss_table3 = agents[0].table[3][3]
          poss_tables = [poss_table0, poss_table1, poss_table2, poss_table3]
          print(poss_table0)
          print(poss_table1)
          print(poss_table2)
          print(poss_table3)
          print("\nPart Table Target Card")
          print(agents[0].table.get_part_table(agents[0].observation, poss_tables[target_idx]))
          print("\nOwn Hat {}".format(agents[0].cal_other_hat(3)))

          print("-------------------------------------------------------------------------------------------------------------")

          print("\n\nPlayer 4")
          print("\n Player Hand")
          print(agents[0].observation['observed_hands'][4])
          print("\nTarget Index")
          target_card, target_idx = agents[4].get_target_card(0)
          print(target_idx)
          print("\nPoss Table Target Card")
          poss_table0 = agents[0].table[4][0]
          poss_table1 = agents[0].table[4][1]
          poss_table2 = agents[0].table[4][2]
          poss_table3 = agents[0].table[4][3]
          poss_tables = [poss_table0, poss_table1, poss_table2, poss_table3]
          print(poss_table0)
          print(poss_table1)
          print(poss_table2)
          print(poss_table3)
          print("\nPart Table Target Card")
          print(agents[0].table.get_part_table(agents[0].observation, poss_tables[target_idx]))
          print("\nOwn Hat {}".format(agents[0].cal_other_hat(4)))
          """

          


          
          # Update Table
          if legal_move:
            for agent3_idx, agent3 in enumerate(agents): 
              agent3.update_tables(action)

          # Make an environment step.
          observations, reward, done, unused_info = self.environment.step(action)


          episode_reward += reward

          
          
          if output: self.env_out(datei,'N',agents,observations,
                                  episode,action,episode_reward)
        
        round += 1
      
      if output: datei.write('Running episode: {} Reward {}\n'.
                              format(episode, episode_reward))
        
          
      rewards.append(episode_reward)
      total_reward += episode_reward
      print("Total Reward ", total_reward)
      print('Running episode: %d' % episode)
      print('Episode Reward: %d' % episode_reward)
      print('Max  Reward: %.3f' % max(rewards))
      print('Avg. Reward: :%.3f', total_reward/(episode+1))

      

    end_time = time.time()
    print("Laufzeit pro Runde")
    print((end_time - start_time) / 100) 
    st_dev = np.std(rewards)
    print("Standardabweichung")
    print(st_dev)
    print("Durchschnitt")
    print(total_reward/(episode+1))
    return rewards
    
    if output: datei.close()


  def env_out(self,datei,st,agents, observations,e,action,reward):
      #e = flags['num_episodes']
      p = flags['players']
      if flags['agent_class'] == "HTGSAgent":
        c="HATG"

      l = self.environment.state.life_tokens()
      info = self.environment.state.information_tokens()

      d = observations['player_observations'][0]['deck_size']

      fd = observations['player_observations'][0]['fireworks']
      fl_k = list(fd.keys())
      fl_v = list(fd.values())

      f=""
      for i in range(len(fl_v)):
        hilf = fl_k[i]+(str)(fl_v[i])
        f+=hilf

      h=""
      cnt=0
      j=0

      cp = observations['player_observations'][0]['current_player']
      hdl = observations['player_observations'][cp]['observed_hands']
      for hd in hdl:
        for m in hd:
          if m['rank']!=-1:
            color = m['color']
            rank = m['rank']
            h+=(color+str(rank))
        if j>0 and j<p-1:
          h+='_'  
        j+=1

      ato=''
      if action != None:
        ac = action['action_type']
        if ac == 'REVEAL_RANK':
          at = action['rank']
          ato = action['target_offset']  
        if ac == 'REVEAL_COLOR': 
          at = action['color']
          ato = action['target_offset']  
        if ac == 'PLAY': 
          at = action['card_index']
        if ac == 'DISCARD': 
          at = action['card_index']
        datei.write('|{}|EP{:4d}|NP{:1d}|{:4s}|LT{}|IT{}|DS{:2d}|{}|REW{:2d}|CP{}|{}|ACT:{:12}|{:1}|{:1}|\n'.format(st,e,p,c,l,info,d,f,reward,cp,h,ac,at,ato))
      else:    
        datei.write('|{}|EP{:4d}|NP{:1d}|{:4s}|LT{}|IT{}|DS{:2d}|{}|REW{:2d}|CP{}|{}|\n'.format(st,e,p,c,l,info,d,f,reward,cp,h))
      return


if __name__ == "__main__":
 
  flags = {'players': 5, 'num_episodes': 100, 'agent_class': 'HTGSAgent'}

  runner = Runner(flags)
  
  if runner.agent_class == HTGSAgent: 
    runner.run()
  else: sys.exit('Wrong Agent Class!\n')

  