#! /usr/bin/python2
# -*- coding: utf-8 -*-
'''
This module implements a generic framework for Iterative Deepening.
The class IterativeDeepening is implemented. The maximum number
of bfs queue, and the maximum number of states to explore are freely
customizable. The generic and end-to-end method of Search is provided.
The components, namely, BFS, DFS, and IterativeDeepening methods with
customizable seed(s) also provide.

In accord with the generic search framework, the abstract classes as
wrappers of customized states, and search space are also provided.
It is trivil to adjust customized search problem in to the framework
provided here.
'''

from __future__ import print_function
import logging

ERR_MESSAGE = {
    0: "Solution found!",
    1: "NO SOLUTION for the problem.",
    2: "No solution found WITHIN GIVEN CONSTRAINS."
}


class State(object):
  '''
  Abstract class for the states and its history in the search space.
  '''
  def __init__(self, state=None, history=None):
    self.state = state
    self.history = history


class Searchable(object):
  '''
  Abstract class for the search space.
  '''
  def __init__(self, start_point=None):
    self.start_point = start_point

  def Neighbors(self, state):
    '''
    Generates the neighbors of the given state in the search space.

    Args:
      state: The State object whose neighbors are to be returned.
    Return:
      A list of State objects.
    '''
    raise NotImplementedError()

  def Assert(self, state):
    '''
    Assert if a given state satisfies the terminating condition.

    Args:
      state: The State Object to be asserted.
    Return:
      bool
    '''
    raise NotImplementedError()


