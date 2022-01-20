**Video link for 3rd iteration demo:** [[DEMO Video for 3rd Iteration]](https://youtu.be/FWYoTp2SbPk)

[![GitHub license](https://img.shields.io/github/license/ai-se/whun)](https://github.com/ai-se/whun/blob/main/LICENSE) 
[![GitHub issues](https://img.shields.io/github/issues/ai-se/whun)](https://github.com/ai-se/whun/issues)
[![arXiv](https://img.shields.io/badge/arXiv-2106.03792-orange.svg)](https://arxiv.org/abs/2106.03792)

![GitHub release (latest by date)](https://img.shields.io/github/v/release/ai-se/whun)
[![Build Status](https://app.travis-ci.com/ai-se/whun.svg?branch=feature-se2021)](https://app.travis-ci.com/ai-se/whun)
[![Coverage Status](https://coveralls.io/repos/github/ai-se/whun/badge.svg?branch=feature-se2021)](https://coveralls.io/github/ai-se/whun?branch=feature-se2021)
# **About SNEAK**
This repository is the official implementation of  ~~Redacted~~

AI tools can generate many solutions, some human preference must be applied to determine which solution is
relevant to the current project.One way to find those preferences is interactive search-based software engineering (iSBSE) where
humans can influence the search process. Current iSBSE methods can lead to cognitive fatigue (when they overwhelm humans with
too many overly elaborate questions.SNEAK is an iSBSE algorithm that avoids that problem. Due to its recursive clustering procedure,SNEAK only pesters humans for O(log2N) interactions. Further, each interaction is mediated via a feature selection procedure that reduces the number of asked questions. When compared to prior state-of-the-art iSBSE systems, SNEAK runs faster, asks fewer questions, and achieves better solutions that are within 1% of the best solutions seen in our sample space. More importantly, SNEAK scales to large problems (in our experiments, models with 1000 variables can be explored with half a dozen interactions where, each time, we ask only four questions). Accordingly, we recommend SNEAK as a baseline against which future iSBSE work should be compared.


### **SNEAK Algorithm**

SNEAK is based on data mining and semi-supervised optimization techniques and it can be applied to various different models. Sample models can be obtained from the [Splot Research](http://www.splot-research.org "Splot Research") website. The dataset is required to be binary. For [Splot Research](http://www.splot-research.org "Splot Research") models we can generate our dataset of solutions through PycoSAT, a sat solver capable of producing valid solutions to these CNF-based models. For other models used in this study, please refer to the original paper of these models or to the code provided by Chen et al in their SWAY paper. SNEAK then performs interactions with humans (or with an oracle). In these interactions human preferences are queried to the human, which choses a set of preferences at every step to eliminate many solutions. At the end of this we would be left with roughly 10% of the original data set. However, we need to find a best possible solution. 

For this the paper can apply different strategies towards finding this best possible solution depending on the time-complexity of the objective evaluation function of the chosen model. These strategies are described in our research. The package provided here uses the ''*standard*'' strategy.

### **Flow Chart**
<br />
<img src="./images/WHUN_flow_chart.jpeg"
     style="float: left; margin-right: 8px;" />
<br />


### **Steps to use SNEAK Package**
```
from SNEAK import SNEAK
SNEAK.SNEAK_run(['flight_bin.csv'],['flight_eval.csv'])
```
### **GUI for Human Interaction**
Inorder to run SNEAK with human interaction you need to execute the "SNEAK_run" method with the required file name attributes and "is_oracle_method" flag as False.

When the SNEAK_run method executes it will open a window with user interface. User can proceed using the GUI to run SNEAK and choose his/her preferences accordingly.

Below is a sample snippet on how to execute the SNEAK_run method.
```
SNEAK_run(['Scrum10k.csv'], ['flight_eval.csv'], False)
```

To run the method for users for the SCRUM model simply execute from the base folder
```
pip install -r 'requirements.txt'
python \src\whun\sneak.py
```

### **Potential Users**
SNEAK algorithm is meant to be a new baseline for future iSBSE algorithms.

SNEAK can also be used in production code without any warranties and the code is provided as is.






### **References**

* Authors for ~~redacted~~

