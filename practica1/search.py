# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).

Name student 1: ...
Name student 2: ...
IA lab group and pair: gggg - mm

"""

import util
from game import Directions


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(search_problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    #from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(search_problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", search_problem.getStartState())
    print("Is the start a goal?", search_problem.isGoalState(search_problem.getStartState()))
    print("Start's successors:", search_problem.getSuccessors(search_problem.getStartState()))
    """
    structure = util.Stack()

    # structure.push([d[1] for d in search_problem.getSuccessors(search_problem.getStartState())]) # DEFINE THE INITIAL STATE
    for s in search_problem.getSuccessors(search_problem.getStartState()):
        structure.push([s])
        
    visited = []
    # path = structure.pop()
    # print(f"path0 {path}")
    # structure.push(path + path)
    # path = structure.pop()
    # print(f"path1 {path}")
    while not structure.isEmpty():
        path = list(structure.pop())
        current_state =  path[-1][0]# INDEX THE CURRENT STATE
        print(f"path: {path} \ncurrent: {current_state}\n\n----------------------------")
        if search_problem.isGoalState(current_state):
            s = [s[1] for s in path] # RETURN THE PATH OF STATES
            print(f"goalState{s}")
            return s # RETURN THE PATH OF STATES


        if current_state not in visited:
            visited.append(current_state)
            for successor in search_problem.getSuccessors(current_state):
                if successor[0] not in visited:
                    new_path =  path + [successor]# CREATE THE NEW PATH OF STATES
                    structure.push(new_path)

    return None


def breadthFirstSearch(search_problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def uniformCostSearch(search_problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, search_problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(search_problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
