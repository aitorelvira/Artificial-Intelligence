# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"        
        foodList = newFood.asList()     #List of food left
        minFoodDistance = 0             #Minimum distance to food
        minGhostDistance = 0            #Minimum distance to a ghost
        ghostValue = 0                  #Value/score of the ghost
        if len(foodList) > 0:           #Know if there is still food left
            minFoodDistance, closestFood = min((manhattanDistance(newPos, food), food) for food in foodList)    #Get the minimum distance to food using the manhattan distance and which is the closest food
        if len(newGhostStates) > 0:     #Know if there is more ghosts
            minGhostDistance, closestGhost = min((manhattanDistance(newPos, ghost.getPosition()), ghost) for ghost in newGhostStates)  #Get the minimum distance to a ghost using the manhattan distance and which is the closest ghost
        if minGhostDistance < 3 and closestGhost.scaredTimer <= 0:         #If the gost is near and scared, its value/score will be -100
            ghostValue = -100
        score = 1.0 / (minFoodDistance + len(foodList) + 1) + ghostValue   #Calculate the score
        return score + successorGameState.getScore()                       #The final score is the one we currently have plus the one from the succesor state
        

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minFunction(state, depth, agent):      #This function calculates the minimum value
            if state.isWin() or state.isLose():     #If the state is winning or losing, return the score of that state
                return state.getScore()
            nextAgent = agent + 1                   #The next agent is the actual agent plus one
            if agent == state.getNumAgents() - 1:   #If the next agent is the total number of agents minus one, that agent will be Pacman, and that is the 0 agent
                nextAgent = 0
            infScore = float("Inf")
            score = infScore
            for move in state.getLegalActions(agent):   #Get each legal action from the state
                if nextAgent == 0:                      #Checks if next agent is Pacman
                    if self.depth == depth + 1:         #If actual depth is the depth plus one, it will evaluate the function with the state successor 
                        score = self.evaluationFunction(state.generateSuccessor(agent, move))
                    else:                               #In other case, it will find the maximum value with the maxFunction
                        score = maxFunction(state.generateSuccessor(agent, move), depth + 1)
                else:                                   #If that agent is not Pacman, it comes back to minFunction but with the next agent, to calculate the minimum value
                    score = minFunction(state.generateSuccessor(agent, move), depth, nextAgent)
                if score < infScore:                    #If that value is less than the values obtained before, that will be the minimum score obtained by the function
                    infScore = score
            return infScore
        
        def maxFunction(state, depth):              #This function calculates the maximum value
            if state.isWin() or state.isLose():     #If the state is winning or losing, return the score of that state
                return state.getScore()
            infScore = float("-Inf")
            score = infScore
            action = Directions.STOP
            for move in state.getLegalActions(0):   #Get all the legal actions from the agent 0, which is Pacman
                score = minFunction(state.generateSuccessor(0, move), depth, 1)    #Calls the minFunction with the agent 1
                if score > infScore:                #If that value is bigger than the values obtained before, that will be the maximum score, and that action will be the best possible move
                    infScore = score                
                    action = move
            if depth == 0:                          #If the agent is Pacman, will return the best action, obtained just above
                return action
            else:                                   #If the agent is not Pacman, will return the best score, obtained just above
                return infScore
        return maxFunction(gameState, 0)            #Calls again the maxFunction with the agent 0, which is Pacman

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        movements = self.maxFunction(gameState, self.depth, float("-Inf"), float("Inf"))[1]  #Calls the maxFunction
        return movements

    def maxFunction(self, gameState, depth, alpha, beta):           #This function obtains the maximum score and best movement
        if gameState.isWin() or gameState.isLose() or depth == 0:   #Checks if it is a winning or losing state or if thats it is the whole depth, so gets the function evaluated and do not make any move
            return (self.evaluationFunction(gameState), None)
        actions = gameState.getLegalActions(0)                      #Gets all the legal actions from that state
        values = []                     #List where values will be stored
        inf = float("-Inf")
        for action in actions:
            inf = max(inf, self.minFunction(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)[0])  #Gets the maximum value between -Infinite or the minimum value obtained by minFunction
            values.append(inf)          #Stores the maximum value obteined
            if inf > beta:              #Check if that value is bigger than beta
                return (inf, action)
            alpha = max(alpha, inf)     #Alpha is the biggest between alpha or the maximum value obtained before (inf)
        max_value = max(values)         #Gets the bigger value from the list
        index = [index for index in range(len(values)) if values[index] == max_value]  #Gets the index of the biggest value
        moves = actions[index[0]]       #That will be the best move
        return (max_value, moves)       #Returns the maximum value and the best move

    def minFunction(self, gameState, depth, agentIndex, alpha, beta):   #This function obtains the minimum score and best movement
        if gameState.isWin() or gameState.isLose() or depth == 0:       #Checks if it is a winning or losing state or if thats it is the whole depth, so gets the function evaluated and do not make any move
            return (self.evaluationFunction(gameState), None)
        actions = gameState.getLegalActions(agentIndex)                 #Gets all the legal actions from that state
        values = []             #List where values will be stored
        inf = float("Inf")
        for action in actions:
            if agentIndex == gameState.getNumAgents() - 1 : 
                inf = min(inf, self.maxFunction(gameState.generateSuccessor(agentIndex, action), depth - 1, alpha, beta)[0])  #Gets the minimum value between infinite or the maximum value obtained by minFunction
                values.append(inf)      #Stores the minimum value obtained
                if inf < alpha:         #Check if that value is less than alpha  
                    return(inf, action)     
                beta = min(beta, inf)   #Beta is the lowest between beta or the minimum value obtained before (inf) 
            else:
                inf = min(inf, self.minFunction(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)[0])  #Gets the minimum value between infinite or the maximum value obtained by minFunction
                values.append(inf)      #Store the minimum value obtained
                if inf < alpha:         #Check if that value is less than alpha
                    return (inf, action)
                beta = min(beta, inf)   #Beta is the lowest between beta or the minimum value obtained before (inf)
        min_value = min(values)
        index = [index for index in range(len(values)) if values[index] == min_value]  #Gets the index of the biggest value
        moves = actions[index[0]]       #That will be the best move
        return (min_value, moves)       #Returns the maximum value and the best move
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"   
        maxValue = float('-inf')
        bestAction = None
        for action in gameState.getLegalActions(0):     #Gets all the legal actions
            value = self.expectiMax(gameState.generateSuccessor(0, action), self.depth, 1)  #Gets the value calling the function expectiMax
            if value > maxValue:                        #If the value obtained is bigger than the maximum value previously obtained
                maxValue = value                        #That will be new best value
                bestAction = action                     #That will be the best action
        return bestAction
        
    def expectiMax(self, gameState, depth, agentIndex):             #Function that gets the total score using expectimax
        if gameState.isWin() or gameState.isLose() or depth == 0:   #Checks if it is a winning or losing state or if thats it is the whole depth, so gets the function evaluated and do not make any move
            return self.evaluationFunction(gameState)

        if agentIndex == 0:                         #Checks if the agent is Pacman
            actions = gameState.getLegalActions(0)  #Gets all the legal actions
            return max(self.expectiMax(gameState.generateSuccessor(0, action), depth, 1) for action in actions) #Gets the max value calling the function again, with the index 1
        else:                                       #Checks if that agent is not Pacman
            actions = gameState.getLegalActions(agentIndex)         #Gets all the legal actions
            newIndex = (agentIndex + 1) % gameState.getNumAgents()  #Gets the new index
            if newIndex == 0:       #Checks if the new index is Pacman
                depth = depth - 1   
            totalValue = sum(self.expectiMax(gameState.generateSuccessor(agentIndex, action), depth, newIndex) for action in actions)#Gets the max value calling the function again, with the new index
            return totalValue * 1.0 / len(actions) * 1.0    #Gets the total value/score
        
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Getting close to ghosts gives a negative score to Pacman, so it will not tend to go near to it.
    If Pacman can eat the ghost, it will give Pacman the highest score, so will try to eat them.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    def ghostValue(newPos, ghostStates): #Gets the score of ghosts
        totalGhost = 0
        for ghost in ghostStates:       #Check all the ghosts
            distance = manhattanDistance(newPos, newGhostStates[0].getPosition())   #Gets the distance to the ghost, using the manhattan distance here too
            if distance > 0:
                if ghost.scaredTimer > 0:   #If that ghost is scared, that ghost will have a bigger value
                    totalGhost = totalGhost + 100.0 / distance
                else:                       #If that ghost is not scared, that ghost will have a lower value
                    totalGhost = totalGhost - 10.0 / distance
        return totalGhost

    def foodValue(newPos, newFood):
        foodList = newFood.asList()     #Gets the new food in a list
        if foodList:
            distance = []               #List where distances will be stored
            for food in newFood.asList():
                distance.append(manhattanDistance(newPos, food))    #Stores the distance obtained with the manhattan distance
            return 10.0 / min(distance)     #Gets the value, divided by the lowest distance
        return 0

    return currentGameState.getScore() + ghostValue(newPos, newGhostStates) + foodValue(newPos, newFood)    #Gets the total score, which is the one of the state plus the ghost and food costs obtained with those functions
     
# Abbreviation
better = betterEvaluationFunction
