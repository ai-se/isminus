This document contains the function and class descriptions:

### Class input_output 
This Module is related to io_helper_class.
The InputOutput is used to perform the below mentioned IO stream related operations:
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
