import copy
import os
import sys

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from INFO_Strategy.possibility_table import Table
from hanabi_learning_environment.rl_env import Agent
from INFO_Strategy.color_enum import Color


class HTGSAgentOwn(Agent):
    def __init__(self, config, *args, **kwargs):
        self.config = config

        self.max_rank = 4
        self.mc = self.init_mc()
        self.observation = None
        self.table = None

        self.colors = ['B', 'G', 'R', 'W', 'Y']

        # Get Hat to recomm
        self.encode_act_to_hat = {0: {'action_type': 'PLAY', 'card_index': 0},
                                  1: {'action_type': 'PLAY', 'card_index': 1},
                                  2: {'action_type': 'PLAY', 'card_index': 2},
                                  3: {'action_type': 'PLAY', 'card_index': 3},
                                  4: {'action_type': 'DISCARD', 'card_index': 0},
                                  5: {'action_type': 'DISCARD', 'card_index': 1},
                                  6: {'action_type': 'DISCARD', 'card_index': 2},
                                  7: {'action_type': 'DISCARD', 'card_index': 3}}

        self.num_colors_left = {'B':  10, 'G': 10, 'R': 10, 'W': 10, 'Y': 10}

        self.num_ranks_left = {0:  15, 1: 10, 2: 10, 3: 10, 4: 5}

        self.color_order = {'R': 0, 'G': 1, 'Y': 2, 'W': 3, 'B': 4}

    def init_table(self, observation):
        self.table = Table(observation)

    def init_mc(self):
        rep_color = [3, 2, 2, 2, 1]

        mc = {'B': rep_color.copy(),
              'G': rep_color.copy(),
              'R': rep_color.copy(),
              'W': rep_color.copy(),
              'Y': rep_color.copy(), }

        return mc

    def act(self):
        """Return action"""
        poss_hand_table = self.table.get_poss_table_hand(0)
        private_poss_hand_table = self.get_privat_poss_hand_table(
            poss_hand_table)

        dead_card_idx = self.dead_card_in_hand(private_poss_hand_table)
        playable_card_idx = self.playable_card_in_hand(private_poss_hand_table)
        duplicate_card_idx = self.duplicate_card_in_hand(
            private_poss_hand_table)
        dispensable_card_idx = self.dispensable_card_in_hand(
            private_poss_hand_table)
        
        # Rule 1.
        if (playable_card_idx is not None):
            act = {'action_type': 'PLAY', 'card_index': playable_card_idx}

        # Rule 2.
        # In the first round it is not allowed to discard (why i dont know)
        elif (len(self.observation['discard_pile']) < 5
            and dead_card_idx is not None
                and round != 1):
            act = {'action_type': 'DISCARD', 'card_index': dead_card_idx}

        # Rule 3.
        elif (self.observation['information_tokens'] > 0):
            act = self.give_hint()
            if act['action_type'] == 'DISCARD' and self.observation['information_tokens'] > 0:
                print("Error")

        # Rule 4.
        elif (dead_card_idx is not None):
            act = {'action_type': 'DISCARD', 'card_index': dead_card_idx}

        # Rule 5.
        elif (duplicate_card_idx is not None):
            act = {'action_type': 'DISCARD', 'card_index': duplicate_card_idx}

        # Rule 6.
        elif (dispensable_card_idx is not None):
            act = {'action_type': 'DISCARD',
                   'card_index': dispensable_card_idx}

        # Rule 7
        else:
            act = {'action_type': 'DISCARD', 'card_index': 0}
        
        action, legal_move = self.filter_illigal_action(act)
    
        return action, legal_move

    def filter_illigal_action(self, action):
        """Filters illegal actions. Sometimes it is not allowed
        to discard a card"""
        legal_move = True
        if (action not in self.observation['legal_moves']):
            legal_move = False
            found = False
            for act_idx, act in enumerate (self.observation['legal_moves']): 
                if act['action_type'] == 'REVEAL_COLOR' or act['action_type'] == 'REVEAL_RANK':
                    action = self.observation['legal_moves'][act_idx]
                    found = True 

            if found == False:
                action = self.observation['legal_moves'][act_idx] 
                legal_move = False   
            
        return action, legal_move

    def get_privat_poss_hand_table(self, poss_hand_table):
        """Return privat_hand_table"""
        private_poss_hand_table = []
        for poss_card_table in poss_hand_table:
            private_poss_card_table = self.get_private_poss_card_table(
                poss_card_table)
            private_poss_hand_table.append(private_poss_card_table)

        return private_poss_hand_table

    def playable_card_in_hand(self, privat_poss_hand_table):
        """ Return Index der ersten spielbaren Karte
        wenn keine Karte spielbare return None"""

        for card_idx, privat_poss_card_table in enumerate(privat_poss_hand_table):
            if (self.playable_card_in_card_table(privat_poss_card_table)):
                return card_idx

        return None

    def playable_card_in_card_table(self, privat_poss_card_table):
        """Return True if all poss cards in card_table are 
        playable, else true false"""

        for color in self.colors:
            for rank in range(self.max_rank + 1):
                if privat_poss_card_table[color][rank] == 1:
                    card = {'color': color, 'rank': rank}
                    if self.playable_card(card) == False:
                        return False

        return True

    def get_private_poss_card_table(self, poss_card_table):
        """Return private poss card table
        This Table takes into accounts the private knowledge and
        exclude all cards that are not possible based on private knowledge"""

        number_colors_left_private, number_ranks_left_private = self.get_privat_num_colors_ranks_left()

        private_poss_card_table = copy.deepcopy(poss_card_table)

        for color in self.colors:
            for rank in range(self.max_rank + 1):
                if poss_card_table[color][rank] == 1:
                    card = {'color': color, 'rank': rank}

                    if (self.poss_card_in_hand(card, number_colors_left_private,
                                               number_ranks_left_private) is False):
                        private_poss_card_table[color][rank] = 0

        return private_poss_card_table

    def get_privat_num_colors_ranks_left(self):
        """Return private num colors """
        number_colors_left_private = {
            'B': self.num_colors_left['B'],
            'G': self.num_colors_left['G'],
            'R': self.num_colors_left['R'],
            'W': self.num_colors_left['W'],
            'Y': self.num_colors_left['Y'],
        }

        number_ranks_left_private = {
            0: self.num_ranks_left[0],
            1: self.num_ranks_left[1],
            2: self.num_ranks_left[2],
            3: self.num_ranks_left[3],
            4: self.num_ranks_left[4]
        }

        for agent_idx, agent_hand in enumerate(self.observation['observed_hands']):
            if agent_idx == 0:
                continue

            for card_idx, card in enumerate(agent_hand):
                card_in_cardknowledge = self.observation['card_knowledge'][agent_idx][card_idx]
                card_cardknowledge_color = card_in_cardknowledge['color']
                card_cardknowledge_rank = card_in_cardknowledge['rank']

                if (card_cardknowledge_color == None):
                    number_colors_left_private[card['color']] -= 1

                if (card_cardknowledge_rank == None):
                    number_ranks_left_private[card['rank']] -= 1

        return number_colors_left_private, number_ranks_left_private

    def poss_card_in_hand(self, card, number_colors_left_private, number_ranks_left_private):

        card_color = card['color']
        card_rank = card['rank']

        if (number_ranks_left_private[card_rank] == 0 or
                number_colors_left_private[card_color] == 0):
            return False

        else:
            return True

    def playable_card(self, card) -> bool:
        """Return True wenn Karte spielbar sonst False"""

        fireworks = self.observation['fireworks']
        return card['rank'] == fireworks[card['color']]

    def dead_card_in_hand(self, privat_poss_hand_table) -> int:
        """ Return index der ersten dead Kart
        wenn keine dead Kart vorhanden return None"""

        for card_idx, privat_card_table in enumerate(privat_poss_hand_table):
            if (self.dead_card_in_poss_card_table(privat_card_table)):
                return card_idx

        return None

    def dead_card_in_poss_card_table(self, privat_poss_card_table):
        """Return True if all possible cards are dead cards
        else False"""

        for color in self.colors:
            for rank in range(self.max_rank + 1):
                if privat_poss_card_table[color][rank] == 1:
                    card = {'color': color, 'rank': rank}
                    if self.dead_card(card) == False:
                        return False

        return True

    def dead_card(self, card):
        """Return True if card is dead, else False """
        firework = self.observation['fireworks']
        if (card['rank'] < firework[card['color']]):
            return True

        # Max Karten pro Rank die abgeworfen sein dürfen
        max_card_per_rank = [3, 2, 2, 2]

        cards_in_dsc_pile = [0, 0, 0, 0]

        for card_dsc_pile in self.observation['discard_pile']:
            # Prüfe alle Karten im dsc_pile mit der selben Farbe und
            # einem geringen Rank
            if (card_dsc_pile['color'] == card['color']
                    and card_dsc_pile['rank'] < card['rank']):

                cards_in_dsc_pile[card_dsc_pile['rank']] += 1

        # Wenn alle Karten eines rankes einer Farbe abgewurfen worden
        # dann return True (Karte ist ToT)
        for idx, elem in enumerate(cards_in_dsc_pile):
            if elem >= max_card_per_rank[idx]:
                return True

        return False

    def give_hint(self):
        act_hint = self.encode_hint()

        return act_hint

    def encode_hint(self):
        hatSumMod8 = self.cal_hat_sum_mod8()

        # if hatSumMod8 < 4 give hint rank (See Paper Cox)
        if (hatSumMod8 < 4):
            hint = self.get_hint_hat_sum_smaller_4(hatSumMod8)
            return hint

        # if hatSumMod8 > 3 give hint color (See Paper Cox)
        else:
            hint = self.get_hint_hat_sum_bigger_3(hatSumMod8)
            return hint

    def cal_hat_sum_mod8(self):
        """Returns the sum of hats from all other player mod 8"""
        hat_sum_player = 0
        max_hat = (self.observation['num_players'] - 1) * 8

        for agent_idx in range(1, self.observation['num_players']):
            hat_player = self.cal_hat_player(agent_idx)

            # hat_player should always just conatain one element,
            # because it should calculate the hat based on hands which can be observed
            # and not the own hand
            if len(hat_player) != 1:
                raise Exception("Hat should only contain one element")

            hat_sum_player += hat_player[0]

        hat_sum_mod = hat_sum_player % max_hat

        return hat_sum_mod

    def cal_hat_player(self, agent_idx, act=None):
        """Return hat vom Spieler mit Index agent_idx

        Parameter
            action(dict): Wenn der eigene Hat berechnet werden soll
                          muss die Action mit übergeben werden.
                          Hierbei muss es sich natürlich um ein Hint handeln 
        """
        # Sonderfall wenn der eigene Hat berechnet werden soll
        # ! Hierfür muss der Hint übergeben werden
        if agent_idx == 0:
            return self.cal_own_hat(act)

        return self.cal_hat_other_ply(agent_idx)

    def decode_hint(self, act, idx_hinted_player, for_hinted_player):
        """Return hat vom Spieler der gehintet wird
           Der gehinted Spieler kennt seine Karten nicht
           und kann somit den hint nur bedingt interpretieren
           Damit alle den possibilty table gleich updaten muss 
           jeder den selben hut bzw. die selben möglichen Hüte 
           für den hinted player berechnen"""

        if for_hinted_player == True:
            card_knowledge_hinted_ply = self.observation['card_knowledge'][idx_hinted_player]

        else:
            card_knowledge_hinted_ply = self.observation['observed_hands'][idx_hinted_player]

        # Calculate highst and lowest color in hand
        highest_rank = self.highest_rank_in_hand(card_knowledge_hinted_ply)
        sec_lowest_rank = self.sec_lowest_rank_in_hand(
            card_knowledge_hinted_ply)
        lowest_rank = self.lowest_rank_in_hand(card_knowledge_hinted_ply)
        sec_highest_rank = self.sec_highest_rank_in_hand(
            card_knowledge_hinted_ply)

        highst_color = self.highest_color_in_hand(card_knowledge_hinted_ply)
        highst_color_value = Color[highst_color].value \
            if highst_color else None

        sec_highst_color = self.sec_highest_color_in_hand(
            card_knowledge_hinted_ply)
        sec_highst_color_value = Color[sec_highst_color].value \
            if sec_highst_color else None

        lowest_color = self.lowest_color_in_hand(card_knowledge_hinted_ply)
        lowest_color_value = Color[lowest_color].value \
            if lowest_color else None

        sec_lowest_color = self.sec_lowest_color_in_hand(
            card_knowledge_hinted_ply)
        sec_lowest_color_value = Color[sec_lowest_color].value \
            if sec_lowest_color else None

        unknown_rank = self.unknown_rank_in_hand(card_knowledge_hinted_ply)
        unknown_color = self.unknown_color_in_hand(card_knowledge_hinted_ply)

        # Wenn der Hint eine Farbe ist
        if act['action_type'] == 'REVEAL_COLOR':
            hat_ply = self.decode_hat_hint_color(act, unknown_color,
                                                 highest_rank, lowest_rank,
                                                 highst_color_value, sec_highst_color_value,
                                                 lowest_color_value, sec_lowest_color_value)

        elif act['action_type'] == 'REVEAL_RANK':
            hat_ply = self.decode_hint_rank(act, unknown_rank, 
                                                 highest_rank, sec_highest_rank,
                                                 lowest_rank, sec_lowest_rank,
                                                 highst_color_value, lowest_color_value)

        else:
            raise ValueError(
                'act[action_type] is not REVEAL_COLOR or REVEAL_RANK')

        return hat_ply

    def decode_hint_rank(self, act, 
                              unknown_rank, 
                              highst_rank, sec_highst_rank,
                              lowest_rank, sec_lowest_rank,
                              highest_color_value, lowest_color_value):
        """Return hat vom hinted player wenn es sich um einen Rank Hint handelt"""

        hinted_rank = act['rank']

        # Wenn höchste Karte != niedrigste Karte dann ist es mit Sicherheit ein Rank Hint
        # und kein speziel Fall von einen Color Hint
        if highest_color_value != lowest_color_value:
            hat = self.decode_hat_rank_no_special_case(act,
                                                       hinted_rank,
                                                       highst_rank, lowest_rank)

        # Wenn höchste Karte == niedrigste Karte ist, dann kann es sich auch
        # um einen speziellen Fall von einem Rank Hint handeln
        else:
            # Wenn mindestens ein Rank auf der Hand bekannt ist
            if highst_rank != None and lowest_rank != None:
                hat = self.decode_hint_rank_special_case_I(act, unknown_rank, 
                                                           hinted_rank, 
                                                           highst_rank, sec_highst_rank,
                                                           lowest_rank, sec_lowest_rank)

            # Wenn kein Rank auf der Hand bekannt ist
            # kann der speziellen Fall von Hint Color nicht ausgeschlossen werden
            # es kann auch nicht auf high Color hint oder low Color hint geschlossen werden
            elif highst_rank == None and lowest_rank == None:
                if act['target_offset'] == 1:
                    hat = [0, 1, 4, 5]
                elif act['target_offset'] == 2:
                    hat = [2, 3, 6, 7]
                else:
                    # target off set muss 1 oder 2 sein
                    raise Exception("target offset must be 1 or 2")

            else:
                raise Exception("This case should never happen")

        return hat

    def decode_hat_rank_no_special_case(self, act,
                                        hinted_rank,
                                        highst_rank, lowest_rank):
        """Return hat vom hinted player wenn es sich um einen Rank Hint handelt
           und es sich nicht um einen speziellen Fall handelt"""

        # Wenn keine Rank auf der Hand bekannt ist
        # sich um einen highst oder lowest rank hint handelt
        if highst_rank == None and lowest_rank == None:
            if act['target_offset'] == 1:
                hat = [0, 1]
            elif act['target_offset'] == 2:
                hat = [2, 3]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Wenn es ein Rank auf der Hand gibt die einen höheren Wert
        # Dann handelt es sich um einen Rank Hint für den niedriegsten Rank
        elif highst_rank > hinted_rank:
            if act['target_offset'] == 1:
                hat = [1]
            elif act['target_offset'] == 2:
                hat = [3]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Wenn es eine Rank auf der Hand gibt die einen niedrigeren Wert hat
        # Dann handelt es sich um einen Rank Hint für den höchsten Rank
        elif lowest_rank < hinted_rank:
            if act['target_offset'] == 1:
                hat = [0]
            elif act['target_offset'] == 2:
                hat = [2]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Wenn eine Karte bekannt ist aber es sich um eine höchsten Rank
        # oder niedrigsten color hint handel kann
        elif (highst_rank == hinted_rank and
                lowest_rank == highst_rank):
            if act['target_offset'] == 1:
                hat = [0, 1]
            elif act['target_offset'] == 2:
                hat = [2, 3]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Dieser Fall sollte eigentlich nie auftreten
        else:
            raise Exception("This case should never happen")

        return hat

    def decode_hint_rank_special_case_I(self, act, unknown_rank, 
                                        hinted_rank, 
                                        highest_rank, sec_highest_rank,
                                        lowest_rank, sec_lowest_rank):
        """ Return hat vom hinted player hat wenn es sich um einen Rank Hint handelt
            und es sich um einen speziellen Fall von einem Rank Hint handel könnte, 
            also highst_color == lowest_color"""

        # Eindeutig High Rank Hint
        if (highest_rank != sec_highest_rank
            and highest_rank == hinted_rank
            and (unknown_rank == False or highest_rank == 5)):

            if act['target_offset'] == 1:
                hat = [0]
            elif act['target_offset'] == 2:
                hat = [2]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Eindeutiger Low Rank Hint
        elif (lowest_rank != sec_lowest_rank
              and lowest_rank == hinted_rank
              and (unknown_rank == False or lowest_rank == 0)):
            if act['target_offset'] == 1:
                hat = [1]
            elif act['target_offset'] == 2:
                hat = [3]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Eindeutiger low Color Hint
        elif (lowest_rank != sec_lowest_rank
              and sec_lowest_rank != sec_highest_rank
              and sec_lowest_rank != highest_rank
              and hinted_rank == sec_lowest_rank):

            if act['target_offset'] == 1:
                hat = [5]

            elif act['target_offset'] == 2:
                hat = [7]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Eindeutiger highest color hint
        elif (highest_rank != sec_highest_rank
              and sec_lowest_rank != sec_highest_rank
              and sec_highest_rank != lowest_rank
              and hinted_rank == sec_highest_rank):

            if act['target_offset'] == 1:
                hat = [4]

            elif act['target_offset'] == 2:
                hat = [6]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Eindeutiger Spezial Fall aber unklar welcher
        elif (hinted_rank != highest_rank
              and hinted_rank != lowest_rank
              and sec_highest_rank != highest_rank
              and sec_highest_rank != lowest_rank
              and sec_lowest_rank != highest_rank
              and sec_lowest_rank != lowest_rank):

            if act['target_offset'] == 1:
                hat = [4, 5]

            elif act['target_offset'] == 2:
                hat = [6, 7]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Eindeutig High Rank Hint oder high Color Hint
        elif (hinted_rank == highest_rank
                and sec_highest_rank == highest_rank
                and sec_lowest_rank != highest_rank
                and lowest_rank != highest_rank):

            if act['target_offset'] == 1:
                hat = [0, 4]

            elif act['target_offset'] == 2:
                hat = [2, 6]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Eindeutig Low Rank Hint oder low Color Hint
        elif (hinted_rank == lowest_rank
                and sec_lowest_rank == lowest_rank
                and sec_highest_rank != lowest_rank
                and highest_rank != lowest_rank):

            if act['target_offset'] == 1:
                hat = [1, 5]

            elif act['target_offset'] == 2:
                hat = [3, 7]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Keinen high rank hint
        elif (hinted_rank < highest_rank):

            if act['target_offset'] == 1:
                hat = [1, 4, 5]

            elif act['target_offset'] == 2:
                hat = [3, 6, 7]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Kein low rank hint
        elif (hinted_rank > lowest_rank):

            if act['target_offset'] == 1:
                hat = [0, 4, 5]

            elif act['target_offset'] == 2:
                hat = [2, 6, 7]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Keine Information kann alles sein
        elif (highest_rank == sec_highest_rank == sec_lowest_rank == lowest_rank):
            if act['target_offset'] == 1:
                hat = [0, 1, 4, 5]
            elif act['target_offset'] == 2:
                hat = [2, 3, 6, 7]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Wenn die niedrigste Farbe gleich der zweithöchsten Farbe ist
        # ! Dieser Fall kann nur eintreten wenn alle Karten die gleiche Farbe haben
        # da der höchste rank aber auch der niedrigste rank ist kann der Fall nicht eintreten
        elif (sec_lowest_rank == sec_highest_rank):
            raise Exception("This case should never happen")

        else:
            raise Exception("This case should never happen")

        return hat

    def decode_hint_rank_special_case_I_I(self, act,
                                          highest_rank, sec_highest_rank,
                                          lowest_rank, sec_lowest_rank,
                                          hinted_rank):
        """Return hat vom hinted player hat wenn es sich um einen Color Hint handelt
        und es sich um einen speziellen Fall von einem Rank Hint handel könnte,
        und sec_lowest_card != sec_highest_card"""

        # Wenn die niedrigste Farbe nicht die zweitniedrigste Rank ist
        # und die zweitniedrigste Rank nicht die niedrigste Rank ist
        # und der hint die zweitniedrigste Rank ist dann handelt es sich
        # um den spezieller Fall Rank Hint lowest rank
        if (sec_lowest_rank != sec_highest_rank
            and sec_lowest_rank != lowest_rank
                and sec_lowest_rank == hinted_rank):

            if act['target_offset'] == 1:
                return [5]

            elif act['target_offset'] == 2:
                return [7]

        # Wenn die höchste Rank nicht zweithöchste Rank ist
        # und die zweitniedrigste Rank nicht die zweithöchste Rank ist
        # und die zweithöchste Rank gehinted wurde
        # dann handelt es sich um den spezieller Fall Rank Hint highest rank
        elif (sec_lowest_rank != sec_highest_rank
              and sec_highest_rank != highest_rank
              and sec_highest_rank == hinted_rank):

            if act['target_offset'] == 1:
                return [4]

            elif act['target_offset'] == 2:
                return [6]

        # Wenn die höchste Rank nicht zweithöchste Rank ist
        # und die niedrigste Rank nicht zweitniedrigste Rank ist
        # aber die zweitniedrigste Rank nicht die zweithöchste Rank ist
        # und die zweitniedrigste / zweithöchste Rank gehinted wurde
        # dann handelt es sich um den spezieller Fall von Rank Hint
        # man weiß aber nicht welcher
        elif (highest_rank != sec_highest_rank
              and lowest_rank != sec_lowest_rank
              and sec_lowest_rank != sec_highest_rank
              and (sec_lowest_rank == hinted_rank
                   or sec_highest_rank == hinted_rank)):

            if act['target_offset'] == 1:
                return [4, 5]

            elif act['target_offset'] == 2:
                return [6, 7]

        else:
            raise Exception("This case should never happen")

    def decode_hat_hint_color(self, act,
            unknown_color,                  
            highst_rank, lowest_rank,
            highst_color_value,  sec_highst_color_value,
            lowest_color_value, sec_lowest_color_value):
        """Return hat vom hinted player wenn es sich um einen Color Hint handelt"""

        hinted_color_value = Color[act['color']].value

        # Wenn höchste Karte != niedrigste Karte dann ist es mit Sicherheit ein Color Hint
        # und kein speziel Fall von einen Rank Hint
        if highst_rank != lowest_rank:
            hat = self.decode_hint_color_no_special_case(act,
                                                         hinted_color_value,
                                                         highst_color_value, lowest_color_value)

        # Wenn höchste Karte == niedrigste Karte ist, dann kann es sich auch
        # um einen speziellen Fall von einem Rank Hint handeln
        else:

            # Wenn mindestens eine Farbe auf der Hand bekannt ist
            if highst_color_value != None and lowest_color_value != None:
                hat = self.decode_hint_color_special_case_I(act,
                                                            unknown_color,
                                                            hinted_color_value,
                                                            highst_color_value, sec_highst_color_value,
                                                            lowest_color_value, sec_lowest_color_value)

            # Wenn keine Farbe auf der Hand bekannt ist
            # kann der speziellen Fall von Rank Hint nicht ausgeschlossen werden
            # es kann auch nicht auf high Color hint oder low Color hint geschlossen werden
            elif highst_color_value == None and lowest_color_value == None:
                if act['target_offset'] == 1:
                    hat = [0, 1, 4, 5]
                elif act['target_offset'] == 2:
                    hat = [2, 3, 6, 7]
                else:
                    # target off set muss 1 oder 2 sein
                    raise Exception("target offset must be 1 or 2")

            else:
                raise Exception("This case should never happen")

        return hat

    def decode_hint_color_no_special_case(self, act,
                                          hinted_color_value, highst_color_value,
                                          lowest_color_value):
        """Return hat vom hinted player hat wenn es sich um einen Color Hint handelt
        und es sich nicht um einen speziellen Fall von einem Rank Hint handelt"""
        # Wenn keine Farbe auf der Hand bekannt ist
        # sich um einen highst oder lowest color hint handelt
        if highst_color_value == None and lowest_color_value == None:
            if act['target_offset'] == 1:
                hat = [4, 5]
            elif act['target_offset'] == 2:
                hat = [6, 7]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Wenn es eine Farbe auf der Hand gibt die einen höheren Wert
        # Dann handelt es sich um einen Color Hint für den niedriegsten Rank
        elif highst_color_value > hinted_color_value:
            if act['target_offset'] == 1:
                hat = [5]
            elif act['target_offset'] == 2:
                hat = [7]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Wenn es eine Farbe auf der Hand gibt die einen niedrigeren Wert hat
        # Dann handelt es sich um einen Color Hint für den höchsten Rank
        elif lowest_color_value < hinted_color_value:
            if act['target_offset'] == 1:
                hat = [4]
            elif act['target_offset'] == 2:
                hat = [6]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Wenn eine Karte bekannt ist aber es sich um eine höchsten color
        # oder niedrigsten color hint handel kann
        elif (highst_color_value == hinted_color_value and
                lowest_color_value == hinted_color_value):
            if act['target_offset'] == 1:
                hat = [4, 5]
            elif act['target_offset'] == 2:
                hat = [6, 7]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Dieser Fall sollte eigentlich nie auftreten
        else:
            raise Exception("This case should never happen")

        return hat

    def decode_hint_color_special_case_I(self, act,
                                         unknown_color,
                                         hinted_color_value,
                                         highest_color_value, sec_highest_color_value,
                                         lowest_color_value, sec_lowest_color_value):
        """Return hat vom hinted player hat wenn es sich um einen Color Hint handelt
          und es sich um einen speziellen Fall von einem Rank Hint handel könnte, 
          also highst_rank == lowst_rank"""

        # Eindeutig highst color hint
        if (highest_color_value != sec_highest_color_value
                and highest_color_value == hinted_color_value
                and (unknown_color == False or highest_color_value == 5)):
            if act['target_offset'] == 1:
                hat = [4]
            elif act['target_offset'] == 2:
                hat = [6]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # Eindeutig lowest color hint
        elif (lowest_color_value != sec_lowest_color_value
              and lowest_color_value == hinted_color_value
              and (unknown_color == False or lowest_color_value == 1)): 
            if act['target_offset'] == 1:
                hat = [5]
            elif act['target_offset'] == 2:
                hat = [7]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")

        # High Rank Hint 
        elif (highest_color_value != sec_highest_color_value
              and sec_lowest_color_value != sec_highest_color_value
              and lowest_color_value != sec_highest_color_value
              and hinted_color_value == sec_highest_color_value):

            if act['target_offset'] == 1:
                hat = [0]

            elif act['target_offset'] == 2:
                hat = [2]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")
                
        # Eindeutiger low Rank Hint
        elif (lowest_color_value != sec_lowest_color_value
              and sec_highest_color_value != sec_lowest_color_value
              and highest_color_value != sec_lowest_color_value
              and hinted_color_value == sec_lowest_color_value):

            if act['target_offset'] == 1:
                hat = [1]

            elif act['target_offset'] == 2:
                hat = [3]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")
        
        # Eindeutig Speziel Fall von Rank Hint
        elif (hinted_color_value != highest_color_value
              and hinted_color_value != lowest_color_value
              and sec_highest_color_value != highest_color_value
              and sec_highest_color_value != lowest_color_value
              and sec_lowest_color_value != highest_color_value
              and sec_lowest_color_value != lowest_color_value):
            
            if act['target_offset'] == 1:
                hat = [0, 1]
            
            elif act['target_offset'] == 2:
                hat = [2, 3]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")
            
        # Eindeutig High Color Hint oder High Rank Hint
        elif (hinted_color_value == highest_color_value
              and sec_highest_color_value == highest_color_value
              and sec_lowest_color_value != highest_color_value
              and lowest_color_value != highest_color_value):
            
            if act['target_offset'] == 1:
                hat = [0, 4]
            
            elif act['target_offset'] == 2:
                hat = [2, 6]
            
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")
        
        # Eindeutig Low Color Hint oder Low Rank Hint
        elif (hinted_color_value == lowest_color_value
                and sec_lowest_color_value == lowest_color_value
                and sec_highest_color_value != lowest_color_value
                and highest_color_value != lowest_color_value):
            
            if act['target_offset'] == 1:
                hat = [1, 5]

            elif act['target_offset'] == 2:
                hat = [3, 7]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")
            
        # Kein high color hint 
        elif(hinted_color_value < highest_color_value):

            if act['target_offset'] == 1:
                hat = [0, 1, 5]
            
            elif act['target_offset'] == 2:
                hat = [2, 3, 7]
            
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")
            
        # Kein low color hint
        elif (hinted_color_value > lowest_color_value):
            
            if act['target_offset'] == 1:
                hat = [0, 4, 5]
            
            elif act['target_offset'] == 2:
                hat = [2, 6, 7]
            
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")
            
        # Keine Information kann alles sein
        elif (highest_color_value == sec_highest_color_value \
              == sec_lowest_color_value == lowest_color_value):
            if act['target_offset'] == 1:
                hat = [0, 1, 4, 5]
            elif act['target_offset'] == 2:
                hat = [2, 3, 6, 7]
            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")        
        
        # Wenn die hinted color nicht die niedrigste Farbe ist
        # dann handelt es sich nicht um einen lowest color hint
        # wenn man aber keinen Rank kennt und
        # highest color == sec highest color == sec lowest color == hinted color
        # hinted_color_value != lowest_color_value
        # dann kann es sich um alles andere handeln aber nicht um
        # ein lowest color hint
        elif (hinted_color_value != lowest_color_value
              and highest_color_value == sec_highest_color_value
              == sec_lowest_color_value == hinted_color_value):

            if act['target_offset'] == 1:
                hat = [0, 1, 4]

            elif act['target_offset'] == 2:
                hat = [2, 3, 6]

            else:
                # target off set muss 1 oder 2 sein
                raise Exception("target offset must be 1 or 2")


        # Wenn die niedrigste Farbe gleich der zweithöchsten Farbe ist
        # ! Dieser Fall kann nur eintreten wenn alle Karten die gleiche Farbe haben
        # da der höchste rank aber auch der niedrigste rank ist kann der Fall nicht eintreten
        elif (sec_lowest_color_value == sec_highest_color_value):
            raise Exception("This case should never happen")

        else:
            raise Exception("This case should never happen")

        return hat

    def decode_hint_color_special_case_I_I(self, act,
            highst_color_value, sec_highst_color_value,
            lowest_color_value, sec_lowest_color_value,
            hinted_color_value):
        """Return hat vom hinted player hat wenn es sich um einen Color Hint handelt
        und es sich um einen speziellen Fall von einem Rank Hint handel könnte,
        und sec_lowest_card != sec_highest_card"""

        # Wenn die niedrigste Farbe nicht die zweitniedrigste Farbe ist
        # und die zweitniedrigste Farbe nicht die niedrigste Farbe ist
        # und der hint die zweitniedrigste Farbe ist dann handelt es sich
        # um den spezieller Fall Rank Hint lowest rank
        if (sec_lowest_color_value != sec_highst_color_value
            and sec_lowest_color_value != lowest_color_value
                and sec_lowest_color_value == hinted_color_value):

            if act['target_offset'] == 1:
                return [1]

            elif act['target_offset'] == 2:
                return [3]

        # Wenn die höchste Farbe nicht zweithöchste Farbe ist
        # und die zweitniedrigste Farbe nicht die zweithöchste Farbe ist
        # und die zweithöchste Farbe gehinted wurde
        # dann handelt es sich um den spezieller Fall Rank Hint highest rank
        elif (sec_lowest_color_value != sec_highst_color_value
              and sec_highst_color_value != highst_color_value
              and sec_highst_color_value == hinted_color_value):

            if act['target_offset'] == 1:
                return [0]

            elif act['target_offset'] == 2:
                return [2]

        # Wenn die höchste Farbe nicht zweithöchste Farbe ist
        # und die niedrigste Farbe nicht zweitniedrigste Farbe ist
        # aber die zweitniedrigste Farbe nicht die zweithöchste Farbe ist
        # und die zweitniedrigste / zweithöchste Farbe gehinted wurde
        # dann handelt es sich um den spezieller Fall von Rank Hint
        # man weiß aber nicht welcher
        elif (highst_color_value != sec_highst_color_value
                and lowest_color_value != sec_lowest_color_value
                and sec_lowest_color_value != sec_highst_color_value
                and (sec_lowest_color_value == hinted_color_value
                     or sec_highst_color_value == hinted_color_value)):

            if act['target_offset'] == 1:
                return [0, 1]

            elif act['target_offset'] == 2:
                return [2, 3]

        else:
            raise Exception("This case should never happen")

    def cal_own_hat(self, act):
        """Returned eigenen hat nur wenn man nicht selbst der gehinted player ist

        Parameters
            action (dict): Die Action muss ein Hint sein 
        """

        # Throw Exception wenn Action kein Hint ist
        if (act['action_type'] == 'PLAY' or
                act['action_type'] == 'DISCARD'):
            raise Exception("In update_tables action must be a hint")

        # given_hat_sum_mod8 := r1 (Paper Cox)
        # hat_sum_mod8 := ri (Paper Cox)
        # own_hat := ci (Paper Cox)

        idx_hinted_ply = (self.observation['current_player_offset'] +
                          act['target_offset']) % 3

        decode_hint = self.decode_hint(
            act, idx_hinted_ply, for_hinted_player=False)

        hat_other_ply = self.cal_hat_other_ply(idx_hinted_ply)[0]

        max_hat = (self.observation['num_players'] - 1) * 2

        own_hat = [(pos_hint_hat - hat_other_ply) % 8
                   for pos_hint_hat in decode_hint]

        return own_hat

    def cal_hat_other_ply(self, agent_idx):
        """Returned hat von anderen Agent nicht dem eigenen"""

        hat = []

        # Raise Expection wenn man den eigenen Hat berechnen will
        if (agent_idx == 0):
            raise Exception("Es kann nur der Hat von anderen Spielern \
                             berechnet werden")

        target_card, target_card_idx = self.get_target_card(agent_idx)

        poss_table_card = self.table.get_poss_card_table(
            agent_idx, target_card_idx)
        part_table = self.table.get_part_table(
            self.observation, poss_table_card)

        rank_target_card = target_card['rank']
        color_target_card = target_card['color']
        hat_value = part_table[color_target_card][rank_target_card]
        hat.append(hat_value)

        return hat

    def get_target_card(self, agent_idx):
        """Return Target Card und Index der Target Card in Hand"""

        poss_hand_table = self.table.get_poss_table_hand(agent_idx)
        sum_mc_Ti_cards, sum_mc_Ti_cut_Si_cards = self.get_sum_mc_Ti_and_sum_mc_Ti_cut_Si(
            poss_hand_table)
        pb_playable_cards = self.get_pb_playable_cards(agent_idx, poss_hand_table,
                                                       sum_mc_Ti_cards,
                                                       sum_mc_Ti_cut_Si_cards)

        player_hand = self.observation['observed_hands'][agent_idx]
        num_cards_in_hand = len(self.observation['observed_hands'][agent_idx])
        pb_playable_cards_in_hand = pb_playable_cards[0:num_cards_in_hand]

        target_card_idx = pb_playable_cards.index(
            max(pb_playable_cards_in_hand))
        target_card = player_hand[target_card_idx]

        return target_card, target_card_idx

    def get_sum_mc_Ti_and_sum_mc_Ti_cut_Si(self, poss_hand_table):
        """Return Nenner und Zahler von Formel S3"""

        sum_mc_Ti_cut_Si_cards = []
        sum_mc_Ti_cards = []

        for poss_table_card in poss_hand_table:

            sum_mc_Ti_cut_Si = 0
            sum_mc_Ti = 0

            for rank in range(self.max_rank + 1):
                for color in self.colors:
                    card = {'color': color, 'rank': rank}

                    # Alle Ti in
                    if (poss_table_card[color][rank] == 1):
                        sum_mc_Ti += self.mc[color][rank]

                    if (self.playable_card(card) and poss_table_card[color][rank] == 1):
                        sum_mc_Ti_cut_Si += self.mc[color][rank]

            sum_mc_Ti_cards.append(sum_mc_Ti)
            sum_mc_Ti_cut_Si_cards.append(sum_mc_Ti_cut_Si)

        return sum_mc_Ti_cards, sum_mc_Ti_cut_Si_cards

    def get_pb_playable_cards(self, agent_idx, poss_hand_table,
                              sum_mc_Ti_cards, sum_mc_Ti_cut_Si_cards):

        pb_playable_cards = []

        for card_idx in range(len(sum_mc_Ti_cards)):
            sum_mc_Ti = sum_mc_Ti_cards[card_idx]
            sum_mc_Ti_cut_Si = sum_mc_Ti_cut_Si_cards[card_idx]

            poss_card_table = poss_hand_table[card_idx]

            if self.table.get_ti(poss_card_table) == 1:
                pb_playable_cards.append(-1)
                continue

            try:
                pb_playable_cards.append(sum_mc_Ti_cut_Si / sum_mc_Ti)

            except ZeroDivisionError:
                # Wenn die Karte bekannt ist wird diese von mc abgezogen
                # Daraus folgt das mc = 0 sein keint
                # Dies kann zur ZeroDivisionError führen

                poss_table = self.table.get_poss_card_table(
                    agent_idx, card_idx)
                card = self.table.get_card(poss_table)

                if (self.playable_card(card) == True):
                    pb_playable_cards.append(1)

                else:
                    pb_playable_cards.append(0)

        return pb_playable_cards

    def get_hint_hat_sum_smaller_4(self, hat_sum_mod8):
        """Return Hint Rank if highst_rank != lowest_rank
           else return specific color hint"""

        idx_ply = 1 if hat_sum_mod8 == 0 or hat_sum_mod8 == 1 else 2

        hand_ply = self.observation['observed_hands'][idx_ply]

        highst_rank = self.highest_rank_in_hand(hand_ply)
        lowest_rank = self.lowest_rank_in_hand(hand_ply)

        if highst_rank != lowest_rank:
            if hat_sum_mod8 == 0 or hat_sum_mod8 == 2:
                hint = {'action_type': 'REVEAL_RANK',
                        'rank': highst_rank,
                        'target_offset': idx_ply}

            elif hat_sum_mod8 == 1 or hat_sum_mod8 == 3:
                hint = {'action_type': 'REVEAL_RANK',
                        'rank': lowest_rank,
                        'target_offset': idx_ply}

            else:
                raise ValueError("hat_sum_mod8 must be in [0, 3]")

        else:
            # Give a color hint if it is not possible to hint rank
            hint = self.get_spec_color_hint(hat_sum_mod8, hand_ply, idx_ply)

        return hint

    def get_spec_color_hint(self, hat_sum_mod8, hand_ply, idx_ply):
        """Return Hint Color with second highest or lowest color
           This only happen if it is not possible to hint rank
           becouse highst_rank == lowest_rank"""

        if hat_sum_mod8 == 0 or hat_sum_mod8 == 2:
            sec_highest_color = self.sec_highest_color_in_hand(hand_ply)

            hint = {'action_type': 'REVEAL_COLOR',
                    'color': sec_highest_color,
                    'target_offset': 2}

        elif hat_sum_mod8 == 1 or hat_sum_mod8 == 3:
            sec_lowest_color = self.sec_lowest_color_in_hand(hand_ply)
            hint = {'action_type': 'REVEAL_COLOR',
                    'color': sec_lowest_color,
                    'target_offset': 1}

        else:
            raise ValueError("hat_sum_mod8 must be in [0, 3]")

        return hint

    def get_hint_hat_sum_bigger_3(self, hat_sum_mod8):
        """Return Hint Color if highst_color != lowest_color
           else return specific rank hint"""

        idx_ply = 1 if (hat_sum_mod8 == 4 or hat_sum_mod8 == 5) \
            else 2

        hand_ply = self.observation['observed_hands'][idx_ply]

        lowest_color = self.lowest_color_in_hand(hand_ply)
        highst_color = self.highest_color_in_hand(hand_ply)

        if lowest_color != highst_color:
            if hat_sum_mod8 == 4 or hat_sum_mod8 == 6:
                hint = {'action_type': 'REVEAL_COLOR',
                        'color': highst_color,
                        'target_offset': idx_ply}

            elif hat_sum_mod8 == 5 or hat_sum_mod8 == 7:
                hint = {'action_type': 'REVEAL_COLOR',
                        'color': lowest_color,
                        'target_offset': idx_ply}

            else:
                raise ValueError("hat_sum_mod8 must be in [4, 7]")

        else:
            # Give a rank hint
            hint = self.get_spec_rank_hint(hat_sum_mod8, hand_ply, idx_ply)

        return hint

    def get_spec_rank_hint(self, hat_sum_mod8, hand_ply, idx_ply):
        """Return Hint Rank with second highest or lowest rank
           This only happen if it is not possible to hint color
           becouse sec_lowest_color == sec_highest_color"""

        if hat_sum_mod8 == 4 or hat_sum_mod8 == 6:
            sec_highest_rank = self.sec_highest_rank_in_hand(hand_ply)
            hint = {'action_type': 'REVEAL_RANK',
                    'rank': sec_highest_rank,
                    'target_offset': idx_ply}

        elif hat_sum_mod8 == 5 or hat_sum_mod8 == 7:
            sec_lowest_rank = self.sec_lowest_rank_in_hand(hand_ply)
            hint = {'action_type': 'REVEAL_RANK',
                    'rank': sec_lowest_rank,
                    'target_offset': idx_ply}

        else:
            raise ValueError("hat_sum_mod8 must be in [4, 7]")

        return hint

    def sorted_ranks_in_hand(self, hand_ply):
        """Return sorted list of ranks in hand"""

        sorted_ranks_in_hand = [card['rank'] for card in hand_ply]

        # Enter None aus liste
        sorted_ranks_in_hand = [rank for rank in sorted_ranks_in_hand
                                if rank is not None]

        sorted_ranks_in_hand.sort()

        return sorted_ranks_in_hand

    def lowest_rank_in_hand(self, hand_ply):
        """Return lowest color in hand"""
        sorted_ranks_in_hand = self.sorted_ranks_in_hand(hand_ply)

        if len(sorted_ranks_in_hand) == 0:
            return None

        return sorted_ranks_in_hand[0]

    def highest_rank_in_hand(self, hand_ply):
        """Return second highest color in hand"""
        sorted_ranks_in_hand = self.sorted_ranks_in_hand(hand_ply)

        if len(sorted_ranks_in_hand) == 0:
            return None

        return sorted_ranks_in_hand[-1]

    def sec_lowest_rank_in_hand(self, hand_ply):
        """Return second lowest rank in hand"""
        sorted_ranks_in_hand = self.sorted_ranks_in_hand(hand_ply)

        if len(sorted_ranks_in_hand) == 0:
            return None

        if len(sorted_ranks_in_hand) == 1:
            return sorted_ranks_in_hand[0]

        return sorted_ranks_in_hand[1]

    def sec_highest_rank_in_hand(self, hand_ply):
        """Return second highest rank in hand"""

        sorted_ranks_in_hand = self.sorted_ranks_in_hand(hand_ply)

        if len(sorted_ranks_in_hand) == 0:
            return None

        if len(sorted_ranks_in_hand) == 1:
            return sorted_ranks_in_hand[0]

        return sorted_ranks_in_hand[-2]

    def sorted_color_in_hand(self, hand_ply):
        """Return sorted color in hand"""

        # Entfern None aus der Liste
        hand_ply = [card for card in hand_ply if card['color'] is not None]
        color_values_in_hand = [Color[card['color']].value
                                for card in hand_ply]
        color_values_in_hand.sort()
        color_in_hand = [Color(value).name for value
                         in color_values_in_hand]

        return color_in_hand

    def lowest_color_in_hand(self, hand_ply):
        """Return lowest color in hand"""
        sorted_color_in_hand = self.sorted_color_in_hand(hand_ply)

        if len(sorted_color_in_hand) == 0:
            return None

        return sorted_color_in_hand[0]

    def highest_color_in_hand(self, hand_ply):
        """Return second highest color in hand"""
        sorted_color_in_hand = self.sorted_color_in_hand(hand_ply)

        if len(sorted_color_in_hand) == 0:
            return None

        return sorted_color_in_hand[-1]

    def sec_lowest_color_in_hand(self, hand_ply):
        """Return second lowest color in hand"""
        sorted_color_in_hand = self.sorted_color_in_hand(hand_ply)

        if len(sorted_color_in_hand) == 0:
            return None

        if len(sorted_color_in_hand) == 1:
            return sorted_color_in_hand[0]

        return sorted_color_in_hand[1]

    def sec_highest_color_in_hand(self, hand_ply):
        """Return second highest color in hand"""
        sorted_color_in_hand = self.sorted_color_in_hand(hand_ply)

        if len(sorted_color_in_hand) == 0:
            return None

        if len(sorted_color_in_hand) == 1:
            return sorted_color_in_hand[0]

        return sorted_color_in_hand[-2]

    def unknown_rank_in_hand(self, hand_ply):
        ranks_in_hand = [card['rank'] for card in hand_ply]
        
        if None in ranks_in_hand:
            return True
        
        return False

    def unknown_color_in_hand(self, hand_ply):
        color_in_hand = [card['color'] for card in hand_ply]
        
        if None in color_in_hand:
            return True
        
        return False

    def duplicate_card_in_hand(self, privat_poss_hand_table):
        """Return First duplicate Cards in hands
        if no card is duplicate return None"""

        for card_idx, poss_card_table in enumerate(privat_poss_hand_table):
            # Um zu bestimmen ob die Karte duplicate ist muss
            # sie bekannt sein also ti = 1

            if (self.duplicate_card_in_poss_card_table(poss_card_table)):
                return card_idx

        return None

    def duplicate_card_in_poss_card_table(self, privat_poss_card_table):
        """Return True if all cards in hand are duplicate, else False"""

        for color in self.colors:
            for rank in range(self.max_rank + 1):
                if privat_poss_card_table[color][rank] == 1:
                    card = {'color': color, 'rank': rank}
                    if self.duplicate_card(card) == False:
                        return False

        return True

    def duplicate_card(self, card):
        """Return True if card if duplicate else False"""

        # Betrachte nur die anderen Hände
        other_hands = self.observation['observed_hands'][1:]
        for other_hand in other_hands:
            for other_card in other_hand:
                if other_card == card:
                    return True

        return False

    def dispensable_card_in_hand(self, private_poss_hand_table):
        """Return Index von dispensable card in hand mit lowest Index
        Wenn keine Karte dispensable return None"""

        for card_idx, poss_card_table in enumerate(private_poss_hand_table):
            # Um zu bestimmen ob die Karte duplicate ist muss
            # sie bekannt sein also ti = 1

            if (self.dispensable_card_in_poss_card_table(poss_card_table)):
                return card_idx

        return None

    def dispensable_card_in_poss_card_table(self, privat_poss_card_table):
        """Return true if all poss cards in hand are dispensable"""

        for color in self.colors:
            for rank in range(self.max_rank + 1):
                if privat_poss_card_table[color][rank] == 1:
                    card = {'color': color, 'rank': rank}
                    if self.dispensable_card(card) == False:
                        return False

        return True

    def dispensable_card(self, card):
        """Return True if Card is dispensable, else False"""

        if (self.dead_card(card)):
            return True

        # Anzahl der verbleiben Karten
        # in Deck, Firework und Händen
        nr_rem_card_in_deck = [3, 2, 2, 2, 1]

        for card_dsc_pile in self.observation['discard_pile']:
            # Prüfe alle Karten im dsc_pile mit der selben Farbe und
            # einem geringen Rank
            if card_dsc_pile['color'] == card['color']:
                nr_rem_card_in_deck[card_dsc_pile['rank']] -= 1

        # Wenn die Karten nur noch einmal da ist
        # dann return True (Karte ist ToT)
        if nr_rem_card_in_deck[card['rank']] == 1:
            return False

        return True

    def update_mc(self):
        """Based on the Public Information we calculate mc
        For each card we find in public information (card_knowledge,
        discard_pile and firework) we reduce max number by one"""

        self.mc = self.init_mc()

        self.update_mc_based_on_card_knowledge()

        self.update_mc_based_on_discard_pile()

        self.update_mc_based_on_firework()

    def update_mc_based_on_firework(self):
        """ Update mc based on Firework"""

        # Jede Karte die im Firework liegt kann nicht
        # mehr auf der Hand eines Spieles sein
        firework = self.observation['fireworks']
        for color, max_rank in firework.items():
            for rank in range(max_rank):
                self.mc[color][rank] -= 1

    def update_mc_based_on_card_knowledge(self):
        """Update mc based on card_knowledge """

        card_knowledge = self.observation['card_knowledge']

        # Prüfe alle Karten in card_knowledge
        for player_card_knowledge in card_knowledge:
            for card in player_card_knowledge:

                # Wenn eine Karte vollständig bekannt dann reduziere mc
                # Diese Karte kann ja nicht mehr einer anderen Hand sein
                if (card['rank'] is not None and
                        card['color'] is not None):

                    self.mc[card['color']][card['rank']] -= 1

    def update_poss_tables_based_on_card_knowledge(self):
        """Update poss tables based on card knowledge"""

        card_knowledge = self.observation['card_knowledge']

        # Prüfe alle Karten in card_knowledge
        for player_idx, player_card_knowledge in enumerate(card_knowledge):
            for card_idx, card in enumerate(player_card_knowledge):

                # Wenn eine Karte vollständig bekannt dann reduziere mc
                # Diese Karte kann ja nicht mehr einer anderen Hand sein
                if (not (card['rank'] is None and
                         card['color'] is None)):

                    self.update_table_based_on_card_from_cardknowledge(
                        player_idx, card_idx, card)

    def update_table_based_on_card_from_cardknowledge(self, player_idx, card_idx, card):
        """Update table based on a card which is known due to cardknowledge"""

        for color in self.colors:
            for rank in range(self.max_rank + 1):

                if (card['rank'] is not None):

                    # Setze für jeden Rank außer den bekannten Rank
                    # Den Wert auf 0 für
                    for rank in range(self.max_rank + 1):

                        if rank == card['rank']:
                            continue

                        for color in self.colors:
                            self.table[player_idx][card_idx][color][rank] = 0

                if (card['color'] is not None):

                    # Setze jede Karte einer anderen Farbe auf 0
                    for color in self.colors:

                        # Überspringe die Farbe welche die Karte hat
                        if color == card['color']:
                            continue

                        for rank in range(self.max_rank+1):
                            self.table[player_idx][card_idx][color][rank] = 0

    def update_mc_based_on_discard_pile(self):
        """Update mc based on discard_pile """

        # Jede Karte die im Discard Pile ist kann nicht mehr in der Hand
        # eines anderen Spieler sein
        discard_pile = self.observation['discard_pile']
        for card in discard_pile:
            self.mc[card['color']][card['rank']] -= 1

    def update_poss_tables_based_card_knowledge(self):
        """Updaten den Possibilty Table auf Basis der card_knowledge
        (Also der Informationen die NUR aus einem hint entstehen, also nicht
        aus dem Hatguessig"""

        card_knowledge = self.observation['card_knowledge']

        for agent_idx, player_card_knowledge in enumerate(card_knowledge):
            for card_idx, card in enumerate(player_card_knowledge):

                # Update possibility table based on card
                self.update_poss_table_based_on_card_from_cardknowledge(
                    card, agent_idx, card_idx)

    def update_poss_table_based_on_card_from_cardknowledge(self, card, agent_idx, card_idx):
        """Update poss table based on card from card_knowledge

        Args:
            card (list): card from card_knowledge
            agent_idx (int): player index where the card came from
            card_idx (int): card index in hand from player 

        Returns:
            None
        """
        # Wenn man Rank von Karte Kennt, kann ausgeschlossen
        # werden das die Karte einen anderen Rank hat
        if (card['rank'] is not None):

            # Setze für jeden Rank außer den bekannten Rank
            # Den Wert auf 0 für
            for rank in range(self.max_rank + 1):

                if rank == card['rank']:
                    continue

                for color in self.colors:
                    self.table[agent_idx][card_idx][color][rank] = 0

        if (card['color'] is not None):

            # Setze jede Karte einer anderen Farbe auf 0
            for color in self.colors:

                # Überspringe die Farbe welche die Karte hat
                if color == card['colors']:
                    continue

                for rank in range(self.max_rank+1):
                    self.table[agent_idx][card_idx][color][rank] = 0

    def update_observation(self, observation):
        """Update Observation"""
        self.observation = observation

    def update_tables(self, action):
        """Update the table based on hint

        Parameters
        action (dict): Die Action muss ein Hint sein 
        """
        if (action['action_type'] == 'REVEAL_COLOR' or
                action['action_type'] == 'REVEAL_RANK'):

            self.update_tables_hint(action)

        if (action['action_type'] == 'PLAY' or
           action['action_type'] == 'DISCARD'):

            self.update_tables_play_or_discard(action)

    def update_tables_play_or_discard(self, action):
        """Update Table based on new Card"""

        thrown_card_idx = action['card_index']
        current_player_idx = self.observation['current_player_offset']
        num_hand_cards = len(
            self.observation['observed_hands'][current_player_idx])

        for card_idx in range(thrown_card_idx, num_hand_cards - 1):
            self.table[current_player_idx][card_idx] = self.table[current_player_idx][card_idx + 1]

        poss_table = {'B': [1, 1, 1, 1, 1],
                      'G': [1, 1, 1, 1, 1],
                      'R': [1, 1, 1, 1, 1],
                      'W': [1, 1, 1, 1, 1],
                      'Y': [1, 1, 1, 1, 1]}

        self.table[current_player_idx][num_hand_cards - 1] = poss_table

    def update_tables_hint(self, action):
        """Update Table based on hint"""
        # Berechne die Hütte aller Spieler (auch den eigenen)
        # auf Basis vom hint
        players_hats = self.players_hats(action)
        target_cards_idx = self.targeted_cards_idx()

        idx_hinting_player = self.observation['current_player_offset']

        for agent_idx in range(self.observation['num_players']):

            # Vom Spieler der den Tipp gibt kann der Poss Table
            # nicht upgedated werden
            if idx_hinting_player == agent_idx:
                continue

            # Update Poss Table auf Basis vom Hat bzw. der möglichen Hütte
            self.update_poss_table_based_on_hat(
                agent_idx,
                players_hats[agent_idx],
                target_cards_idx[agent_idx])

    def update_poss_table_based_on_hat(self, agent_idx, players_hats, target_card_idx):
        """Update the poss_table for an agent"""

        poss_table_card = self.table[agent_idx][target_card_idx]
        part_table = self.table.get_part_table(
            self.observation, poss_table_card)

        for color in self.colors:
            for rank in range(self.max_rank + 1):
                if part_table[color][rank] not in players_hats:
                    self.table[agent_idx][target_card_idx][color][rank] = 0

        # Ceck if phoss_table only contais 0 values / Bug purposes
        values_table = list(self.table[agent_idx][target_card_idx].values())
        one_list_values = sum(values_table, [])
        if sum(one_list_values) == 0:
            raise Exception('Poss Table only contains 0 values')

    def players_hats(self, action):
        """Return list with hats off all Players"""
        player_hats = []

        # Der Spieler der den Hint gibt, also
        idx_hinting_player = self.observation['current_player_offset']
        idx_hinted_player = (action['target_offset'] + idx_hinting_player) \
            % self.observation['num_players']

        for agent_idx in range(self.observation['num_players']):

            # Der Spieler der den Hint gibt kann ja nicht seinen Hat wissen
            # Damit wird dieser auch nicht berechnet den es ist keine
            # Public Information
            if agent_idx == idx_hinted_player:
                hat = self.cal_hat_hinted_ply(action, idx_hinted_player)

            elif agent_idx == idx_hinting_player:
                hat = None

            elif agent_idx == 0:
                hat = self.cal_own_hat(action)

            elif (agent_idx != idx_hinting_player
                  and agent_idx != idx_hinted_player
                  and agent_idx != 0):
                hat = self.cal_hat_other_ply(agent_idx)

            else:
                raise Exception("Dieser Fall sollte nicht auftreten")

            player_hats.append(hat)

        return player_hats

    def cal_hat_hinted_ply(self, action, idx_hinted_player):
        """Return hat of the player who is hinted"""

        given_hat = self.decode_hint(
            action, idx_hinted_player, for_hinted_player=True)

        hinting_ply_idx = self.observation['current_player_offset']

        # Wenn ich der jenige bin der gehintet wird muss ich den hat
        # vom den Spieler berechnen der nicht gehintet hat
        # Das ist also Spieler 1 oder 2
        if idx_hinted_player == 0:
            idx_other_player = 1 if hinting_ply_idx == 2 else 2

        # Wenn ich nicht der gehintete bin, bin ich der hintende oder der andere Spieler
        # Ich bin der andere Spieler wenn hinting_ply_idx == 1
        else:
            if idx_hinted_player == 1:
                idx_other_player = 0 if hinting_ply_idx == 2 else 2
            elif idx_hinted_player == 2:
                idx_other_player = 0 if hinting_ply_idx == 1 else 1
            else:
                raise Exception("Dieser Fall sollte nicht auftreten")

        hat_other_ply = self.cal_hat_player(idx_other_player, action)[0]

        hat_hinted_ply = [(pos_hat - hat_other_ply) %
                          8 for pos_hat in given_hat]

        return hat_hinted_ply

    def targeted_cards_idx(self):
        """Return list mit targed_cards von allen Agent
        außer dem der aktuell dar ist. Also dem der gehintet hat"""

        targeted_cards_idx = []
        idx_hinting_player = self.observation['current_player_offset']

        for agent_idx in range(self.observation['num_players']):

            # Der Spieler der den Hint gibt kann ja nicht seinen Hat wissen
            # Damit wird dieser auch nicht berechnet den es ist keine
            # Public Information
            if idx_hinting_player == agent_idx:
                targeted_cards_idx.append(None)
                continue

            _, target_idx = self.get_target_card(agent_idx)
            targeted_cards_idx.append(target_idx)

        return targeted_cards_idx
