import random
from BaseAI import BaseAI

import time

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)
# getAvailableMoves(self, dirs=vecIndex): # -> List[(int, Grid)]

class IntelligentAgent(BaseAI):
    maxTime = 0.2   # Maximum time allowed per move in seconds
    buffer  = 0.01  # Buffer time to make sure we don't exceed maxTime
    turnStartTime = None

    def eval(self, grid):
        # Calculate heuristic value of the grid
        return 1.0

    def minimize(self, grid, alpha, beta, depth):
        # End this depth if time is almost up
        if time.process_time() - self.turnStartTime > self.maxTime - self.buffer:
            return None
        
        # Computer will minimize
        minUtility = float('inf')
        minChild = None
        minMove = None

        if self.terminalTestMin(grid) or depth == 0:
            return None, eval(grid), None
        
        for tileValue in [2, 4]:
            for emptyCell in grid.getAvailableCells():

                newGrid = grid.clone().setCellValue(emptyCell, tileValue)
                
                res = self.maximize(newGrid, alpha, beta, depth)

                if isinstance(res, tuple):
                    _, utility, move = res
                else:
                    return None

                if utility < minUtility:
                    minChild, minUtility, minMove = newGrid, utility, move

                if minUtility <= alpha:
                    break

                if minUtility < beta:
                    beta = minUtility

        return minChild, minUtility, minMove

    def maximize(self, grid, alpha, beta, depth):
        # End this depth if time is almost up
        if time.process_time() - self.turnStartTime > self.maxTime - self.buffer:
            return None
        
        # Player will maximize
        maxUtility = float('-inf')
        maxChild = None
        maxMove = None

        if self.terminalTestMax(grid):
            return None, eval(grid), None
        
        for move, newGrid in grid.getAvailableMoves():
            _, utility, _ = self.maximize(newGrid, alpha, beta, depth - 1)
                
            res = self.maximize(newGrid, alpha, beta, depth - 1)

            if isinstance(res, tuple):
                _, utility, _ = res
            else:
                return None

            if utility > maxUtility:
                maxChild, maxUtility, minMoveMove = newGrid, utility, move

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

    def getMoveWithIds(self, grid):
        startTime = time.process_time()

        # Implement iterative deepening here
        depth = 1
        move = grid.getAvailableMoves()[0][0]  # Default move

        while time.process_time() - startTime < self.maxTime - self.buffer:
            res = self.minimize(grid, float('-inf'), float('inf'), depth)

            if isinstance(res, tuple):
                _, _, move = res
            else:
                break
            depth += 1