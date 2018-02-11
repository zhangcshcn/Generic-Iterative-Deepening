#! /usr/bin/python2
# -*- coding: utf-8 -*-
import unittest
from iterative_deepening import State, Searchable, IterativeDeepening


class TreeNode(object):
  def __init__(self, val=0):
    self.val = val
    self.left = None
    self.right = None


class TreeState(State):
  def __init__(self, state, history=None):
    super(TreeState, self).__init__(state, history)


class TreeSpace(Searchable):
  def __init__(self, root, target=0):
    super(TreeSpace, self).__init__(root)
    self.target = target

  def Neighbors(self, state):
    res = []
    if state.state.left:
      res.append(TreeState(state.state.left))
    if state.state.right:
      res.append(TreeState(state.state.right))
    return res

  def Assert(self, state):
    return state is not None and state.state.val == self.target

class TreeTest(unittest.TestCase):
  def setUp(self):
    self.root = TreeNode(0)
    queue = [self.root]
    for i in xrange(7):
      node = queue.pop(0)
      node.left = TreeNode(2*i + 1)
      node.right = TreeNode(2*i + 2)
      queue += [node.left, node.right]

  def testBFSErr0(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=8,
        max_states_num=16)
    sol, err = solver.BFS()
    self.assertEqual(target, sol.state.val)
    self.assertEqual(0, err)
    self.assertSequenceEqual(
        [5, 6, 7, 8, 9],
        [i.state.val for i in solver.bfs_queue])
    self.assertEqual(10, solver.num_states_seen)

  def testBFSErr1(self):
    target = 17
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=8,
        max_states_num=16)
    sol, err = solver.BFS()
    self.assertEqual(None, sol)
    self.assertEqual(1, err)
    self.assertSequenceEqual([], [i.state.val for i in solver.bfs_queue])
    self.assertEqual(14, solver.num_states_seen)

  def testBFSErr2A(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=2,
        max_states_num=16)
    sol, err = solver.BFS()
    self.assertEqual(None, sol)
    self.assertEqual(2, err)
    self.assertSequenceEqual([1, 2], [i.state.val for i in solver.bfs_queue])
    self.assertEqual(2, solver.num_states_seen)

  def testBFSErr2B(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=8,
        max_states_num=9)
    sol, err = solver.BFS()
    self.assertEqual(None, sol)
    self.assertEqual(2, err)
    self.assertSequenceEqual(
        [5, 6, 7, 8, 9],
        [i.state.val for i in solver.bfs_queue])
    self.assertEqual(9, solver.num_states_seen)

  def testDFSErr0A(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=8,
        max_states_num=16)
    sol, err = solver.DFS(tree_space.start_point)
    self.assertEqual(target, sol.state.val)
    self.assertEqual(0, err)
    self.assertEqual(8, solver.num_states_seen)

  def testDFSErr0B(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(tree_space)
    sol, err = solver.DFS(tree_space.start_point, 3)
    self.assertEqual(target, sol.state.val)
    self.assertEqual(0, err)
    self.assertEqual(8, solver.num_states_seen)

  def testDFSErr1A(self):
    target = 17
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(tree_space)
    sol, err = solver.DFS(tree_space.start_point)
    self.assertEqual(None, sol)
    self.assertEqual(1, err)
    self.assertEqual(14, solver.num_states_seen)

  def testDFSErr1B(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(tree_space)
    sol, err = solver.DFS(tree_space.start_point, 2)
    self.assertEqual(None, sol)
    self.assertEqual(1, err)
    self.assertEqual(6, solver.num_states_seen)


  def testDFSErr2(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space, max_states_num=7)
    sol, err = solver.DFS(tree_space.start_point)
    self.assertEqual(None, sol)
    self.assertEqual(2, err)
    self.assertEqual(7, solver.num_states_seen)

  def testIterativeDeepeningErr0(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space, max_states_num=10)
    sol, err = solver.IterativeDeepening([tree_space.start_point])
    self.assertEqual(target, sol.state.val)
    self.assertEqual(0, err)
    self.assertEqual(10, solver.num_states_seen)

  def testIterativeDeepeningErr1(self):
    target = 16
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space, max_states_num=16)
    sol, err = solver.IterativeDeepening([tree_space.start_point])
    self.assertEqual(None, sol)
    self.assertEqual(1, err)
    self.assertEqual(14, solver.num_states_seen)

  def testIterativeDeepeningErr2(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space, max_states_num=9)
    sol, err = solver.IterativeDeepening([tree_space.start_point])
    self.assertEqual(None, sol)
    self.assertEqual(2, err)
    self.assertEqual(9, solver.num_states_seen)

  def testSearchErr0A(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=3,
        max_states_num=16)
    sol, err = solver.Search()
    self.assertEqual(target, sol.state.val)
    self.assertEqual(0, err)
    self.assertSequenceEqual([2, 3, 4], [i.state.val for i in solver.bfs_queue])
    self.assertEqual(10, solver.num_states_seen)

  def testSearchErr0B(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=8,
        max_states_num=16)
    sol, err = solver.Search()
    self.assertEqual(target, sol.state.val)
    self.assertEqual(0, err)
    self.assertSequenceEqual([5, 6, 7, 8, 9], [i.state.val for i in solver.bfs_queue])
    self.assertEqual(10, solver.num_states_seen)

  def testSearchErr0C(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=0,
        max_states_num=16)
    sol, err = solver.Search()
    self.assertEqual(target, sol.state.val)
    self.assertEqual(0, err)
    self.assertSequenceEqual([0], [i.state.val for i in solver.bfs_queue])
    self.assertEqual(10, solver.num_states_seen)

  def testSearchErr0D(self):
    target = 10
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=1,
        max_states_num=16)
    sol, err = solver.Search()
    self.assertEqual(target, sol.state.val)
    self.assertEqual(0, err)
    self.assertSequenceEqual([0], [i.state.val for i in solver.bfs_queue])
    self.assertEqual(10, solver.num_states_seen)

  def testSearchErr1(self):
    target = 17
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=3,
        max_states_num=16)
    sol, err = solver.Search()
    self.assertEqual(None, sol)
    self.assertEqual(1, err)
    self.assertSequenceEqual([2, 3, 4], [i.state.val for i in solver.bfs_queue])
    self.assertEqual(14, solver.num_states_seen)

  def testSearchErr2(self):
    target = 17
    tree_space = TreeSpace(TreeState(self.root), target)
    solver = IterativeDeepening(
        tree_space,
        max_queue_size=3,
        max_states_num=9)
    sol, err = solver.Search()
    self.assertEqual(None, sol)
    self.assertEqual(2, err)
    self.assertSequenceEqual([2, 3, 4], [i.state.val for i in solver.bfs_queue])
    self.assertEqual(9, solver.num_states_seen)


if __name__ == "__main__":
  unittest.main()
