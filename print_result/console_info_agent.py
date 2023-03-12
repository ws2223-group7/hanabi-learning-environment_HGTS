import numpy as np


def info(agents, agent_id, action):
          
          cardknowledge_agent = [agents[0].observation['card_knowledge'][idx] for idx in range(len(agents))]
          poss_table_players = [agents[idx_agent].table[0] for idx_agent in range(len(agents))]
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
          print("\n Mc")
          print(agents[0].mc)
          print("\nCardknowledge")
          for idx in range (len(agents)):
              print(cardknowledge_agent[idx])  

          for player_idx in range(len(agents)):
            player_before = (player_idx - 1) if player_idx > 0 else len(agents)-1 
            player_hand = agents[player_before].observation['observed_hands'][1]
            target_card, target_idx = agents[player_idx].get_target_card(0)  
            poss_table_player = poss_table_players[player_idx]
            part_table_target_card = agents[player_idx].table.get_part_table(
                agents[player_idx].observation, poss_table_player[target_idx])
            current_player = agents[player_idx].observation['current_player_offset']
            
            
            
            # Agent himself this own hat 
            if (current_player != 0 
               and action['action_type'] != 'DISCARD'
               and action['action_type'] != 'PLAY'):
              own_hat = agents[player_idx].cal_own_hat(action)       
            else:
                own_hat = None 

            # Other agents hat current agent
            own_hat_other_agents = agents[player_before].cal_hat_other_ply(1)


            print("---------------------------------------------------------------------------------------------------------")
            print("\n\nPlayer {}".format(player_idx))
            print("\n Player Hand")
            print(player_hand)
            print("\nTarget Index{}".format(target_idx))
            print("\nPoss Table Player")
            for card_idx in range(len(poss_table_player)):
                print(poss_table_player[card_idx])
    

            print("\nPart Table Target Card")
            print(part_table_target_card)

            if action['action_type'] == 'REVEAL_COLOR' or action['action_type'] == 'REVEAL_RANK':
                
              print("\nOwn Hat calculated by agent himslef")
              print(own_hat)

              print("\n Own Hat calulated by other agents")
              print(own_hat_other_agents)

              if own_hat != own_hat_other_agents and own_hat != None:
                  decode_hint_hat = agents[player_idx].decode_act_to_hat_sum(action)
                  hat_sum = agents[player_idx].cal_hat_sum_mod8()
                  hat_hinted_ply = agents[player_idx].cal_hat_player(current_player)
                  max_hat = (agents[player_idx].observation['num_players'] - 1) * 2
                  own_hat = (decode_hint_hat - 
                         (hat_sum - hat_hinted_ply)) % max_hat
                  raise Exception("Own Hat is not the same")

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


