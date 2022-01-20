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
```
Function: update_picked_array
            Description: Function to update picked array based on the corresponding attributes that are selected.
            Inputs:
                -selected: Value that determines if the east branch is selected or the west branch is selected.
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
###Class tree_node
This class is used for the following tasks:
1. Initialising the tree node
2. Finding the difference between east and west nodes
3. Finding the difference array between east and west nodes

####Member functions:
```
        Function: __init__
        Description: Initialises the attributes of the TreeNode
        Inputs:
                east :Item
                west :Item
                east_node :TreeNode
                west_node  :treeNode
                leaf : boolean
        Output:
                self initialised with attributes
```
```
        Function: difference
        Description: Returns the difference of east and west items
        Inputs:
                self :TreeNode
        Output:
                np.sum(res) :Sum of elements in res,Numpy array
```
```
        Function: diff_array
        Description: Returns the difference array of east and west items
        Inputs:
                self :TreeNode
        Output:
                res :Numpy Array
```
###Class utils
This is the utility class and is used for the following tasks
1. Split the east and west items
2. To find the tree node after splitting

####Member functions:
```
    Function: sway
    Description: Takes a specific number of items of type Item and returns
    the root after calculating the west,east,east_node and west_node
    Inputs:
        -items:Item
        -enough:integer
    Output:
        -root :TreeNode
```
```
    Function: sway
    Description: Takes a items of type Item and total groups,
    calcultes radius, take each item and put them in their radius
    and sort them by distance in reverse and converted all the items
    to the polar coordinate system and divide them into east and west.
    Inputs:
        -items:Item
        -total_group:integer
    Output:
        -west: representative of the group
        -east: representative of the group
        -west_items: all the others items except the representative
        -east_items: all the others items except the representative
```
###Class Method
This class is used store the sat solver solutions in form of a tree,
    ranking of each node down to its feature and then handles the weight adjustments,
    re-ranking tree based on the user preferences and finding the corresponding
    solutions.

####Member functions:
```
    Function: pick_questions
        Description: returns questions associated with this node
        Inputs:
            -self: method object
            -node: item node
        Output:
            -questions: array of questions
```
```
    Function: find_node
        Description: creates a queue of trees and returns path_id and
        node based on tree and current best node
        Inputs:
        Output:
            -path_id: path
            -node: last node in the path
```
```
    Function: adjust_tree
        Description: adjusts the current node of tree based on picked questions
        Inputs:
            -self: method object
            -node: item node
            -q_idx: picked questions
        Output:
```
```
    Function: get_index
        Description:
        Inputs:
            -self: method object
            -diff:
            -ranks:
        Output:
            questions: questions specific to this nodes
```
```
    Function: process_options
            Description: Given east and west branch, the method will check if both the branches have valid nodes or not.
            If one of the branch doesn't have valid nodes it will return the other brancch as selectedd preference.
            Inputs:
                -self: method object
                -left_branch: East Branch
                -right_branch: West Branch
            Output:
                - 0: If east branch doesn't have any valid nodes, we send 0 signifying that west branch needs to be selected.
                - 1: If west branch doesn't have any valid nodes, we send 1 signifying that east branch needs to be selected.
                - -1: If both the branches have valid nodes, we send -1 signifying that human needs to select his preference.
```
```
    Function: ask_questions
        Description:
        Inputs:
            -self: method object
            -q_idx: picked questions
            -node: item node
        Output:
```
```
    Function: adjust_weights
        Description: adjusts the weights in tree based on picked question
        Inputs:
            -self: method object
            -node: item node
            -picked: picked question
            -q_idx: all questions related to node
        Output:
```
```
    Function: increment the depth of east_node and west_node if its not None
        Description:
        Inputs:
            -self: method object
            -node: item node
            -depth: Integer, picked question
        Output:
```
```
    Function: re_rank
        Description: rerank the tree based on current state of the method object
        Inputs:
            -self: method object
        Output:
