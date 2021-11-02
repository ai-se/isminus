This document contains the function and class descriptions:

### Class input_output 
This Module is related to io_helper_class.
The InputOutput is used to perform the below-mentioned IO stream related operations:
1. Convert dimacs input to CNF format.
2. Read the question text input from the csv file.

#### Member functions:
```
Function: read_dimacs
        Description: This function is created to read dimac format input and convert it to CNF form
        Input:
            - filename : File
        Output:
            - names : Array of features
            - cnf : Solution in CNF form
```
```
Function : get_question_text
        Description : This function is created to read text input regarding questions
        Input:
            - filename : File
            - column : int
        Output:
            - column of dataframe : DataFrame
```

### Class item
This class has the structure for each solution with all required parameters

#### Member functions:

```
Function : __init__
        Description : This is the constructor for item_helper_class class
        Input :
            - item : item
            - eval : Array
```

```
Function : calc_staticfeatures
        Description : This function updates the parameters related to static features
        Input:
            - items : item[]
        Output:
            - none
```
```
Function : rank_features
        Description :  This function is used to update the ranking parameters of all the features
        Input:
            - items : item[]
            - names : Array of attribute names
        Output:
            - count : int
            - rank : int
```

### Class oracle
This class is used to perform the human interaction automatically.
Oracle is presented with the questions and the preferences for those questions.
It will randomly choose the preferences everytime. So it is used to replace human interactions.

####Member functions:
```
Function: constructor
            Description: Initializes the class object attributes with initial values
            Inputs:
                -size: number
            Output:
                None
```
```
Function: pick
            Description: Function to find a random preference value for a question inorder to do the human interaction automatically
            Inputs:
                -q_idx: List of indices of questions
                -node: TreeNode
            Output:
                -selected : Either 1 or 0 based on the condition if the preference is selected or not.
```

###Class ranker
This class is used for the following tasks:
1. Ranking all the solutions
2. Finding the current best node to ask further questions to the user
3. Checking for the best solutions

####Member functions:
```
Function: level_rank_features
            Description: Function to build a tree of all the solutions
            Inputs:
                -root: TreeNode
                -weights: Array of weights from Method class object.
            Output:
                -items_rank : Solutions tree based on the ranking
```
```
Function: rank_nodes
            Description: Function to find out the current best node to ask human preferences
            Inputs:
                -root: TreeNode
                -rank: Rank value from Method class object.
            Output:
                -largest : Largest score among the questions
```