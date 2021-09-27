import random


# This class is used to perform the human interaction automatically.
# Oracle is presented with the questions and the preferences for those questions.
# It will randomly choose the preferences everytime. This way it is used as a replacement for human interaction.
class Oracle:
    def __init__(self, size):
        self.picked = [0] * size

    def pick(self, q_idx, node):
        west_points = 0
        east_points = 0
        # Check how many of these questions I have picked before
        for i in range(len(q_idx)):
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
        if selected:
            for i in range(min(len(q_idx), 4)):
                if self.picked[q_idx[i]] == 0:
                    self.picked[q_idx[i]] = node.east[0].item[q_idx[i]]
        else:
            for i in range(min(len(q_idx), 4)):
                if self.picked[q_idx[i]] == 0:
                    self.picked[q_idx[i]] = node.west[0].item[q_idx[i]]
        # Return selected {0 = East, 1 = West}
        return selected