```
```
    Function: check_solution
        Description: finds all the possible solutions in the tree
        Inputs:
            -self: method object
        Output:
```
```
    Function: get_item
        Description: return item based on the input path
        Inputs:
            -self: method object
            -path: item node
        Output:
```
```
    Function: pick_best
        Description: picks the best solution among all the possible solutions
        Inputs:
            -self: method object
            -solutions: item node
        Output:
            solution:
```
###Class SatSolver
This class is used for getting Items

####Member functions:
```
    Function: get_solutions
    Description: Takes CNF and evaluation metrics and returns list of Item class objects
        Inputs:
            -cnf:String
            -eval_file:String
        Output:
            -items:Item
```
###Class Search
This class is used for searching the tree

####Member functions:
```
    Function: bfs
    Description: Takes tree and target and creates a queue of trees and returns path_id and node
        Inputs:
            -tree: String
            -target:String
        Output:
            -path_id: path
            -node: last node in the path
```
```
    Function: bfs_final
    Description: Takes tree and target and creates a queue of trees and returns path_id and node
        Inputs:
            -tree: String
            -target:String
        Output:
            -path_id: path
            -node: last node in the path
```
```
    Function: get_all_items
    Description: Takes tree and returns results
        Inputs:
            -tree: TreeNode
        Output:
            -results: results
```
```
    Function: get_all_leaves
    Description: Takes tree and returns leaves
        Inputs:
            -tree: TreeNode
        Output:
            -results: results with leaves
```
```
    Function: get_item
    Description: Takes tree and path, and returns item
        Inputs:
            -tree: TreeNode
            -path: array
        Output:
            -item: either from the west of the east side
```
###Class CustomDialog
This class is used to handle the dialog box that is presented to the Human to choose his preference.

####Member functions:
```
     Function: constructor
     Description: Initializes the class object attributes with initial values
            Inputs:
                -center_widget: Center Widget instance
                -left_branch: East branch to show east branch node attributes
                -right_branch: West branch to show west branch node attributes
                -parent: Parent widget if any, default value is None
            Output:
                None

```
###Class UIHelper
This class is used to create Graphical User Interface which can be used for human interaction purposes.

####Member functions:
```
    Function: constructor
    Description: Initializes the class object attributes with initial values
            Inputs:
                -q_app_ref: QApplication reference
                -sneak_run: SNEAK method to be invoked on clicking run button in GUI
                -parent: Parent widget if any, default value is None
            Output:
                None
```
```
    Function: prepare_landing_screen
    Description: Function to initialize all the UI components of Landing Screen
            Inputs:
                -sneak_run: Method to initiate SNEAK algorithm execution. Will be invoked on clicking run button in GUI
            Output:
                None
```
```
    Function: prepare_wait_screen
    Description: Function to initialize all the UI components of Wait/Processing Screen
            Inputs:
                None
            Output:
                None
```
```
    Function: prepare_results_screen
    Description: Function to initialize all the UI components of Iteration Screen
            Inputs:
                None
            Output:
                None
```
```
    Function: update_widget
    Description: Function to change screens based on the flow of the code
            Inputs:
                -next_widget: Value of the next screen that needes to be shown
            Output:
                None
```
```
    Function: run_button_handler
    Description: Function to handle the run button click on GUI
            Inputs:
                -sneak_run: SNEAK method to be invoked on clicking run button in GUI
            Output:
                None
```
```
    Function: update_result_label
    Description: Function to update Result label in the GUI
            Inputs:
                -result: String that contains list of prefernces that SNEAK has generated based on Human interaction
            Output:
                None
```
```
    Function: show_options_dialog
    Description: Function to show dialog box to the human inorder for the human to select his preferences
            Inputs:
                -left_branch: East branch nodes that contain attributes
                -right_branch: West branch nodes that contain attributes
            Output:
                - 1: Return 1 if the user has selected the attributes of the east branch
                - 0: Return 0 if the user has selected the attributes of the west branch
```