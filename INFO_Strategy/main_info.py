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
      print("\n\n\n------------------------------ New Episode -------------------------")
      while not done:

        # Loop over all agents 
        for agent_id, agent in enumerate(agents):

          # Update Observation 
          for agent_id2, agent2 in enumerate(agents):
            observation = observations['player_observations'][agent_id2]
            agent2.update_observation(observation)
            agent2.update_mc()

          action = agent.act()

          # Ausgabe des aktuellen Spiels vor Aktion:
          if output: self.env_out(datei,'V',agents,
                                  observations,episode,
                                  action,episode_reward)

          
          # Update Possibilty table auf Basis vom Hint
          if (action['action_type'] == 'REVEAL_COLOR' or 
              action['action_type'] == 'REVEAL_RANK'):

            for agent3 in agents: 
              agent3.update_tables(action)

          # Make an environment step.
          observations, reward, done, unused_info = self.environment.step(action)

          episode_reward += reward
          
          if output: self.env_out(datei,'N',agents,observations,
                                  episode,action,episode_reward)
      
      if output: datei.write('Running episode: {} Reward {}\n'.
                              format(episode, episode_reward))
          
      rewards.append(episode_reward)
      total_reward += episode_reward
      print("Total Reward ", total_reward)
      print('Running episode: %d' % episode)
      print('Max  Reward: %.3f' % max(rewards))
      print('Avg. Reward: {:%.3f}', total_reward/(episode+1))
      if output: datei.close()
    return rewards

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

  