# pylint: disable=missing-module-docstring, wrong-import-position, too-few-public-methods, line-too-long, too-many-arguments, unused-variable, pointless-string-statement, used-before-assignment, no-value-for-parameter

import sys
import os
import copy
import numpy as np

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
parentPath2 = os.path.dirname(parentPath)
sys.path.append(parentPath2)


from bad.encoding.observation import Observation
from bad.action_provider import ActionProvider

class LikelihoodHandCard(dict):
    '''likely hood hand card'''
    def __init__(self, idx_ply: int, idx_card: int, constants, observation: Observation,
                 act_network: ActionProvider, last_act: int = None, pub_belief = None, pre_hanabi_env = None):
        """Initialize / Update the likelihood based on the action, observation and action network
           By initializing the likelihood, the first time last_act,pub_belief and pre_hanabi_env are None

        Args:
            idx_ply: Index Player curresondes to this HandCard 
            idx_card: Card Index from HandCard
            constants (HanabiEnv): Hanabi environment 
            observation (Observation): Part of Input from Network
            act_network (ActionNetwork): Network that predicts the action
            last_act (int, None): the last action taken by the agent
            public_belief (PublicBelief, None): Public belief from the previous step
            pre_hanabi_env(HanabiEnviornment, None): Hanabi Enviornment from previous step 

        Returns:
            dict: Likelihood to be a spefic for a hand card 
                  based on action of other player 
        """

        self.idx_ply = idx_ply
        self.idx_card = idx_card
        super().__init__(self.init(constants, observation,
                                   act_network, last_act, pub_belief, pre_hanabi_env))

    def init(self, constants, observation: Observation, act_network: ActionProvider,
             last_act, pub_belief, pre_hanabi_env) -> dict:
        '''init'''

        if (pub_belief is None and last_act is None
                and observation is None):
            '''Initialize the likelihood for the first time'''
            return self.first_init_likelihood(constants)

        # Update the likelihood based on the old likelihood, action, input from network and action network
        return self.update_likelihood(constants, observation, act_network,
                                      last_act, pub_belief, pre_hanabi_env)

    def first_init_likelihood(self, constants) -> dict:
        """Initialize the likelihood for the first time"""

        likelihood_hand_card = {}

        list_one = [1 for _ in range(constants.num_ranks + 1)]
        for color in constants.colors:
            likelihood_hand_card.update({color: list_one.copy()})

        return likelihood_hand_card

    def update_likelihood(self, constants, observation: Observation, network: ActionProvider,
                          last_act, pub_belief, pre_hanabi_env) -> dict:
        """Update the likelihood based on the old likelihood, action, input from network and action network"""

        # Get all possible hand_card combinations
        hand_card_combinations = self.hand_card_combinations(constants)

        # Get the possiblity for hand_card_combinations
        hand_card_combinations_possibility = self.hand_card_combinations_pos(
            act_network_output, last_act)

        # Create observations based on the hand_card_combinations, which are used as an input
        # for the action network to get the action based on the hand_card_combinations
        observations_for_hand_card_combinations = self.create_observations(observation, hand_card_combinations)

        # Get action from network based on hand_card_combinations and observation (input from network)
        act_network_output = self.output_actions_network(
            observations_for_hand_card_combinations, pre_hanabi_env, pub_belief, network)

        # Update the hand_card_combinations_possibility
        # based on the action from network
        # (Eliminate the hand_card_combinations that are not possible)
        hand_card_combinations_possibility = self.update_hand_card_combinations_pos(
            hand_card_combinations_possibility, act_network_output, last_act,
            pub_belief.hint_matrix)

        # Normalize the hand_card_combinations_possibility
        hand_card_combinations_possibility = self.normalize_hand_card_possibility(
            hand_card_combinations_possibility)

        # Get the possiblity for each possible hand_card
        hand_card_possibility = self.hand_card_possibility(
            hand_card_combinations_possibility)

        # Update the likelihood based on the hand_card_combinations_possibility
        likelihood = self.calculate_new_likelihood(
            pub_belief, hand_card_possibility)

        return likelihood

    def create_observations(self, observation: Observation, hand_card_combinations) -> list:
        """Create observations based on the hand_card_combinations, which are used as an input
        for the action network to get the action based on the hand_card_combinations"""

        observations_for_hand_card_combinations = []
        for hand_card_combination in hand_card_combinations:
            observations_for_hand_card_combinations.append(
                self.observation_based_on_hand_card_combination(observation, hand_card_combination))

        return observations_for_hand_card_combinations

    def observation_based_on_hand_card_combination(self, observation: Observation,
                                                   hand_card_combination) -> Observation:
        """Create an observation based on the hand_card_combination and old observation"""
        new_observation = copy.copy(observation)
        other_ply_hand = new_observation['player_observations'][0]['observed_hands'][1]
        for idx_card, card in enumerate(hand_card_combination):
            other_ply_hand[idx_card] = card

        return new_observation

    def hand_card_combinations(self, constants) -> list:
        """Returns all possible hand_card combinations"""

        # Get all possible cards
        card_combinations = self.card_combinations(constants)

        # Build all possible hand_card combinations
        hand_card_combinations = []
        for card1 in card_combinations:
            for card2 in card_combinations:
                for card3 in card_combinations:
                    hand_card_combinations.append([card1, card2, card3])

        return hand_card_combinations

    def card_combinations(self, constants) -> list:
        """Return all possible cards"""
        card_combinations = [{'color': color, 'rank': rank} for color in constants.colors
                             for rank in range(constants.max_rank + 1)]

        return card_combinations

    def output_actions_network(self, observations_for_hand_card_combinations,
                               pre_hanabi_env, pub_belief, network: ActionProvider) -> list:
        """Returns the actions from network based on hand_card_combinations and observation (input from network)"""

        output_actions = []
        for observation in observations_for_hand_card_combinations:
            bad = network.get_action(observation)
            bad_result = bad.decode_action(pre_hanabi_env.state.legal_moves_int(), pub_belief)
            next_action = bad_result.sampled_action
            output_actions.append()

        return output_actions

    def build_observations(self, public_feature_one_hot_sig_vec, hand_card_combis_one_hot) -> list:
        """Create Inputs for network"""

        inputs_network = []
        for hand_card_combi_one_hot in hand_card_combis_one_hot:
            inputs_network.append(np.concatenate(public_feature_one_hot_sig_vec, hand_card_combi_one_hot))

        return inputs_network

    def hand_card_combinations_pos(self, hand_card_combinations, public_belief) -> list:
        """Returns the possiblity for hand_card_combinations"""

        hand_card_combinations_possibility = []
        for card_combination in hand_card_combinations:

            # Get the possiblity for each card
            card1_possiblity = self.card_possibility(
                card_combination[0], public_belief, 0)
            card2_possiblity = self.card_possibility(
                card_combination[1], public_belief, 1)
            card3_possiblity = self.card_possibility(
                card_combination[2], public_belief, 2)

            # Get the possiblity for the hand_card_combination and append it to the list
            hand_card_combinations_possibility.append(
                card1_possiblity * card2_possiblity * card3_possiblity)

        return hand_card_combinations_possibility

    def card_possibility(self, card, public_belief, card_idx):
        """Returns the possibility for a card based on the public belief"""
        card_color = card['color']
        card_rank = card['rank']
        card_possibility = public_belief[self.idx_ply][card_idx][card_color][card_rank]

        return card_possibility

    def update_hand_card_combinations_pos(self, hand_card_combis_pos,
                                          network_output, last_act, hint_matrix) -> list:
        """Update the hand_card_combinations_possibility based on the action from network
           (Eliminate the hand_card_combinations that are not possible)

        Args:
            hand_card_combis_pos (list): Possibility for all combinations of own hand based on public belief
                                           A.k.a. the possibility for the hand card combinations 
            network_output (list): Outputs from the network based on the hand card combinations 
            last_act (_type_): last action with the other action played
            hint_matrix (HintMatrix): 

        Return:
            hand_card_combis_pos(list): Updated Version of possibility for our own hand  
        """

        # Eliminate the hand_card_combinations that are not possible
        # based on the action from network
        hand_card_combis_pos = self.update_hand_card_combinations_pos_based_on_net_output(
            hand_card_combis_pos, network_output, last_act)

        # Eliminate the hand_card_combinations that are not possible based on hint_matrix
        hand_card_combis_pos = self.update_hand_card_combinations_pos_based_on_hint_matrix(
            hand_card_combis_pos, hint_matrix)

        return hand_card_combis_pos

    def update_hand_card_combinations_pos_based_on_net_output(self, hand_card_combinations_possibility,
                                                                  act_network_output, last_act):
        """Eliminate the hand_card_combinations that are not possible based on the action from network"""
        for idx, action in enumerate(act_network_output):
            if action != last_act:
                hand_card_combinations_possibility[idx] = 0

        return hand_card_combinations_possibility

    def update_hand_card_combinations_pos_based_on_hint_matrix(self, hand_card_combinations_possibility,
                                                               hint_matrix):
        """Eliminate the hand_card_combinations that are not possible based on hint_matrix"""

        for idx_hand_card_combination, hand_card_combination in hand_card_combinations_possibility:
            for idx_card, card in enumerate(hand_card_combination):
                card_rank = card['rank']
                card_color = card['color']
                if hint_matrix[self.idx_ply][idx_card][card_color][card_rank] == 0:
                    hand_card_combinations_possibility[idx_hand_card_combination] = 0

        return hand_card_combinations_possibility

    def normalize_hand_card_possibility(self, hand_card_combinations_possibility):
        """Normalize the hand_card_combinations_possibility"""

        my_sum = 0
        for possibility in hand_card_combinations_possibility:
            my_sum += possibility

        for i, possibility in enumerate(hand_card_combinations_possibility):
            hand_card_combinations_possibility[i] = possibility / my_sum

        return hand_card_combinations_possibility

    def hand_card_possibility(self, hand_card_combinations_possibility, hand_cards_combination) -> dict:
        """Get the possiblity for each possible hand_card"""
        all_possible_cards = self.card_combinations()

        # Init dict for hand_card_possibility
        hand_card_possibility = {}
        for card in all_possible_cards:
            hand_card_possibility.update({card: 0})

        # Get for each card the possibility based on the hand_card_combinations_possibility
        for hand_card_combination_pos in hand_card_combinations_possibility:

            # The card possibilty is based on the card_idx
            card = hand_cards_combination[self.idx_card]

            hand_card_possibility[card] += hand_card_combination_pos

        return hand_card_possibility

    def calculate_new_likelihood(self, pub_belief: dict, hand_card_combinations_possibility):
        """Update the likelihood based on the hand_card_combinations_possibility and the old likelihood"""
        new_likelihood = {}
        for color, color_likelihood in pub_belief.likelihood.items():
            new_color_likelihood = [hand_card_combinations_possibility[color][rank] * color_likelihood[rank]
                                    for rank in range(len(color_likelihood))]
            new_likelihood.update({color: new_color_likelihood})

        return new_likelihood
