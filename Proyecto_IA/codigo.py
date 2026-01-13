import sys
import random
import numpy as np
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt
import tensorflow as tf

# Cargar el modelo entrenado
MODEL_PATH = "tictactoe_ia.h5"
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

class TicTacToeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TicTacToe")
        self.setFixedSize(300, 300)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.buttons = []
        self.AI_MARKER = [0, 0, 1]
        self.PLAYER_MARKER = [0, 1, 0]
        self.EMPTY_MARKER = [1, 0, 0]
        self.state_size = 27
        self.reset_board()
        self.init_ui()
        self.start_game()

    def reset_board(self):
        self.board = [list(self.EMPTY_MARKER) for _ in range(9)]
        self.game_over = False
        self.turn = None  # 'user' o 'ai'

    def init_ui(self):
        self.buttons = []
        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(80, 80)
            font = QFont()
            font.setPointSize(20)
            btn.setFont(font)
            btn.clicked.connect(lambda checked, idx=i: self.handle_click(idx))
            self.layout.addWidget(btn, i // 3, i % 3)
            self.buttons.append(btn)

    def start_game(self):
        self.reset_board()
        self.update_ui()
        self.turn = random.choice(["user", "ai"])
        if self.turn == "ai":
            self.ai_move()

    def handle_click(self, idx):
        if self.game_over or self.turn != "user":
            return
        if self.board[idx] != self.EMPTY_MARKER:
            return
        self.board[idx] = list(self.PLAYER_MARKER)
        self.update_ui()
        if self.check_winner(self.PLAYER_MARKER):
            self.end_game("¡Ganaste!")
            return
        if self.is_full():
            self.end_game("Empate")
            return
        self.turn = "ai"
        self.ai_move()

    def ai_move(self):
        if self.game_over:
            return
        state = np.array(self.board).flatten().reshape(1, self.state_size)
        act_values = model.predict(state, verbose=0)
        action = np.argmax(act_values[0])
        # Si la casilla está ocupada, buscar la siguiente libre
        if self.board[action] != self.EMPTY_MARKER:
            free = [i for i, v in enumerate(self.board) if v == self.EMPTY_MARKER]
            if free:
                action = random.choice(free)
            else:
                self.end_game("Empate")
                return
        self.board[action] = list(self.AI_MARKER)
        self.update_ui()
        if self.check_winner(self.AI_MARKER):
            self.end_game("¡La IA ganó!")
            return
        if self.is_full():
            self.end_game("Empate")
            return
        self.turn = "user"

    def update_ui(self):
        for i, btn in enumerate(self.buttons):
            if self.board[i] == self.AI_MARKER:
                btn.setText("X")
            elif self.board[i] == self.PLAYER_MARKER:
                btn.setText("O")
            else:
                btn.setText("")

    def check_winner(self, marker):
        b = self.board
        win_patterns = [
            [0,1,2],[3,4,5],[6,7,8], # filas
            [0,3,6],[1,4,7],[2,5,8], # columnas
            [0,4,8],[2,4,6]          # diagonales
        ]
        for pattern in win_patterns:
            if all(b[i] == marker for i in pattern):
                return True
        return False

    def is_full(self):
        return all(cell != self.EMPTY_MARKER for cell in self.board)

    def end_game(self, message):
        self.game_over = True
        QMessageBox.information(self, "Fin de la partida", message)
        self.start_game()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicTacToeGUI()
    window.show()
    sys.exit(app.exec())