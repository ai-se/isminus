"""This module is related to Oracle class"""
# pylint: disable=import-error,invalid-name,too-few-public-methods
import random


class Oracle:
    """
    This class is used to perform the human interaction automatically.
    Oracle is presented with the questions and the preferences for those questions.
    It will randomly choose the preferences everytime. So it is used to replace human interactions.
    """

    def __init__(self, size):
        """Constructor for oracle class"""
        self.picked = [0] * size

    def pick(self, q_idx, node):
        """Function to find a random preference value for a question"""
        west_points = 0
        east_points = 0
        # Check how many of these questions I have picked before
        q_idx_len = len(q_idx)
        for i in range(q_idx_len):
            if node.east[0].item[q_idx[i]] and self.picked[q_idx[i]] == 1:
                east_points += 1
            elif node.west[0].item[q_idx[i]] and self.picked[q_idx[i]] == 1:
                west_points += 1
        # Random selection favoring the side i like the most
        if east_points + west_points > 0:
            weighted_selection = west_points / (east_points + west_points)
        else:
            weighted_selection = 0.5

        if random.random() < weighted_selection:
            selected = 0
        else:
            selected = 1
        # Update my vector of picked options
        for i in range(min(len(q_idx), 4)):
            if selected and self.picked[q_idx[i]] == 0:
                self.picked[q_idx[i]] = node.east[0].item[q_idx[i]]
            elif not selected and self.picked[q_idx[i]] == 0:
                self.picked[q_idx[i]] = node.west[0].item[q_idx[i]]
        # Return selected {0 = East, 1 = West}
        return selected
