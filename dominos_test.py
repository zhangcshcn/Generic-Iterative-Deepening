#! /usr/bin/python2
# -*- coding: utf-8 -*-
import unittest
from dominos import Domino, PostCorrespondenceState, DominoSpace

class PostCorrespondenceStateTest(unittest.TestCase):
  def testIsValid(self):
    states = [
        PostCorrespondenceState(),
        PostCorrespondenceState(("a", ""), []),
        PostCorrespondenceState(("a", "b"), []),
        PostCorrespondenceState(("", "b"), []),
        PostCorrespondenceState(("", ""), [1]),
        PostCorrespondenceState(("a", ""), [1]),
        PostCorrespondenceState(("a", "b"), [1]),
        PostCorrespondenceState(("", "b"), [1]),
        PostCorrespondenceState(("", ""), [1, 2]),
        PostCorrespondenceState(("a", ""), [1, 2]),
        PostCorrespondenceState(("a", "b"), [1, 2]),
        PostCorrespondenceState(("", "b"), [1, 2]),
    ]
    expected = [
        False, False, False, False,
        True, True, True, True,
        True, True, True, True,
    ]
    test_result = [s.IsValid() for s in states]
    self.assertEqual(expected, test_result)


class DominoSpaceTest(unittest.TestCase):
  def setUp(self):
    self.domino_space = DominoSpace(
        dominos=[
            Domino(1, ("c", "cca")), Domino(2, ("ac", "ba")),
            Domino(3, ("bb", "b")), Domino(4, ("ac", "cb")),
        ]
    )

  def testCatDomino(self):
    states = [
        PostCorrespondenceState(("", ""), []),
        PostCorrespondenceState(("a", ""), [1]),
        PostCorrespondenceState(("", "a"), [2]),
        PostCorrespondenceState(("ab", ""), [3]),
    ]
    dominos = [
        [Domino(1, ("", "")), Domino(2, ("b", "ab")),
         Domino(3, ("ab", "b")), Domino(4, ("", "ab"))], # excat match
        [Domino(1, ("ab", "a")), Domino(2, ("b", "a")),
         Domino(3, ("abc", "b")), Domino(4, ("cd", "abc"))],
        [Domino(1, ("ab", "abc")), Domino(2, ("b", "abc")),
         Domino(3, ("a", "b")), Domino(4, ("c", "abcd"))],
        [Domino(1, ("ab", "bb")), Domino(2, ("cd", "bc")),
         Domino(3, ("bc", "bc")), Domino(4, ("cd", "cdef"))], # Miss match
    ]
    expected = [
        [
            PostCorrespondenceState(("", ""), [1]),
            PostCorrespondenceState(("", ""), [1, 2]),
            PostCorrespondenceState(("", ""), [2, 3]),
            PostCorrespondenceState(("", ""), [3, 4])],
        [
            PostCorrespondenceState(("b", ""), [1]),
            PostCorrespondenceState(("b", ""), [1, 2]),
            PostCorrespondenceState(("c", ""), [2, 3]),
            PostCorrespondenceState(("d", ""), [3, 4])],
        [
            PostCorrespondenceState(("", "c"), [1]),
            PostCorrespondenceState(("", "c"), [1, 2]),
            PostCorrespondenceState(("", "b"), [2, 3]),
            PostCorrespondenceState(("", "d"), [3, 4])],
        [
            PostCorrespondenceState(),
            PostCorrespondenceState(),
            PostCorrespondenceState(),
            PostCorrespondenceState()],
    ]
    for idx, test_dominos in enumerate(dominos):
      test_result = map(DominoSpace._CatDomino, states, test_dominos)
      self.assertSequenceEqual(
          [x.state for x in expected[idx]], [x.state for x in test_result])
      self.assertSequenceEqual(
          [x.history for x in expected[idx]], [x.history for x in test_result])

  def testNeighbors(self):
    states = [
        PostCorrespondenceState(("", ""), []),
        PostCorrespondenceState(("", "ca"), [1]),
        PostCorrespondenceState(("b", ""), [3]),
        PostCorrespondenceState(("c", ""), [3, 2]),
        PostCorrespondenceState(("", "a"), [3, 2, 1]),
        PostCorrespondenceState(("", "b"), [3, 2, 1, 4])
    ]
    expected = [
        [PostCorrespondenceState(("", "ca"), [1]),
         PostCorrespondenceState(("b", ""), [3])],
        [PostCorrespondenceState(("", "acca"), [1, 1])],
        [PostCorrespondenceState(("c", ""), [3, 2]),
         PostCorrespondenceState(("bb", ""), [3, 3])],
        [PostCorrespondenceState(("", "a"), [3, 2, 1])],
        [PostCorrespondenceState(("", "b"), [3, 2, 1, 4])],
        [PostCorrespondenceState(("", ""), [3, 2, 1, 4, 3])],
    ]
    for idx, state in enumerate(states):
      test_result = self.domino_space.Neighbors(state)
      self.assertSequenceEqual(
          [x.state for x in expected[idx]], [x.state for x in test_result])
      self.assertSequenceEqual(
          [x.history for x in expected[idx]], [x.history for x in test_result])

  def testAssert(self):
    states = [
        PostCorrespondenceState(("", ""), [1]),
        PostCorrespondenceState(("", "a"), [1]),
        PostCorrespondenceState(("a", ""), [1]),
        PostCorrespondenceState(("a", "a"), [1]),
        PostCorrespondenceState(("b", "a"), [1]),
        PostCorrespondenceState(("ab", "a"), [1]),
        PostCorrespondenceState(("a", "ab"), [1])
    ]
    expected = [
        True, False, False, True, False, False, False
    ]
    test_result = [self.domino_space.Assert(s) for s in states]
    self.assertSequenceEqual(expected, test_result)

  def testDominoFunctional(self):
    expected = [
        PostCorrespondenceState(("", "ca"), [1]),
        PostCorrespondenceState(("b", ""), [3])]
    test_result = self.domino_space.Neighbors(self.domino_space.start_point)
    self.assertSequenceEqual(
        [x.state for x in expected], [x.state for x in test_result])
    self.assertSequenceEqual(
        [x.history for x in expected], [x.history for x in test_result])


if __name__ == "__main__":
  unittest.main()
