#! /usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import logging
import argparse

from iterative_deepening import BFSnIterativeDeepening, ERR_MESSAGE, Element, State, Searchable


class Domino(Element):
  def __init__(self, index, content):
    super(Domino, self).__init__(index, content)

  def __repr__(self):
    return "{{{}: {}}}".format(self.index, self.content)


class PostCorrespondenceState(State):
  def __init__(self, state=("", ""), history=None):
    super(PostCorrespondenceState, self).__init__(state, history)

  def IsValid(self):
    return True if self.history else False

  def __str__(self):
    return "-".join(["D%d"%d for d in self.history])

  def __repr__(self):
    return "{{{}, {}}}".format(self.state, self.history)


class DominoSpace(Searchable):
  '''
  The class DominoSpace contains
    fields:
      start_point: a PostCorrespondenceState to start with.
        Initialized to state=("", ""), history=[].
      dominos: a list of Domino.
    methods:
      Neighbors(state): generate a list of neighboring states of the
        given state by trying concatenating dominos.
      Assert(state): determine if the STATE meets the goal.
 '''
  def __init__(self, dominos,
               start_point=PostCorrespondenceState(("", ""), [])):
    super(DominoSpace, self).__init__(start_point)
    # self.start_point = start_point
    self.dominos = sorted(dominos, key=lambda d: d.index)

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
    state_top, state_bottom = state.state
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
      state: A valid state should having at least one empty string ("") in state.
    Returns:
      A list of the valid neighbor states.
    '''
    neighbors = [self._CatDomino(state, d) for d in self.dominos]
    return [n for n in neighbors if n.IsValid()]

  def Assert(self, state):
    '''
    Assert if the given state meets the goal.
    '''
    if state.IsValid():
      return state.state[0] == state.state[1]
    else:
      return False

  def Replay(self, state):
    '''
    Return the sequence of states towards the finding of the given state
    in chronological order.

    Args:
      state: The state object to whose history is to be replayed.
    Return:
      A list of states towards the finding of the given state
    organized in chronological order.
    '''
    final = state.history
    start = self.start_point.history
    final = final[len(start):]

    index_to_domino = {d.index: d for d in self.dominos}
    states = [self.start_point]
    for state in final:
      states.append(self._CatDomino(states[-1], index_to_domino[state]))
    return states


def LoadFile(fname=None):
  '''
  Args:
    fname: The file name.
  Returns:
    max_queue_size: The maximum queue size for BFS.
    max_states_num: The maximum number of states to explore.
    dominos: A list of Domino object.
  '''
  max_queue_size = None
  max_states_num = None
  dominos = None
  if not os.path.isfile(fname):
    print('Cannot open file: {}.'.format(fname))
    exit()
  else:
    try:
      with open(fname) as fin:
        max_queue_size = int(fin.next())
        max_states_num = int(fin.next())
        dominos = []
        for line in fin:
          idx, str_top, str_bottom = line.strip('\n').split(' ')
          dominos.append(Domino(int(idx), (str_top, str_bottom)))
    except:
      print(r'''Incompatible format!
    
    Please follow strictly the sample from the course webpage.
    First line: "\d+" marking max size of queue
    Second line: "\d+" marking the max total number of states
    Remaining lines: "\d+ \w+ \w+" marking the Dominos' index and strings''')
      exit()

  return max_queue_size, max_states_num, dominos


def main():
  parser = argparse.ArgumentParser(
      description=("Using BFS with Iterative Deepening to solve "
                  "the post correspondence problem of dominos."))
  parser.add_argument("FILE", type=str, help="Input file name.")
  parser.add_argument("-d", "--debug", action="store_true",
                      help="show all the debug logging infomation.")
  parser.add_argument("-v", "--verbose", action="store_true",
                      help="track the state changes towards the solution.")

  args = parser.parse_args()
  if args.debug:
    logging.getLogger().setLevel(logging.INFO)


  if len(sys.argv) == 1:
    print('The program needs an argument indicating the input file!')
    return
  fname = sys.argv[1]
  max_queue_size, max_states_num, dominos = LoadFile(fname)
  dominos = DominoSpace(dominos=dominos)
  solver = BFSnIterativeDeepening(
      dominos,
      max_queue_size=max_queue_size,
      max_states_num=max_states_num)
  sol, err = solver.Search()
  print(ERR_MESSAGE[err])
  if sol:
    print("Solution:\n\t%s"%sol)
  if args.verbose and sol:
    print("Path towards solution state:\n\t", end="")
    path_to_sol = dominos.Replay(sol)
    print(" => ".join(["{}".format(s.state) for s in path_to_sol]))
  if args.verbose:
    all_states = solver.seen_bfs_states.keys() + solver.seen_dfs_states.keys()
    print("All %d states explored:\n\t"%len(all_states), end="")
    print(" ".join(["{}".format(s) for s in all_states]))

  else:
    logging.info("%r, %r", sol, err)


if __name__ == '__main__':
  main()
