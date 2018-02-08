#! /usr/bin/python2
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os

class Domino:
  def __init__(self, index, content):
    self.index = index
    self.content = content

class PostCorrespondenceState:
  def __init__(self, seqs=("", ""), history=None):
    self.seqs = seqs
    self.history = history or []
  
  def IsValid(self):
    return True if self.history else False
    

class DominoSpace:
  '''
  The class DominoSpace contains 
    fields:
      start_point: a PostCorrespondenceState to start with. 
        Initialized to seqs=("", ""), history=[].
      dominos: a list of Domino.
    methods:
      Neighbors(state): generate a list of neighboring STATEs of the 
        given state by trying concatenating dominos.
      Assert(state): determine if the STATE meets the goal.
 '''
  def __init__(self, dominos, 
               start_point=PostCorrespondenceState(("", ""),[])):
    self.start_point = start_point
    self.dominos = sorted(dominos, key=lambda d:d.index)

  def _CatDomino(self, state, domino):
    '''
    Concatenate a domino to a state and determine if it is valid.
    Args:
      state: a PostCorrespondenceState Object.
        A valid state should have at least one empty string ("").
      domino: (int, (str_top, str_bottom)) to concatenate to the state.
    Returns:
      If a valid state is produced, return the state.
      Otherwise return None.
    '''
    state_top, state_bottom = state.seqs
    domino_top, domino_bottom = domino.content
    new_top, new_bottom = state_top + domino_top, state_bottom + domino_bottom
    max_len_prefix = min(len(new_top), len(new_bottom))
    if new_top[:max_len_prefix] == new_bottom[:max_len_prefix]:
      return PostCorrespondenceState(
          (new_top[max_len_prefix:], new_bottom[max_len_prefix:]),
          state.history+[domino.index]
          )
    else:
      return PostCorrespondenceState()

  def Neighbors(self, state):
    '''
    Generates a sequence of valid neighbors of a given state.
    Args:
      state: (str_top, str_bottom). 
        A valid state should have at least one empty string ("").
    Returns:
      A list of the valid neighbor states.
    '''
    neighbors = [self._CatDomino(state, d) for d in self.dominos]
    return [n for n in neighbors if n.IsValid()]
  
  def Assert(self, state):
    if state.IsValid():
      return state.seqs[0] == state.seqs[1]
    else:
      return False
      
        


class IterativeDeepening():
  def __init__(self, max_queue_size=100, max_states_num=1000):
    self.bfs_queue = []
    self.dfs_stack = []
    self.seen_bfs_states = set()
    self.seen_dfs_states = set()
    self.num_states_seen = 0
    self.max_queue_size = min(max_queue_size, 2**20)
    self.max_states_num = max_states_num
  
  def bfs(self, searchable):
    # Initialize.
    self.bfs_queue.append(searchable.start_point)
    while (
        self.num_states_seen < self.max_states_num and 
        self.bfs_queue):
      u = self.bfs_queue.pop(0)
      # Get unseen neighboring states.
      neighbors = [
          n for n in searchable.Neighbors(u) 
          if n.seqs not in self.seen_bfs_states]
      # If max_queue_size is reached, stop bfs. 
      # Insert u back to the front of the queue.
      if len(neighbors) + len(self.bfs_queue) > self.max_queue_size:
        self.bfs_queue.insert(0, u)
        return None, 2
      # Appending neighbors to the queue.
      for v in neighbors:
        self.num_states_seen += 1
        if self.num_states_seen > self.max_states_num:
          # No solution was found within the limits of search.
          return None, 2
        
        self.seen_bfs_states.add(v.seqs)
        
        if searchable.Assert(v):
          # Solution found.
          return v, 0
        
        self.bfs_queue.append(v)

    if self.bfs_queue:
      return None, 2
    else:
      return None, 1
              
  
  def dfs(self, depth=1):
    pass

  def search(self, searchable):
    '''
    Args:
      searchable: an class object with 
        1. a start_point field as the start point of searching,
        2. a Neighbors(state) method to generate neighboring states, and
        3. a Assert(state) method to evaluate the state.
    Returns:
      (STATE, exit code)
      0 solution found
      1 no solution exists.
      2 no solution was found within the limits of search.
    '''
    v, err = self.bfs(searchable)
    return v, err


def LoadFile(fname=None):
  max_queue_size = None
  max_states_num = None
  dominos = None
  if not os.path.isfile(fname):
    print('Cannot open file: {}.'.format(fname))
  else:
    try:
      with open(fname) as f:
        
          max_queue_size = int(f.next())
          max_states_num = int(f.next())
          dominos = []
          for line in f:
            idx, str_top, str_bottom = line.strip('\n').split(' ')
            dominos.append(Domino(idx, (str_top, str_bottom)))
    except: 
      print('''Incompatible format! \n
    Please follow strictly the sample from the course webpage.
    First line: "\d+" marking max size of queue 
    Second line: "\d+" marking the max total number of states 
    Remaining lines: "\d+ \c+ \c+" marking the Dominos' index and strings''')

  return max_queue_size, max_states_num, dominos


def main():
  if len(sys.argv) == 1:
    print('The program needs an argument indicating the input file!')
    return 
  fname = sys.argv[1]
  max_queue_size, max_states_num, dominos = LoadFile(fname)
  dominos = DominoSpace(dominos=dominos)
  search_engine = IterativeDeepening(
      max_queue_size=max_queue_size,
      max_states_num=max_states_num)
  v, err = search_engine.search(dominos)
  if v:
    print (v.seqs, v.history)
  else:
    print (v, err)

if __name__ == '__main__':
  main()

