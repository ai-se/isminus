[![GitHub license](https://img.shields.io/github/license/ai-se/whun)](https://github.com/ai-se/whun/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/ai-se/whun)](https://github.com/ai-se/whun/issues)

# **About WHUN**
This repository is the official implementation of [Preference Discovery in Large Product Lines](https://arxiv.org/pdf/2106.03792.pdf "Preference Discovery in Large Product Lines")

AI tools can generate many solutions, some human preference must be applied to determine which solution is
relevant to the current project.One way to find those preferences is interactive search-based software engineering (iSBSE) where
humans can influence the search process. Current iSBSE methods can lead to cognitive fatigue (when they overwhelm humans with
too many overly elaborate questions.WHUN is an iSBSE algorithm that avoids that problem. Due to its recursive clustering procedure,WHUN only pesters humans for O(log2N) interactions. Further, each interaction is mediated via a feature selection procedure that reduces the number of asked questions. When compared to prior state-of-the-art iSBSE systems, WHUN runs faster, asks fewer questions, and achieves better solutions that are within 0.1% of the best solutions seen in our sample space. More importantly, WHUN scales to large problems (in our experiments, models with 1000 variables can be explored with half a dozen interactions where, each time, we ask only four questions). Accordingly, we recommend WHUN as a baseline against which future iSBSE work should be compared.

### **WHUN Algorithm**

WHUN is based on iSBSE method and it is applied on few data sets to prove its efficiency. The data model is obtained from the [Splot Research](http://www.splot-research.org "Splot Research") website. The data is in the binary format. Along with data for every model we have a set of constraints which makes the solution suitable. To achieve this the constraints are applied to the data set using a PICO SAT solver, which removes all the data points which do not fit into the constraints. This step reduces the size of the data set to a significant amount. Next step is where the iSBSE approach starts. Here human preferences are given in form of questions to Oracle, which choses an answer at every step in the binary clustering to eliminate many solutions. At the end of this we would be left with roughly 10% of the original data set. However, we need to find a best possible solution. For this the paper applies a ranking algorithm to rank all the solutions and pick the best. 

### **Flow Chart**
<br />
<img src="./images/whun_flow_chart.jpeg"
     style="float: left; margin-right: 8px;" />
<br />

### **Current Progress**

Code Refactoring : 

1. Code Modularization to remove tight coupling.
2. Removal of unused packages
3. Made hardcoded variables configurable
4. Static code analyser report before and after code refactoring 

### **Future work on WHUN**

1.) Adding test suite<br />
2.) Packaging - pip install whun<br />
3.) Currently human interaction in WHUN is automated using Oracle. Oracle is presented with the questions and it randomly chooses the human preference. We plan to replace Oracle with actual human interaction, We will provide a user interface which will take the human preference from User. Moreover, based on user preference UI will show possible solutions.<br />
4.) Visual repreentation of the whun product line.<br />
5.) Testing model with human inputs

## **Developer Guide**

### **Requirements**

To install requirements:
```
pip install -r requirements.txt
```

### **Installation**
```
python3 whun.py
```
### **Static Analysis Report**
```
```
### **Virtual Env**
```
vir
```
### **Code Formater**
```
fr
```

### **Group 37 Details:**

1.) Akhil Gangarpu Sudhakar (<agangar@ncsu.edu>)<br />
2.) Jaydeep Patel (<jpatel33@ncsu.edu>)<br />
3.) Shubham Waghe(<swaghe@ncsu.edu>)<br />
4.) Venkata Sai Teja Malapati(<vmalapa@ncsu.edu>)<br />
5.) Vijaya Durga Kona(<vkona@ncsu.edu>)<br />

### **Feature tracking**
[Jira Board](https://se2021-group37.atlassian.net/secure/RapidBoard.jspa?rapidView=1&selectedIssue=SEWE-37 "Jira Board")