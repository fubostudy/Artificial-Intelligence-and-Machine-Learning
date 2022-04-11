# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primari
# ly created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import time
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

    def getAction(self, gameState): #根据当前的评估函数确定下一步的动作
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        # 获取当前可能的下一步的方向 有stop east ...
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        # 根据评估函数获取所有的下一步的权值
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # 获取最好的分数
        bestScore = max(scores)
        # 根据最好的分数获取最好的行动选择
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # 从最好的行动集合中随机选择一个最为下一步的动作
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        #获取位置
        newGhostPos = successorGameState.getGhostPositions()
        CapsulesPos = successorGameState.getCapsules()

        # 设定参数：评估函数组合中每个距离特征的权重 w 、吃豆人不受幽灵影响的最大距离alpha
        w = [2,6,10,0.5]
        alpha = 4

        # 吃豆人和豆子的距离 （1/曼哈顿距离mdis）
        FoodDis = 0
        for x in range(newFood.width):  #遍历二维数组
            for y in range(newFood.height):
                if newFood[x][y]:
                    FoodDis += w[0]*(1/manhattanDistance(newPos, [x,y]))
        # 吃豆人和幽灵的距离 （1/曼哈顿距离mdis）
        GhostDis = 0
        for ghosts,scareTimes in zip(newGhostPos, newScaredTimes):
            mdis = manhattanDistance(newPos, ghosts)
            if scareTimes > 0:  # 恐惧状态
                GhostDis += w[1]*(1/mdis)
            elif 0 < mdis and mdis < alpha:  # 正常状态
                GhostDis -= w[2]*(1/mdis)
            elif mdis==0:  # 下一步可能是幽灵
                GhostDis -= 100000
        # 吃豆人和胶囊的距离 （1/曼哈顿距离mdis）
        CapsulesDis = 0
        for capsules in CapsulesPos:
            mdis = manhattanDistance(newPos, capsules)
            if mdis > 0:  #尽量去吃
                CapsulesDis += w[3]*(1/mdis)
            elif mdis == 0: # 下一步可能是胶囊
                CapsulesDis += 100000
        # return successorGameState.getScore()
        return successorGameState.getScore()+FoodDis+GhostDis+CapsulesDis #组合后的评估函数

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

        # max层仅用于吃豆人，吃豆人的agentIndex =0 @xxf
        def maxLevel(gameState, depth):  # 传入游戏状态，深度
            currDepth = depth + 1  # 吃豆人当前深度+1
            # 判断当前状态是否达到了停止条件
            if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
                return self.evaluationFunction(gameState)
            maxvalue = -999999 # 初始化maxvalue为负无穷
            actions = gameState.getLegalActions(0) # actions记录合法的移动
            for action in actions:# 根据移动来生成后继状态
                successor = gameState.generateSuccessor(0, action)
                # 用maxvalue与min层比较，取最大值
                maxvalue = max(maxvalue, minLevel(successor, currDepth, 1))
            return maxvalue  # 在该层中找到最大值传导到上一层

        # min层是对于幽灵而言的，参数为游戏状态，深度，agentIndex
        def minLevel(gameState, depth, agentIndex):
            minvalue = 999999  # 初始化minvalue为正无穷
            if gameState.isWin() or gameState.isLose():  # 赢或者输了就退出
                return self.evaluationFunction(gameState)
            # 获取当前状态合法的移动
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                # 根据移动生成新的后继状态
                successor = gameState.generateSuccessor(agentIndex, action)
                # 根据幽灵的个数，找到min层中的最小值minvalue
                if agentIndex == (gameState.getNumAgents() - 1):#最后一个幽灵
                    minvalue = min(minvalue, maxLevel(successor, depth))
                else: #不是最后一个幽灵
                    minvalue = min(minvalue, minLevel(successor, depth, agentIndex + 1))
            return minvalue

        currentScore = -999999 # 初始化
        returnAction = ''
        # 获取吃豆人合法的行动
        actions = gameState.getLegalActions(0)
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            # 接下里的一层是min层，可以把当前的这一层看作min层的根结点
            score = minLevel(nextState, 0, 1)
            # 选择后继状态中最大值移动
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction  # 返回最高得分移动的方向
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxLevel(gameState, depth, alpha, beta):
            currDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
                # return self.evaluationFunction(gameState)
                return better(gameState)
            maxvalue = -999999
            actions = gameState.getLegalActions(0)

            alpha1 = alpha
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                maxvalue = max(maxvalue, minLevel(successor, currDepth, 1, alpha1, beta))
                if maxvalue > beta: #最大得分超过beta
                    return maxvalue
                alpha1 = max(alpha1, maxvalue)
            return maxvalue #返回最大得分

        def minLevel(gameState, depth, agentIndex, alpha, beta):
            minvalue = 999999
            if gameState.isWin() or gameState.isLose():
                # return self.evaluationFunction(gameState)
                return better(gameState)
            actions = gameState.getLegalActions(agentIndex)

            beta1 = beta
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == (gameState.getNumAgents() - 1):
                    minvalue = min(minvalue, maxLevel(successor, depth, alpha, beta1))
                    if minvalue < alpha: #最小得分小于alpha
                        return minvalue
                    beta1 = min(beta1, minvalue)
                else:
                    minvalue = min(minvalue, minLevel(successor, depth, agentIndex + 1, alpha, beta1))
                    if minvalue < alpha: #最小得分小于alpha
                        return minvalue
                    beta1 = min(beta1, minvalue)
            return minvalue

        actions = gameState.getLegalActions(0)
        currentScore = -999999
        returnAction = ''
        alpha = -999999
        beta = 999999
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            score = minLevel(nextState, 0, 1, alpha, beta)
            if score > currentScore:
                returnAction = action
                currentScore = score
            if score > beta:
                return returnAction
            alpha = max(alpha, score)
        return returnAction
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newGhostPos = currentGameState.getGhostPositions()
    CapsulesPos = currentGameState.getCapsules()

    # 设定参数：评估函数组合中每个距离特征的权重 w 、吃豆人不受幽灵影响的最大距离alpha
    w = [2,6,40,0.5]
    alpha = 4

    # 吃豆人和豆子的距离 （1/曼哈顿距离mdis）
    FoodDis = 0
    for x in range(newFood.width):  # 遍历二维数组
        for y in range(newFood.height):
            if newFood[x][y]:
                FoodDis += w[0] * (1 / manhattanDistance(newPos, [x, y]))
    # 吃豆人和幽灵的距离 （1/曼哈顿距离mdis）
    GhostDis = 0
    for ghosts, scareTimes in zip(newGhostPos, newScaredTimes):
        mdis = manhattanDistance(newPos, ghosts)
        if scareTimes > 0:  # 恐惧状态
            GhostDis += w[1] * (1 / mdis)
        elif 0 < mdis and mdis < alpha:  # 正常状态
            GhostDis -= w[2] * (1 / mdis)
        elif mdis == 0:  # 下一步可能是幽灵
            GhostDis -= 100000
    # 吃豆人和胶囊的距离 （1/曼哈顿距离mdis）
    CapsulesDis = 0
    for capsules in CapsulesPos:
        mdis = manhattanDistance(newPos, capsules)
        if mdis > 0:  # 尽量去吃
            CapsulesDis += w[3] * (1 / mdis)
        elif mdis == 0:  # 下一步可能是胶囊
            CapsulesDis += 100000
    # return successorGameState.getScore()
    return currentGameState.getScore() + FoodDis + GhostDis + CapsulesDis  # 组合后的评估函数
#util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
