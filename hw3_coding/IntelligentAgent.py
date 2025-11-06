import random
from BaseAI import BaseAI

import time
import math

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)
# getAvailableMoves(self, dirs=vecIndex): # -> List[(int, Grid)]

class IntelligentAgent(BaseAI):
    maxTime = 0.2   # Maximum time allowed per move in seconds
    buffer  = 0.01  # Buffer time to make sure we don't exceed maxTime
    turnStartTime = None

    def eval(self, grid):
        # Calculate heuristic value of the grid
        # Avaliable_cell_count
        avaliable_cell_count = len(grid.getAvailableCells())

        # average_tile_value
        sum = 0
        count = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.getCellValue((x, y)) != 0:
                    sum += grid.getCellValue((x, y))
                    count += 1

        return math.log2(sum / count) + avaliable_cell_count

    def minimize(self, grid, alpha, beta, depth):
        # print("Minimize at depth:", depth)
        # End this depth if time is almost up
        # import pdb; pdb.set_trace()
        if time.process_time() - self.turnStartTime > self.maxTime - self.buffer:
            return None
        
        # Computer will minimize
        minUtility = float('inf')
        minChild = None
        minMove = None

        if self.terminalTestMin(grid) or depth == 0:
            return None, self.eval(grid), None
        
        for tileValue in [2, 4]:
            # print("Inserting tile:", tileValue)
            for emptyCell in grid.getAvailableCells():
                # print("At cell:", emptyCell)
                
                newGrid = grid.clone()
                newGrid.setCellValue(emptyCell, tileValue)
                
                res = self.maximize(newGrid, alpha, beta, depth)

                if isinstance(res, tuple):
                    _, utility, move = res
                else:
                    return None

                if utility < minUtility:
                    # print("New min utility:", utility, "at cell", emptyCell, "with tile", tileValue)
                    minChild, minUtility, minMove = newGrid, utility, move

                if minUtility <= alpha:
                    break

                if minUtility < beta:
                    beta = minUtility

        return minChild, minUtility, minMove

    def maximize(self, grid, alpha, beta, depth):
        # print("Maximize at depth:", depth)
        # End this depth if time is almost up
        # import pdb; pdb.set_trace()
        if time.process_time() - self.turnStartTime > self.maxTime - self.buffer:
            return None
        
        # Player will maximize
        maxUtility = float('-inf')
        maxChild = None
        maxMove = None

        if self.terminalTestMax(grid):
            return None, self.eval(grid), None
        
        for move, newGrid in grid.getAvailableMoves():                
            # import pdb; pdb.set_trace()
            res = self.minimize(newGrid, alpha, beta, depth - 1)

            if isinstance(res, tuple):
                _, utility, _ = res
            else:
                return None

            if utility > maxUtility:
                maxChild, maxUtility, maxMove = newGrid, utility, move

            if maxUtility >= beta:
                break

            if maxUtility > alpha:
                alpha = maxUtility

        return maxChild, maxUtility, maxMove
    
    def terminalTestMax(self, grid):
        # Check if there are no available moves
        return grid.canMove() == False
    
    def terminalTestMin(self, grid):
        # Check if there are no empty cells
        return len(grid.getAvailableCells()) == 0

    def getMove(self, grid):
        self.turnStartTime = time.process_time()

        # Implement iterative deepening here
        depth = 1
        move = grid.getAvailableMoves()[0][0]  # Default move

        while time.process_time() - self.turnStartTime < self.maxTime - self.buffer:
            # print("Searching at depth:", depth)
            res = self.minimize(grid, float('-inf'), float('inf'), depth)

            if isinstance(res, tuple):
                _, _, move = res
                # print("Best move at depth", depth, "is", move)
                if move is None:
                    raise Exception("No valid move found")
            else:
                # print("Time's up during search at depth:", depth)
                break
            # import pdb; pdb.set_trace()
            depth += 1

        return move