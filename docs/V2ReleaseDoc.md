# Release 2.0.1

### Packaging: 
The WHUN code base has been exposed as Python package which is available to to be installed in users’ system and run. whun_run method will allow the user to input the constraints in CNF format and obtain best solution in the search space. 

```
pip install -i https://test.pypi.org/simple/ whun==0.0.1 
```

### Unit Testing and Code Coverage

Unit testing was done using pytest python package. This was integrated with Travis for CI and every time there was a commit into the code base, automatically tests would run and generate a report about pass/fail and the code coverage was reported using coverage python package. The reports were sent to each contributor in mail. 

```
Coverage: https://coveralls.io/github/ai-se/whun
Travis: https://app.travis-ci.com/github/ai-se/whun
```

### Travis integration

Travis CI was integrated to check the stability after each commit. The requirements were installed from requirements.txt. We used multiple python versions to have a backward compatibility and also included a script to run test and coverage on each build. 
```
Travis yml : https://github.com/ai-se/whun/blob/feature-se2021/.travis.yml 

Coverage report:
coverage run --source=./src/whun/whun_helper,./src/whun/utils -m pytest && coverage report
```

### Short Releases

The deliverables were planned monthly and according to that we released the first version at the end of September. 
https://github.com/ai-se/whun/releases/tag/1.0.1

Release 1.0.1 included: 
1. Study of the research work
2. Modularization
3. Refactoring
4. Styler and Formatter
5. Kernel best practices
6. Initial Documentation

We are going to make the second release for October end - Release 2.0.1
https://github.com/ai-se/whun/releases/tag/2.0.1

### No Regression Rule

Any previously working functionality was not broken due to the new implementations. We added more enhancements to the code. We did packaging, added tests cases and travis integration. The issues we faced while doing the integrations were all fixed and reported in JIRA. 
```
JIRA link: https://se2021-group37.atlassian.net/jira/software/c/projects/SEWE/boards/1
```
### Short Video 

The following is a short high level video describing the research and use case.
It summarises the details of the first and second release, and the expected future work.

<video style="width:70%" controls>
  <source src="https://app.animaker.com/video/VOSL7A6ONJOVJSG3">
  Your browser does not support the video tag.
</video>