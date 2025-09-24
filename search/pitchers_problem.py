# pitchers.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
# This pitchers project was developed by Bikramjit Banerjee @ USM.

import search
import random

# Module Classes

class PitchersState:
 """
 This class defines the mechanics of the puzzle itself.  The
 task of recasting this puzzle as a search problem is left to
 the PitchersPuzzleSearchProblem class.
 """

 def __init__( self, numbers ):
   """
     Constructs a new pitchers puzzle from an ordered list of numbers.

   numbers: a list of integers containing the goal(in gallons), and the
   capacities of the pitchers and their initial contents, also in gallons.
   Thus, the list should contain:

       [goal, cap_1, ..., cap_n, con_1, ..., con_n]
   """
   
   numbers = numbers[:] # Make a copy so as not to cause side-effects.
   self.goal = numbers[0]
   num_pitchers = (len(numbers) - 1) // 2
   self.capacities = numbers[ 1 : num_pitchers + 1 ]
   self.contents = numbers[ num_pitchers + 1 : ]

 def isGoal( self ):
   """
   >>> PitchersState([1, 3, 8, 12, 0, 0, 0]).isGoal()
   False ##It's the initial state!
   """
   for x in self.contents:
    if x==self.goal:
     return True
   return False

 def legalMoves( self ):
   """
     Returns a list of legal moves from the current state.
   e:i         Means empty pitcher i
   f:i         Means fill pitcher i
   p:i:j       Means pour pitcher i to j
   >>> PitchersState([1, 3, 8, 12, 0, 0, 0]).legalMoves()
   ['f:0', 'f:1', 'f:2']
   """
   moves = []
   for i in range(len(self.contents)):
    con_i = self.contents[i]
    cap_i = self.capacities[i]
    if con_i > 0:
     moves.append('e:'+str(i))
    if con_i < cap_i:
     moves.append('f:'+str(i))
   for i in range(len(self.contents)):
    for j in range(len(self.contents)):
     if i==j:
      continue
     con_i = self.contents[i]
     con_j = self.contents[j]
     cap_j = self.capacities[j]
     if (con_i > 0) and (con_j < cap_j):
      moves.append('p:'+str(i)+':'+str(j))
   return moves

 def result(self, move):
   """
     Returns a new PitchersState with the current state 
   updated based on the provided move. E.g., applying 'p:1:0'
   to state [1,2,3,0,3] should result in state [1,2,3,2,1].

   The move should be a string drawn from a list returned by legalMoves.
   Therefore you may assume that the input move is legal.
   
   NOTE: This function *does not* change the current object.  Instead,
   it returns a new object, return_state
   """
   return_state = PitchersState([self.goal] + list(self.capacities + self.contents))
   "*** YOUR CODE HERE ***"
   return return_state

 # Utilities for comparison and display
 def __eq__(self, other):
   """
       Overloads '==' such that two PitchersPuzzles with the same configuration
     are equal.
   """
   if (self.goal == other.goal) and \
      (self.contents == other.contents) and \
      (self.capacities == other.capacities):
    return True
   else:
    return False

 def __hash__(self):
   return hash(str([self.goal] + list(self.capacities + self.contents)))

 def __getAsciiString(self):
   return str([self.goal] + list(self.capacities + self.contents))+'\n'

 def __str__(self):
   return self.__getAsciiString()


class PitchersPuzzleSearchProblem(search.SearchProblem):
  """
    Implementation of a SearchProblem for the Pitchers domain
    Each state is represented by an instance of Pitchers.
  """
  def __init__(self,puzzle):
    "Creates a new PitchersPuzzleSearchProblem which stores search information."
    self.puzzle = puzzle

  def getStartState(self):
    return self.puzzle
      
  def isGoalState(self,state):
    return state.isGoal()
   
  def getSuccessors(self,state):
    """
      Returns a list of (successor, action, stepCost) tuples where
      each succesor is the result of applying action to state
      and the cost is 1.0 for each
    """
    succ = []
    for a in state.legalMoves():
      succ.append((state.result(a), a, 1))
    return succ

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions. The sequence must
     be composed of legal moves
     """
     return len(actions)

#Below are a few random instances of the pitchers puzzle
PITCHERS_PUZZLE_DATA = [[4, 5, 3, 0, 0], 
                     [2, 7, 3, 0, 0],
                     [4, 7, 3, 0, 0],
                     [1, 2, 5, 10, 0, 0, 0],
                     [1, 3, 8, 12, 0, 0, 0]]

def loadPitchersPuzzle(puzzleNumber):
  """
    puzzleNumber: The number of the pitchers puzzle to load.
    
    Returns a puzzle object generated from one of the
    provided puzzles in PITCHERS_PUZZLE_DATA.
    
    puzzleNumber can range from 0 to ...
  """
  return PitchersState(PITCHERS_PUZZLE_DATA[puzzleNumber])

if __name__ == '__main__':
  puzzle = loadPitchersPuzzle(random.choice(range(len(PITCHERS_PUZZLE_DATA))))
  print('A random puzzle:')
  print(puzzle)
  
  problem = PitchersPuzzleSearchProblem(puzzle)
  path = search.breadthFirstSearch(problem)
  print('BFS found a path of %d moves: %s' % (len(path), str(path)))
  curr = puzzle
  i = 1
  for a in path:
    print("Allowed moves: ", curr.legalMoves())
    curr = curr.result(a)
    print('Selected move: %s. After %d move%s the state is' % (a, i, ("", "s")[i>1]))
    print(curr)
    
    input("Press return for the next state...")   # wait for key stroke
    i += 1
