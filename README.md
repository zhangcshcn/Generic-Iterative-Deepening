[![Build Status](https://travis-ci.org/zhangcshcn/Generic-Iterative-Deepening.svg?branch=master)](https://travis-ci.org/zhangcshcn/Generic-Iterative-Deepening)
[![codecov](https://codecov.io/gh/zhangcshcn/Generic-Iterative-Deepening/branch/master/graph/badge.svg)](https://codecov.io/gh/zhangcshcn/Generic-Iterative-Deepening)

Generic Iteratic Deepening package for `python 2.7`

Author: Chen Zhang  
Email: zhangc.sh.cn@gmail.com 

#### Background
This package is originally a responce to [Programming Assignment 1](https://cs.nyu.edu/courses/spring18/CSCI-GA.2560-001/prog1.html) of Aritifical Intelligence tough by [Professor Ernest Davis](https://cs.nyu.edu/davise/) with NYU.
1. [The Post Correspondence Problem](http://en.wikipedia.org/wiki/Post_correspondence_problem)  
1. [Problem definition](https://cs.nyu.edu/courses/spring18/CSCI-GA.2560-001/hwk1.html)  
1. [Coding requirements](https://cs.nyu.edu/courses/spring18/CSCI-GA.2560-001/prog1.html)  

#### About
I tried to make the program generic. Some abstract classes are raised in the prgram,
even though Python 2 does not have official support for that. The code is well-documented
with docstring. It is not going to be hard to figure out the definition
and implementation details of the phantom abstract classes. 

- [*iterative_deepening.py*](iterative_deepening.py) contains a generic **`IterativeDeepening`
class** good for **`Searchable` objects**. The abstract classes of `Searchable` and `State` are also implemented.  
- [*dominos.py*](dominos.py), is the code that solves the assignment problem. A `DominoSpace` (subclass of `Searchable`) and `PostCorrespondenceState` (subclass of `State`) are implemented, along with class `Domino`. 
- [*iterative_deepening_test.py*](iterative_deepening_test.py) includes the unit test for the package. A commonly seen `TreeNode` class is defined, and is wraped up to `TreeState` by inheriting `State` defined in [*iterative_deepening.py*](iterative_deepening.py). 

The package provides the following search methods:
- `BFS` Standard Breadth-First Search w/ or w/out maxmium queue size and maximum number of states explored
- `DFS` Standard Depth-First Search w/ or w/out maximum number of states explored
- `IterativeDeepening` Standard Iterative Deepening w/ or w/out maximum number of states explored
- `Search` Iterative Deepening using a list of seeds initialized with BFS w/ maximum queue size.

The search methods returns the solution (`None` if unfound) 
and the error code

> 0 - sulution found  
> 1 - no soluion exists  
> 2 - solution not found within the constraints  
