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

    # def __init__(self, gain1, gain2, gain3, gain4):
    #     self.gain = [gain1, gain2, gain3, gain4]

    def availableCellCount(self, grid):
        return len(grid.getAvailableCells())
    
    def averageTileValue(self, grid):
        sum = 0
        count = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.getCellValue((x, y)) != 0:
                    sum += grid.getCellValue((x, y))
                    count += 1

        return math.log2(sum / count)
    
    def monotonicity(self, grid):
        # Check Downward
        downScore = 0
        for col in range(grid.size):
            colScore = 0
            for row in range(0,grid.size):
                for nextRow in range(row + 1, grid.size):
                    if grid.getCellValue((nextRow, col)) > grid.getCellValue((row, col)):
                        colScore += 1
            downScore += colScore

        # Check Upward
        upScore = 0
        for col in range(grid.size):
            colScore = 0
            for row in range(0,grid.size)[::-1]:
                for nextRow in range(0, row)[::-1]:
                    if grid.getCellValue((nextRow, col)) > grid.getCellValue((row, col)):
                        colScore += 1
            upScore += colScore

        verticalScore = max(downScore, upScore)

        # Check Rightward
        rightScore = 0
        for row in range(grid.size):
            rowScore = 0
            for col in range(0,grid.size):
                for nextCol in range(col + 1, grid.size):
                    if grid.getCellValue((row, nextCol)) > grid.getCellValue((row, col)):
                        rowScore += 1
            rightScore += rowScore

        # Check Leftward
        leftScore = 0
        for row in range(grid.size):
            rowScore = 0
            for col in range(0,grid.size)[::-1]:
                for nextCol in range(0, col)[::-1]:
                    if grid.getCellValue((row, nextCol)) > grid.getCellValue((row, col)):
                        rowScore += 1
            leftScore += rowScore
        horizontalScore = max(rightScore, leftScore)

        return verticalScore + horizontalScore
    
    def smoothness(self, grid):
        def getNeighbors(row, col):
            neighbors = []
            # import pdb; pdb.set_trace()
            if row == 0:
                neighbors.append((row + 1, col))
            elif row == grid.size - 1:
                neighbors.append((row - 1, col))
            else:
                neighbors.append((row - 1, col))
                neighbors.append((row + 1, col))

            if col == 0:
                neighbors.append((row, col + 1))
            elif col == grid.size - 1:    
                neighbors.append((row, col - 1))
            else:
                neighbors.append((row, col - 1))
                neighbors.append((row, col + 1))
            return neighbors

        smoothnessScore = 0

        for row in range(grid.size):
            for col in range(grid.size):
                homeValue = grid.getCellValue((row, col))
                for neighbor in getNeighbors(row, col):
                    # import pdb; pdb.set_trace()
                    neighborValue = grid.getCellValue(neighbor)
                    if neighborValue != 0:
                        diff = abs(homeValue - neighborValue)
                        smoothnessScore -= diff if diff <= 1 else math.log2(diff)

        return smoothnessScore
                

    def eval(self, grid):
        # Calculate heuristic value of the grid
        # gain = self.gain
        gain = [10.0, 2.0, 7.0, 4.0]
        # print("Gain:", gain)

        availableCellCount = self.availableCellCount(grid)
        averageTileValue   = self.averageTileValue(grid)
        monotonicity       = self.monotonicity(grid)
        smoothness         = self.smoothness(grid)

        # print(
        #     "No Gain", 
        #     # availableCellCount,
        #     averageTileValue,
        #     monotonicity,
        #     # smoothness
        # )

        # print(
        #     "With Gain", 
        #     # gain[0] * availableCellCount,
        #     gain[1] * averageTileValue,
        #     gain[2] * monotonicity,
        #     # gain[3] * smoothness
        # )

        return gain[0] * availableCellCount + \
               gain[1] * averageTileValue   + \
               gain[2] * monotonicity       + \
               gain[3] * smoothness

    def minimize(self, grid, alpha, beta, depth):
        # print("Minimize at depth:", depth)
        # End this depth if time is almost up
        # import pdb; pdb.set_trace()
        # print('Start time:', self.turnStartTime)
        if time.process_time() - self.turnStartTime > self.maxTime - self.buffer:
            # print('Returning None due to time limit')
            return None
        
        # Computer will minimize
        minUtility = float('inf')
        minChild = None
        minMove = None

        # if depth == 0:
            # print('Depth 0 reached')
        #     return None, self.eval(grid), None
        
        for tileValue in [2, 4]:
            # print("Inserting tile:", tileValue)
            for emptyCell in grid.getAvailableCells():
                # print('CCCCCC')
                # print("At cell:", emptyCell)
                
                newGrid = grid.clone()
                newGrid.setCellValue(emptyCell, tileValue)
                
                res = self.maximize(newGrid, alpha, beta, depth - 1)

                if isinstance(res, tuple):
                    _, utility, move = res
                else:
                    # print('DDDDDDDD')
                    return None

                if utility < minUtility:
                    # print("New min utility:", utility, "at cell", emptyCell, "with tile", tileValue)
                    minChild, minUtility, minMove = newGrid, utility, move

                if minUtility <= alpha:
                    break

                if minUtility < beta:
                    beta = minUtility

                # print('EEEEEEEEE')
        return minChild, minUtility, minMove

    def maximize(self, grid, alpha, beta, depth):
        # print("Maximize at depth:", depth)
        # End this depth if time is almost up
        # import pdb; pdb.set_trace()
        if time.process_time() - self.turnStartTime > self.maxTime - self.buffer:
            return None

        if depth == 0:
            # print('Depth 0 reached')
            return None, self.eval(grid), None
        
        # Player will maximize
        maxUtility = float('-inf')
        maxChild = None
        maxMove = None

        if self.terminalTestMax(grid):
            return None, self.eval(grid), None
        
        for move, newGrid in grid.getAvailableMoves():                
            # import pdb; pdb.set_trace()
            res = self.minimize(newGrid, alpha, beta, depth)

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
            # print("Starting grid:", grid.map)
            res = self.maximize(grid, float('-inf'), float('inf'), depth)

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
