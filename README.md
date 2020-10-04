# Data Engineering Coding Challenges

## Judgment Criteria

- Beauty of the code (beauty lies in the eyes of the beholder)
- Testing strategies
- Basic Engineering principles

## Problem 1

### Parse fixed width file

- Generate a fixed width file using the provided spec (offset provided in the spec file represent the length of each field).
- Implement a parser that can parse the fixed width file and generate a delimited file, like CSV for example.
- DO NOT use python libraries like pandas for parsing. You can use the standard library to write out a csv file (If you feel like)
- Language choices (Python or Scala)
- Deliver source via github or bitbucket
- Bonus points if you deliver a docker container (Dockerfile) that can be used to run the code (too lazy to install stuff that you might use)
- Pay attention to encoding

## Choices

- Any language, any platform
- One of the above problems or both, if you feel like it.

---
### Assumptions: 
* Hopefully there will be no docker permission issues (I tested it on Windows 10 + msys2 + Docker Desktop and Linux Mint + Docker 19) 
* Performance optimisation is not required.
* Logging is not required. 
---
###  Requirements 
* python 3.7.9
* tox

#### Building :

    ./docker_build 

    uses existing artifact from .tox/dist 

    tox -e py37
    ./docker_build 

    rebuilds dist package
    
#### Running : 
        
    ./docker_run_fwf.sh 
    creates a file o.txt in the project directory based on spec.json 
    
    ./docker_run_csv.sh 
    creates a file o.csv from o.txt in the project directory based on spec.json