class IterativeDeepening(object):
  '''
  This is a generic class for BFS with Iterative Deepening.

  It search on a Searchalbe object. Searchable objects should have
  field:
    start_point:  An State object marking the start point of the search.
  methods:
    Neighbors(state): Generate the neighboring states.
    Assert(state):    Assert if the state meets the goal.
  '''
  def __init__(self, searchable, max_queue_size=100, max_states_num=1000):
    '''
    Args:
      searchable:     The Searchable object representing the search space.
      max_queue_size: The maximum size of the queue maintained during BFS.
      max_states_num: The maximum number of states to be explored.
    '''
    self.searchable = searchable
    self.bfs_queue = []
    # In iterative deepening, the depth of the dfs calls gradually
    # increases. Elements that are previously visited will for sure
    # be revisited. Whereas for elements visited in the BFS stage,
    # the program should never touch them. There is clearly a need
    # to tell the elements visited during BFS from those during DFS.
    self.seen_bfs_states = {}
    self.seen_dfs_states = {}
    self.num_states_seen = 0
    self.max_queue_size = min(max_queue_size, 2**20)
    self.max_states_num = max_states_num

  def _GetNewNeighbors(self, state):
    return [
        neighbor for neighbor in self.searchable.Neighbors(state)
        if neighbor.state not in self.seen_bfs_states]

  def BFS(self, seed=None, max_queue_size=None):
    '''
    Args:
      seed: A State object to start with. Default to
        self.searchable.start_point.
      max_queue_size: Maximum size of the queue maintained during
        BFS. Default to self.max_queue_size.
    Returns:
      sol: The solution state. If not found, None is returned.
      err: Exit code
        0 - sulution found;
        1 - no soluion exists within the depth of the search;
        2 - solution not found within the maximum number of states.
    '''
    # Initialize.
    max_queue_size = None or self.max_queue_size
    seed_state = seed or self.searchable.start_point
    self.bfs_queue.append(seed_state)
    while (
        self.num_states_seen < self.max_states_num and
        self.bfs_queue):
      logging.info("bfs queue: %s", self.bfs_queue)
      node = self.bfs_queue.pop(0)
      # Get unseen neighboring states.
      neighbors = self._GetNewNeighbors(node)
      # If max_queue_size is reached, stop bfs.
      # Insert node back to the front of the queue.
      if len(neighbors) + len(self.bfs_queue) > max_queue_size:
        self.bfs_queue.insert(0, node)
        return None, 2
      for neighbor in neighbors:
        if self.num_states_seen >= self.max_states_num:
          # No solution was found within the limits of search.
          return None, 2
        self.num_states_seen += 1
        self.seen_bfs_states[neighbor.state] = neighbor.history
        if self.searchable.Assert(neighbor):
          # Solution found.
          return neighbor, 0
        self.bfs_queue.append(neighbor)
    if self.bfs_queue:
      return None, 2
    else:
      return None, 1

  def DFS(self, root, max_depth=1000):
    '''
    Args:
      root: The root of the DFS.
      max_depth: Maximum depth of the DFS.
    Returns:
      sol: The solution state. If not found, None is returned.
      err: Exit code
        0 - sulution found;
        1 - no soluion exists within the depth of the search;
        2 - solution not found within the maximum number of states.
    '''
    # Initialization.
    neighbors = self._GetNewNeighbors(root)
    for neighbor in neighbors:
      if neighbor.state not in self.seen_dfs_states:
        if self.num_states_seen >= self.max_states_num:
          return None, 2
        self.num_states_seen += 1
        self.seen_dfs_states[neighbor.state] = neighbor.history
        if self.searchable.Assert(neighbor):
          return neighbor, 0
    dfs_stack = [(root, 1, neighbors)]
    # Iteration-based DFS with constraint on depth.
    while dfs_stack:
      logging.info("dfs stack: %s", dfs_stack)
      if not dfs_stack[-1][2]:
        # All neighbors visited. Finshed with the last element.
        dfs_stack.pop(-1)
        continue
      depth = dfs_stack[-1][1]
      if depth >= max_depth:
        # Deep enough. No need to explore the neighbors.
        dfs_stack.pop(-1)
        continue
      # Get an element. Explore its neihgbors.
      node = dfs_stack[-1][2].pop(0)
      neighbors = self._GetNewNeighbors(node)
      if not neighbors:
        continue
      for neighbor in neighbors:
        if neighbor.state not in self.seen_dfs_states:
          if self.num_states_seen >= self.max_states_num:
            return None, 2
          self.num_states_seen += 1
          self.seen_dfs_states[neighbor.state] = neighbor.history
          if self.searchable.Assert(neighbor):
            return neighbor, 0
      dfs_stack.append((node, depth+1, neighbors))
    return None, 1

  def IterativeDeepening(self, seeds=None):
    '''
    This function repeatively call DFS (with constraint on depth and
    maximum number of states), iterating over every element in seeds
    self.bfs_queue as root. It returns the result and error code when
    the constraint on the number of states is met, or when no new
    state is to be discovered.

    Args:
      seeds: A list of State objects to start with. Default to
        self.bfs_queue.
    Returns:
      sol: The solution state. If not found, None is returned.
      err: Exit code
        0 - sulution found;
        1 - no soluion exists;
        2 - solution not found within the maximum number of states.
    '''
    iterate_depth = 0
    num_states_before = self.num_states_seen
    seed_list = seeds or self.bfs_queue
    while True:
      iterate_depth += 1
      logging.info("Iteration deptp = %d", iterate_depth)
      for seed in seed_list:
        sol, err = self.DFS(seed, iterate_depth)
        logging.info("dfs return: %r, %r", sol, err)
        logging.info("States: %r/%r", self.num_states_seen, self.max_states_num)
        if sol:
          return sol, err
        if self.num_states_seen >= self.max_states_num:
          return None, 2

      if num_states_before == self.num_states_seen:
        # If no new states is seen in an iteration, no more will show up.
        # There is therefore no solution.
        return None, 1
      else:
        num_states_before = self.num_states_seen

    return None, 2

  def Search(self):
    '''
    This function first call BFS (with constraint on maximum queue size
    and maximum number of states). If necessary, it will then call
    IterativeDeepening (with constraint on maximum number of states).
    It will then return the result and error code.

    Returns:
      sol: The solution state. If not found, None is returned.
      err: Exit code
        0 - sulution found;
        1 - no soluion exists;
        2 - solution not found within the constraints.
    '''
    sol, err = self.BFS()
    logging.info(self.bfs_queue)
    logging.info("States: %r/%r", self.num_states_seen, self.max_states_num)
    if err != 2:
      # Solution found or no solution exist after BFS. No need for DFS.
      return sol, err
    else:
      sol, err = self.IterativeDeepening()
      return sol, err
