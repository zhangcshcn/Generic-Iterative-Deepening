import unittest
import DominosID

class DominoTest(unittest.TestCase):
  def setUp(self):
    self.Dominos = DominosID.Dominos(
      dominos=[
        (1, ("c", "cca")),(2, ("ac", "ba")),
        (3, ("bb", "b")),(4, ("ac", "cb")),]
    )
  
  def testCatDomino(self):
    states = [
      (("", ""),[]), (("a", ""),[1]), (("", "a"),[2]), (("ab", ""),[3]),
    ]
    dominos = [
      [(1, ("", "")),(2, ("b", "ab")),(3, ("ab", "b")),(4, ("", "ab"))],# excat match
      [(1, ("ab", "a")),(2, ("b", "a")),(3, ("abc", "b")),(4, ("cd", "abc"))],
      [(1, ("ab", "abc")),(2, ("b", "abc")),(3, ("a", "b")),(4, ("c", "abcd"))],
      [(1, ("ab", "bb")),(2, ("cd", "bc")),(3, ("bc", "bc")),(4, ("cd", "cdef"))],  # Miss match
    ]
    expected = [
      [(("", ""),[1]), (("", ""),[1, 2]), (("", ""),[2, 3]), (("", ""),[3, 4])],
      [(("b", ""),[1]), (("b", ""),[1, 2]), (("c", ""),[2, 3]), (("d", ""),[3, 4])],
      [(("", "c"),[1]), (("", "c"),[1, 2]), (("", "b"),[2, 3]), (("", "d"),[3, 4])],
      [None, None, None, None],
    ]
    for idx, test_dominos in enumerate(dominos):
      test_result = map(self.Dominos._CatDomino, states, test_dominos)
      self.assertSequenceEqual(expected[idx], test_result)

  def testNeighbors(self):
    states = [
      (("", ""),[]),(("", "ca"),[1]),(("b", ""),[3]), (("c", ""),[3, 2]), 
      (("", "a"),[3, 2, 1]), (("", "b"),[3, 2, 1, 4])
    ]
    expected = [
      [(("", "ca"),[1]), (("b", ""),[3])],
      [(("", "acca"),[1, 1])],
      [(("c", ""),[3, 2]), (("bb", ""),[3, 3])],
      [(("", "a"),[3, 2, 1])],
      [(("", "b"),[3, 2, 1, 4])],
      [(("", ""),[3, 2, 1, 4, 3])],
    ]
    for idx, state in enumerate(states):
      test_result = self.Dominos.Neighbors(state)
      self.assertSequenceEqual(expected[idx], test_result)

  def testAssert(self):
    states = [
      (("", ""),[]), (("", "a"),[]), (("a", ""),[]), (("a", "a"),[]), 
      (("b", "a"),[]), (("ab", "a"),[]), (("a", "ab"),[])
    ]
    expected = [
      True, False, False, True, False, False, False 
    ]
    test_result = [self.Dominos.Assert(s) for s in states]
    self.assertSequenceEqual(expected, test_result)

  def testDominoFunctional(self):
    expected = [(("", "ca"),[1]), (("b", ""),[3])]
    test_result = self.Dominos.Neighbors(self.Dominos.start_point)
    self.assertSequenceEqual(expected, test_result)

class IterativeDeepeningTest(unittest.TestCase):
  def setUp():
    pass
  
if __name__ == "__main__":
  unittest.main()