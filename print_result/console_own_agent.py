import numpy as np

def info(agents, agent_id, action):
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
          print(cardknowledge_agent0)
          print(cardknowledge_agent1)
          print(cardknowledge_agent2)

          

          print("---------------------------------------------------------------------------------------------------------")
          print("\n\nPlayer 0")
          print("\n Player Hand")
          print(agents[2].observation['observed_hands'][1])
          target_card, target_idx = agents[0].get_target_card(0)
          print("\nTarget Index{}".format(target_idx))
          print("\nPoss Table Target Card")
          poss_table0 = agents[0].table[0][0]
          poss_table1 = agents[0].table[0][1]
          poss_table2 = agents[0].table[0][2]
          poss_table3 = agents[0].table[0][3]
          poss_table4 = agents[0].table[0][4]
          poss_tables = [poss_table0, poss_table1, poss_table2, poss_table3, poss_table4]
          print(poss_table0)
          print(poss_table1)
          print(poss_table2)
          print(poss_table3)
          print(poss_table4)
          print("\nPart Table Target Card")
          print(agents[0].table.get_part_table(agents[0].observation, poss_tables[target_idx]))
          
          own_hat_cal_other_ply = agents[2].cal_hat_other_ply(1)
          print("\nOwn Hat")
          print(own_hat_cal_other_ply)

          if action['action_type'] == 'REVEAL_COLOR' or action['action_type'] == 'REVEAL_RANK':  
            idx_hinting_player = agents[0].observation['current_player_offset']
            idx_hinted_player = (action['target_offset'] + idx_hinting_player) \
                                % agents[0].observation['num_players']

            if idx_hinted_player == 0:
              own_hat_cal_hinted_ply = agents[0].cal_hat_hinted_ply(action, 0)
              print("\nOwn Hat hinted Player {}".format(own_hat_cal_hinted_ply))  

              if own_hat_cal_other_ply[0] not in own_hat_cal_hinted_ply:
                  print("Own Hat hinted Player is wrong")

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
          poss_table4 = agents[0].table[1][4]
          poss_tables = [poss_table0, poss_table1, poss_table2, poss_table3, poss_table4]
          print(poss_table0)
          print(poss_table1)
          print(poss_table2)
          print(poss_table3)
          print(poss_table4)
          print("\nPart Table Target Card")
          print(agents[0].table.get_part_table(agents[0].observation, poss_tables[target_idx]))
          
          own_hat_cal_other_ply = agents[0].cal_hat_other_ply(1)
          print("\nOwn Hat {}".format(own_hat_cal_other_ply))


          if action['action_type'] == 'REVEAL_COLOR' or action['action_type'] == 'REVEAL_RANK':  
            idx_hinting_player = agents[1].observation['current_player_offset']
            idx_hinted_player = (action['target_offset'] + idx_hinting_player) \
                                % agents[1].observation['num_players']

            if idx_hinted_player == 0:
              own_hat_cal_hinted_ply = agents[0].cal_hat_hinted_ply(action, 1)
              print("\nOwn Hat hinted Player {}".format(
                  own_hat_cal_hinted_ply))

              if own_hat_cal_other_ply[0] not in own_hat_cal_hinted_ply:
                  print("Own Hat hinted Player is wrong")                   

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
          poss_table4 = agents[0].table[2][4]
          poss_tables = [poss_table0, poss_table1, poss_table2, poss_table3, poss_table4]
          print(poss_table0)
          print(poss_table1)
          print(poss_table2)
          print(poss_table3)
          print(poss_table4)
          print("\nPart Table Target Card")
          print(agents[0].table.get_part_table(agents[0].observation, poss_tables[target_idx]))
          
          own_hat_cal_other_ply = agents[0].cal_hat_other_ply(2)
          print("\nOwn Hat {}".format(own_hat_cal_other_ply))

          if action['action_type'] == 'REVEAL_COLOR' or action['action_type'] == 'REVEAL_RANK':
            idx_hinting_player = agents[2].observation['current_player_offset']
            idx_hinted_player = (action['target_offset'] + idx_hinting_player) \
                                % agents[2].observation['num_players']

            if idx_hinted_player == 0:
                    own_hat_cal_hinted_ply = agents[0].cal_hat_hinted_ply(action, 2)
                    print("\nOwn Hat hinted Player {}".format(own_hat_cal_hinted_ply))   

                    if own_hat_cal_other_ply[0] not in own_hat_cal_hinted_ply:
                      print("cal_hat_hinted_ply falsch berechnet")

          print("-------------------------------------------------------------------------------------------------------------")


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