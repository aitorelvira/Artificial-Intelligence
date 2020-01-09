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
"""

import util

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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"   
    root = problem.getStartState() 					#Find the first state
    states = util.Stack() 						    #Create the LIFO stack
    states.push((root, [])) 						#Introduce the first state into the stack
    visitedStates= [] 							    #Create the list of visited states
    visitedStates.append(root) 						#The first state is the root    
    while states and not problem.isGoalState(root):	                #If the current state is the goal or there is no more states, then finish searching
        state, movement = states.pop() 					            #Obtain the state from the stack
        visitedStates.append(state) 					                #Introduce the state in the visted states list
        successors = problem.getSuccessors(state) 				        #Obtain the state's successors
        for successor in successors: 					
            position = successor[0] 						                #The position of the successor's state
            if position not in visitedStates:
                root = successor[0] 						                    #Now we will be working with that state so we update the root (it s like starting again)
                newMovement = successor[1] 						            #The movement of the successor's state movement
                completeMovement = movement + [newMovement] 			        #The movement will be the one that the state has done + the one from the successor to the next one
                states.push((position, completeMovement))				    #Introduce the state that has that position and that final movement
    return completeMovement						    #Return the path that pacman has to do
    util.raiseNotDefined()




def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    root = problem.getStartState()                  #Find the first state
    states = util.Queue()                           #Create the FIFO queue
    states.push((root, []))                         #Introduce the first state into the queue
    visitedStates = []                              #Create the list of visited states
    visitedStates.append(root)                      #The first state is the first one visited
    while states:                                               #If there is no more states, then finish searching
        state, movement = states.pop()                           #Obtain the state from the queue
        if problem.isGoalState(state):
            return movement
        successors = problem.getSuccessors(state)                #Obtain the state's successors
        for successor in successors:
            position = successor [0]
            if position not in visitedStates:
                visitedStates.append(position)                   #Introduce the state in the visited states list
                newMovement = successor[1]                       #The movement of the successor's state movement
                completeMovement = movement + [newMovement]      #The movement will be the one that the state has done + the one from the successor to the next one
                states.push((position, completeMovement))        #Introduce the state that has that position and that final movement
    util.raiseNotDefined()
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    root = problem.getStartState()                  #Find the first state
    states = util.PriorityQueue()                   #Create the priority queue
    states.push((root, []), 0)                      #Introduce the first state into the priority queue
    visitedStates = []                              #Create the list of visited states

    while states:                                                               #If there is no more states, then finish searching
        state, movement = states.pop()                                          #Obtain the state from the priority queue
        if problem.isGoalState(state):
            return movement
        if state not in visitedStates:                                          
            successors = problem.getSuccessors(state)                           #Obtain the state's successors
            for successor in successors:
                position = successor[0]
                if position not in visitedStates:
                    newMovement = successor[1]                                  #The movement of the successor's state movement
                    completeMovement = movement + [newMovement]                 #Calculate the complete movement: the previous movements + the new movement to the successor
                    totalCost = problem.getCostOfActions(completeMovement)      #Calculate the cost of the action with that total cost
                    states.push((position, completeMovement), totalCost)        #Introduce the state with that position and movement, and the cost for that action
        visitedStates.append(state)                 #Introduce the state in the visited states list      
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #This methon is quite similar as UCS, but it calculates the cost also with the heuristic
    root = problem.getStartState()                          #Find the first state
    states = util.PriorityQueue()                           #Create the priority queue
    states.push((root, []), nullHeuristic(root, problem))   #Introduce the first state into the priority queue
    visitedStates = []                                      #Create the list of visited states
    while states:
        state, movement = states.pop()                                          #Obtain the state from the priority queue
        if problem.isGoalState(state):                                          
            return movement
        if state not in visitedStates:
            successors = problem.getSuccessors(state)                           #Obtain the state's successors
            for successor in successors:
                position = successor[0]
                if position not in visitedStates:
                    newMovement = successor[1]                                  #The movement of the successor's state movement
                    completeMovement = movement + [newMovement]                 #Calculate the complete movement: the previous movements + the new movement to the successor
                    totalCost = problem.getCostOfActions(completeMovement) + heuristic(position, problem)   #Calculates the cost as UCS but adding the heuristic's cost
                    states.push((position, completeMovement), totalCost)        ##Introduce the state with that position and movement, and the cost for that action
        visitedStates.append(state)                         #Introduce the state in the visited states list
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
