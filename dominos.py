#! /usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import logging
import argparse

from iterative_deepening import BFSnIterativeDeepening

parser = argparse.ArgumentParser(
    description=("Using BFS with Iterative Deepening to solve "
                 "the post correspondence problem of dominos."))
parser.add_argument("FILE", type=str, help="Input file name.")
parser.add_argument("-v","--verbose", action="store_true",
    help="show all the logging infomation.")
parser.add_argument("-t","--track", action="store_true",
    help="track the state changes towards the solution.")

args = parser.parse_args()
if args.verbose:
  logging.getLogger().setLevel(logging.INFO)


class Domino:
  def __init__(self, index, content):
    self.index = index
    self.content = content
  
  def __repr__(self):
    return "{{{}: {}}}".format(self.index, self.content)


class PostCorrespondenceState:
  def __init__(self, seqs=("", ""), history=None):
    self.seqs = seqs
    self.history = history or []
  
  def IsValid(self):
    return True if self.history else False

  def __repr__(self):
    return "{{{}, {}}}".format(self.seqs, self.history)


class DominoSpace:
  '''
  The class DominoSpace contains 
    fields:
      start_point: a PostCorrespondenceState to start with. 
        Initialized to seqs=("", ""), history=[].
      dominos: a list of Domino.
    methods:
      Neighbors(state): generate a list of neighboring states of the 
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
      Otherwise return an invalid state.
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
      state: A valid state should having at least one empty string ("") in seqs.
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
    Remaining lines: "\d+ \w+ \w+" marking the Dominos' index and strings''')

  return max_queue_size, max_states_num, dominos


def main():
  if len(sys.argv) == 1:
    ('The program needs an argument indicating the input file!')
    return 
  fname = sys.argv[1]
  max_queue_size, max_states_num, dominos = LoadFile(fname)
  dominos = DominoSpace(dominos=dominos)
  search_engine = BFSnIterativeDeepening(
      dominos,
      max_queue_size=max_queue_size,
      max_states_num=max_states_num)
  v, err = search_engine.Search()
  if v:
    logging.info("%r, %r"%(v.seqs, v.history))
  else:
    logging.info("%r, %r"%(v, err))

if __name__ == '__main__':
  main()