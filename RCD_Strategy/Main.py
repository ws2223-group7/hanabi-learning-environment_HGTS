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

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment import rl_env
from hanabi_learning_environment.agents.random_agent import RandomAgent
from hanabi_learning_environment.agents.simple_agent import SimpleAgent

# from hanabi_learning_environment.agents.test_agent import HTGSAgent 
from RCD_Strategy.htgs_agent import HTGSAgent

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

  def env_out(self,datei,st,agents, observations,e,action,reward):
      #e = flags['num_episodes']
      p = self.flags['players']
      if self.flags['agent_class'] == "HTGSAgent":
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
      while not done:

        # Loop over all agents 
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

          #Ausgabe des aktuellen Spiels vor Aktion:
          if output: self.env_out(datei,'V',agents,observations,episode,action,episode_reward)
          
          # If hint is given calculate the corresponding hat  
          if (action['action_type'] == 'REVEAL_COLOR' 
             or action['action_type'] == 'REVEAL_RANK'):
             
             for agent_id2, agent2 in enumerate(agents):
              if agent_id == agent_id2:
                continue 

              # Setze Observation von Spielern die hint bekommen    
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

          
          # Make an environment step.
          
          observations, reward, done, unused_info = self.environment.step(
              current_player_action)

          episode_reward += reward
          
          if output: self.env_out(datei,'N',agents,observations,episode,current_player_action,episode_reward)
      if output: datei.write('Running episode: {} Reward {}\n'.format(episode, episode_reward))
          
      rewards.append(episode_reward)
      total_reward += episode_reward
      print("Total Reward ", total_reward)
      print('Running episode: %d' % episode)
      print('Max  Reward: %.3f' % max(rewards))
      print('Avg. Reward: ', format(total_reward/(episode+1),'.3f'))
      if output: datei.close()
    return rewards

def main():
  flags = {'players': 2, 'num_episodes': 10, 'agent_class': 'HTGSAgent'}

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
  if runner.agent_class == HTGSAgent: 
    runner.run()
  else: sys.exit('Wrong Agent Class!\n')

if __name__ == "__main__":
  main()

  