import random
from BaseAI import BaseAI

import time

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)
# getAvailableMoves(self, dirs=vecIndex): # -> List[(int, Grid)]

class IntelligentAgent(BaseAI):
    maxTime = 0.2   # Maximum time allowed per move in seconds
    buffer  = 0.01  # Buffer time to make sure we don't exceed maxTime
    turnStartTime = None

    def minimize(self, grid, alpha, beta):
        minUtility = float('inf')
        minChild = None
        minMove = None

        if self.terminalTestMin(grid):
            return None, eval(grid), None
        
        for move, newGrid in grid.getAvailableMoves():
            _, utility = self.maximize(newGrid, alpha, beta)

            if utility < minUtility:
                minChild, minUtility, minMove = newGrid, utility, move

            if minUtility <= alpha:
                break

            if minUtility < beta:
                beta = minUtility

        return minChild, minUtility, minMove

    def maximize(self, grid, alpha, beta):
        maxUtility = float('-inf')
        maxChild = None
        maxMove = None

        if self.terminalTestMax(grid):
            return None, eval(grid), None
        
        for move, newGrid in grid.getAvailableMoves():
            _, utility = self.maximize(newGrid, alpha, beta)

            if utility > maxUtility:
                maxChild, maxUtility, minmaxMoveMove = newGrid, utility, move

            if maxUtility <= alpha:
                break

            if maxUtility < beta:
                beta = maxUtility

        return maxChild, maxUtility, maxMove
    
    def terminalTestMax(self, grid):
        # Check if there are no available moves
        return len(grid.getAvailableMoves()) == 0
    
    def terminalTestMin(self, grid):
        # Check if there are no empty cells
        return len(grid.getAvailableCells()) == 0



    def getMove(self, grid):
        startTime = time.process_time()

        # Implement iterative deepening here
        
        


        return random.choice(moveset)[0] if moveset else None

    # def getMoveWithIds(self, grid):
    #     startTime = time.process_time()

    #     # Implement iterative deepening here
    #     depth = 1
    #     while time.process_time() - startTime < self.maxTime - self.buffer:
    #         availableMoves, resultGrid = grid.getAvailableMoves()

    #         for 
        


    #     return random.choice(moveset)[0] if moveset else None
        