import numpy as np


def info(observations, agents, agent_id, action):
          
          cardknowledge_agent = [agents[0].observation['card_knowledge'][idx] for idx in range(len(agents))]
          num_tokens = agents[0].observation['information_tokens']  
          lifes = agents[0].observation['life_tokens']
          deck_size = agents[0].observation['deck_size']
          print("\n---------------------------------------------------------------------------------------------------------")
          print("\n---------------------------------------------------------------------------------------------------------")
          print("\nRound {}".format(round))
          print("Current Player {}".format(agent_id))
          
          print("\n Information Tokens {}".format(num_tokens))
          print("\n Life Tokens {}".format(lifes))
          print("\n Deck Size {}".format(deck_size))

          print("\nAction Player {}".format(agent_id))
          print(action)
          print("\nFirework")
          print(agents[0].observation['fireworks'])
          print("\nDiscard Pile")
          print(agents[0].observation['discard_pile'])
          print("\nCardknowledge")
          for idx in range (len(agents)):
              print(cardknowledge_agent[idx])  

          for player_idx in range(len(agents)):
            player_before = (player_idx - 1) if player_idx > 0 else len(agents)-1 
            player_hand = observations['player_observations'][player_before]\
                                      ['observed_hands'][1]
            current_player = observations['player_observations'][player_idx]\
                                         ['current_player_offset']
            
            

            print("---------------------------------------------------------------------------------------------------------")
            print("\n\nPlayer {}".format(player_idx))
            print("\n Player Hand")
            print(player_hand)
    


 
def round_results(total_reward, episode, episode_reward, rewards):
    print("\n------------------------------------")
    print("Runden Ergebnis")
    print(f"Total Reward {total_reward}")
    print(f"Running episode: {episode}")
    print(f"Episode Reward: {episode_reward}")
    print(f"Max  Reward: {max(rewards)}")
    print(f"Avg. Reward: {total_reward/(episode+1)}")

def overall_results(end_time, start_time, rewards, total_reward, episode):
    print("\n------------------------------------")
    print("Gesamt Ergebnis")
    print("Laufzeit pro Runde")
    print((end_time - start_time) / 100) 
    st_dev = np.std(rewards)
    print("Standardabweichung")
    print(st_dev)
    print("Durchschnitt")
    print(total_reward/(episode+1))

