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
        gain = [3, 1, 1.2, 1]

        availableCellCount = self.availableCellCount(grid)
        averageTileValue   = self.averageTileValue(grid)
        monotonicity       = self.monotonicity(grid)
        smoothness         = self.smoothness(grid)

        return gain[0] * availableCellCount + \
               gain[1] * averageTileValue   + \
               gain[2] * monotonicity       + \
               gain[3] * smoothness

    def expectimax(self, grid, alpha, beta, depth):
        # End this depth if time is almost up
        if time.process_time() - self.turnStartTime > self.maxTime - self.buffer:
            return None

        if depth == 0:
            return None, self.eval(grid), None

        # Player will maximize
        maxUtility = float('-inf')
        maxChild = None
        maxMove = None

        if self.terminalTestMax(grid):
            return None, self.eval(grid), None

        for move, newGrid in grid.getAvailableMoves():
            res = self.expectimin(newGrid, alpha, beta, depth)

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

    def expectimin(self, grid, alpha, beta, depth):
        # End this depth if time is almost up
        if time.process_time() - self.turnStartTime > self.maxTime - self.buffer:
            return None

        # Computer will minimize
        minUtility = float('inf')
        minChild = None
        minMove = None

        for emptyCell in grid.getAvailableCells():

            res = self.expectichance(grid, alpha, beta, depth, emptyCell)

            if isinstance(res, tuple):
                newGrid, utility, move = res
            else:
                return None

            if utility < minUtility:
                minChild, minUtility, minMove = newGrid, utility, move

            if minUtility < beta:
                beta = minUtility

        return minChild, minUtility, minMove

    def expectichance(self, grid, alpha, beta, depth, cell):
        chanceNodeUtility = 0
        for tileValue, probability in [(2, 0.9), (4, 0.1)]:
            newGrid = grid.clone()
            newGrid.setCellValue(cell, tileValue)
            res = self.expectimax(newGrid, alpha, beta, depth - 1)

            if isinstance(res, tuple):
                _, utility, move = res
                chanceNodeUtility += probability * utility
            else:
                return None

        return newGrid, chanceNodeUtility, move

    def terminalTestMax(self, grid):
        # Check if there are no available moves
        return grid.canMove() == False

    def getMove(self, grid):
        self.turnStartTime = time.process_time()

        # Implement iterative deepening here
        depth = 1
        move = grid.getAvailableMoves()[0][0]  # Default move

        while time.process_time() - self.turnStartTime < self.maxTime - self.buffer:
            res = self.expectimax(grid, float('-inf'), float('inf'), depth)

            if isinstance(res, tuple):
                _, _, move = res
                if move is None:
                    raise Exception("No valid move found")
            else:
                break
            # import pdb; pdb.set_trace()
            depth += 1

        return move
