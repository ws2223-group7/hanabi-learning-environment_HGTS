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