## NYU-AI-Spring 2018
Auther: Chen Zhang (cz1389@)  
Email: chen.zhang@nyu.edu  

### Programming Assignment 1

#### Background
1. [The Post Correspondence Problem](http://en.wikipedia.org/wiki/Post_correspondence_problem)  
1. [Problem definition](https://cs.nyu.edu/courses/spring18/CSCI-GA.2560-001/hwk1.html)  
1. [Coding requirements](https://cs.nyu.edu/courses/spring18/CSCI-GA.2560-001/prog1.html)  

#### About  
I tried to make the program generic. Some abstract classes are raised in the prgram,
even though Python 2 does not have official support for that. The code is well-documented
with docstring. It is not going to be hard to figure out the definition
and implementation details of the phantom abstract classes.  

- The [*iterative_deepening.py*](iterative_deepening.py) contains a generic *BFSwIterativeDeepening*
class good for **searchable objects**.  
- In [*dominos.py*](dominos.py), a **searchable class** (*DominoSpace*) is implemented
along with its dependents, an **element class** (*Domino*) and **state class** (*PostCorrespondenceState*).  
- [*dominos_test.py*](dominos_test.py) contains unittest for methods in [*dominos.py*](dominos.py).  

#### Input format  
Follow strictly the sample format in the [Coding requirements](https://cs.nyu.edu/courses/spring18/CSCI-GA.2560-001/prog1.html).  

- First line: max size of queue (regex: "\d+\n")  
- Second line: Max total number of states (regex: "\d+\n")  
- Remaining lines: Dominos (regex: "[\d+ \w+ \w+\n]+")  

#### Requirements  
- python 2.7
- argparse

#### Running the program
```
$ python dominos.py [-t] FILE  

positional arguments:  
  FILE             input file name.  
optional arguments:  
  -v, --verbose    print sequence of states generated in searching for the solution 
```

#### Output   
The solution will be printed to the termial.  

If a solution is found, the sequence of dominos will be printed. 
If '-v' is set, the sequence of states generated in searching for 
the solution will also be printed.  

If no solution is found, the program will indicate if there is 
no solution to the problem, or that the program failed to find
a solution under the given constraint.