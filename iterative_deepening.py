#! /usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging

ERR_MESSAGE = {
    0: "Solution found!",
    1: "NO SOLUTION for the problem.",
    2: "No solution found WITHIN GIVEN CONSTRAINS."
}


class Element(object):
  def __init__(self, index, content):
    self.index = index
    self.content = content


class State(object):
  def __init__(self, state=("", ""), history=None):
    self.state = state
    self.history = history

  def IsValid(self):
    raise NotImplementedError()


class Searchable(object):
  def __init__(self, start_point=None):
    self.start_point = start_point

  def Neighbors(self, state):
    raise NotImplementedError()

  def Assert(self, state):
    raise NotImplementedError()


class BFSnIterativeDeepening(object):
  '''
  This is a generic class for BFS with Iterative Deepening.

  It search on a Searchalbe object. Searchable objects should have
  field:
    start_point:
      An State object with
        fields:
          state:     The state.
          history:  The path lead to the state from the state point.
        method:
          IsValid(state): Assert if the state is valid.
  methods:
    Neighbors(state): Generate the neighboring states.
    Assert(state):    Assert if the state meets the goal.
  '''
  def __init__(self, searchable, max_queue_size=100, max_states_num=1000):
    '''
    Args:
      searchable:     The Searchable object.
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

  def BFS(self):
    '''
    This function conducts BFS from the self.searchable.start_point
    with a constraint in the maximum size of the queue and the maximum
    number of states. It will then return the result and error code.

    Returns:
      sol: The solution state. If not found, None is returned.
      err: Exit code
        0 - sulution found;
        1 - no soluion exists within the depth of the search;
        2 - solution not found within the maximum number of states.
    '''
    # Initialize.
    self.bfs_queue.append(self.searchable.start_point)
    while (
        self.num_states_seen < self.max_states_num and
        self.bfs_queue):
      logging.info("bfs queue: %s", self.bfs_queue)
      node = self.bfs_queue.pop(0)
      # Get unseen neighboring states.
      neighbors = self._GetNewNeighbors(node)
      # If max_queue_size is reached, stop bfs.
      # Insert u back to the front of the queue.
      if len(neighbors) + len(self.bfs_queue) > self.max_queue_size:
        self.bfs_queue.insert(0, node)
        return None, 2
      for neighbor in neighbors:
        self.num_states_seen += 1
        if self.num_states_seen > self.max_states_num:
          # No solution was found within the limits of search.
          return None, 2
        self.seen_bfs_states[neighbor.state] = neighbor.history
        if self.searchable.Assert(neighbor):
          # Solution found.
          return neighbor, 0
        self.bfs_queue.append(neighbor)
    if self.bfs_queue:
      return None, 2
    else:
      return None, 1

  def DFS(self, root, max_depth):
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

  def IterativeDeepening(self):
    '''
    This function repeatively call DFS (with constraint on depth and
    maximum number of states), iterating over every element in
    self.bfs_queue as root. It returns the result and error code when
    the constraint on the number of states is met, or when no new
    state is to be discovered.

    Returns:
      sol: The solution state. If not found, None is returned.
      err: Exit code
        0 - sulution found;
        1 - no soluion exists;
        2 - solution not found within the maximum number of states.
    '''
    iterate_depth = 0
    num_states_before = self.num_states_seen
    while self.num_states_seen < self.max_states_num:
      iterate_depth += 1
      logging.info("Iteration deptp = %d", iterate_depth)
      for root in self.bfs_queue:
        sol, err = self.DFS(root, iterate_depth)
        logging.info("dfs return: %r, %r", sol, err)
        logging.info("States: %r/%r", self.num_states_seen, self.max_states_num)
        if err != 0:
          continue
        else:
          return sol, err
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
