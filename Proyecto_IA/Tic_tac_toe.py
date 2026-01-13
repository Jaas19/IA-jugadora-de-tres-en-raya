import numpy as np
import random
import tensorflow as tf
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import copy

class Environment:
    def __init__(self):
        self.AI_INPUT = [0,0,1]
        self.PLAYER_INPUT = [0,1,0]
        self.EMPTY_INPUT = [1,0,0]
        self.board = [list(self.EMPTY_INPUT) for _ in range(9)]
        self.done = False

    def get_flattened_board(self):
        return np.array(self.board).flatten()

    def reset(self):
        self.board = [list(self.EMPTY_INPUT) for _ in range(9)]
        self.done = False

    # Función ejecutada para comprobar si se continua el juego
    def check_empty_tiles(self):
        for tile in self.board:
            if tile == self.EMPTY_INPUT:
                return True
        return False

    # Función ejecutada en cada movimiento
    def check_board(self):
        rows = [
            self.board[0:3],
            self.board[3:6],
            self.board[6:9],
            self.board[0::3],
            self.board[1::3],
            self.board[2::3],
            self.board[0::4],
            self.board[2:7:2]
        ]
        for row in rows:
            if row[0] == row[1] == row[2] and row[0] != self.EMPTY_INPUT:
                if row[0] == self.AI_INPUT:
                    return +10
                elif row[0] == self.PLAYER_INPUT:
                    return -10
            else:
                continue
        return 0

    def change_board(self, position, movement):
        if self.board[position] != self.EMPTY_INPUT:
            return -10
        else:
            self.board[position] = list(movement)
            if self.check_board() == 0:
                result = Minimax.get_scores(board = self.board)
                self.change_board(result, self.PLAYER_INPUT)

    def restart_board(self):
        self.board = [list(self.EMPTY_INPUT) for _ in range(9)]

    def is_full(self):
        return not any(tile == self.EMPTY_INPUT for tile in self.board)


class Minimax:
    def __init__(self):
        self.AI = [0, 0, 1]
        self.PLAYER = [0, 1, 0]
        self.EMPTY = [1, 0, 0]

    def get_scores(self, board):
        scores = []

        for i in range(9):
            if board[i] != self.EMPTY:
                scores.append(-999)
            else:
                board[i] = self.AI

                score = self._recursive_solve(board, depth=0, is_ai_turn=False)
                scores.append(score)

                board[i] = self.EMPTY

        return scores

    def _recursive_solve(self, board, depth, is_ai_turn):
        winner = self.check_winner(board)

        if winner == 10: return 10 - depth
        if winner == -10: return -10 + depth
        if self.is_full(board): return 0

        if is_ai_turn:
            best_score = -100
            for i in range(9):
                if board[i] == self.EMPTY:
                    board[i] = self.AI
                    score = self._recursive_solve(board, depth + 1, False)
                    board[i] = self.EMPTY
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = 100
            for i in range(9):
                if board[i] == self.EMPTY:
                    board[i] = self.PLAYER
                    score = self._recursive_solve(board, depth + 1, True)
                    board[i] = self.EMPTY
                    best_score = min(best_score, score)
            return best_score

    def check_winner(self, board):
        lines = [
            board[0:3], board[3:6], board[6:9],
            board[0::3], board[1::3], board[2::3],
            board[0::4], board[2:7:2]
        ]
        for line in lines:
            if line[0] == line[1] == line[2] and line[0] != self.EMPTY:
                if line[0] == self.AI: return 10
                if line[0] == self.PLAYER: return -10
        return 0

    def is_full(self, board):
        return not any(tile == self.EMPTY for tile in board)