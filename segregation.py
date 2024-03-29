#!/usr/bin/env python3

from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton,
    QLabel, 
    QTextEdit,
    QVBoxLayout,
    )
from PyQt6.QtGui import QFont
import sys

from random import shuffle, randrange
from itertools import product

class game_board:
    def __init__(self):
        self.m = self._build_map()
        self.threshold = 4
        # Parameters
        #     Threshold
        #     Map size
        #     % filled up
        #     -> become num of x and num of o
        #     # of iterations

    def _build_map(self):
        n_i = 20
        n_j = 40

        m = [[' '] * n_j for _ in range(n_i)]

        rand_position = [(i, j) for i in range(n_i) for j in range(n_j)]
        shuffle(rand_position)

        n = n_i * n_j
        percent = int(n*48/100)

        for p in range(percent):
            m[rand_position[p][0]][rand_position[p][1]] = 'o'
        for p in range(percent, percent*2):
            m[rand_position[p][0]][rand_position[p][1]] = 'x'

        return m

    def _neighbors(self, m, i, j):
        n_i = len(m)
        n_j = len(m[0])

        counter = {}
        counter['o'] = 0
        counter['x'] = 0
        counter[' '] = 0

        for ii, jj in [(i+1, j), (i-1, j), (i, j+1), (i, j-1), (i+1, j+1), (i-1, j+1), (i+1, j-1), (i-1, j-1), ]:
            if ii < 0 or ii > n_i-1 or jj < 0 or jj > n_j-1:
                continue
            counter[m[ii][jj]] += 1

        return counter['o'], counter['x'], counter[' ']


    def _move(self, m, i, j, n_o_max=99, n_x_max=99):
        # Setting the n_o_max to 99 means don't care.
        n_i = len(m)
        n_j = len(m[0])
        for _ in range(90):
            ii = randrange(0, n_i)
            jj = randrange(0, n_j)
            n_o, n_x, _ = self._neighbors(m, ii, jj)
            if m[ii][jj] == ' ' and n_o <= n_o_max and n_x <= n_x_max:
                m[i][j], m[ii][jj] = m[ii][jj], m[i][j]
                break

    def tick(self):
        n_i = len(self.m)
        n_j = len(self.m[0])

        move_intended = 0

        for i, j in product(range(n_i), range(n_j)):
            n_o, n_x, _ = self._neighbors(self.m, i, j)
            # print(f"{i=}, {j=}, {n_o=}, {n_x=}, {n_space=}")

            # The number of neighbors is 8 at max.
            if self.m[i][j] == 'o' and n_x > self.threshold:
                # n_x+1 means
                ## OK to move to somewhere a little worse
                ## It helps explore better overall pattern
                ## by don't stuck in a local minimal.
                self._move(self.m, i, j, n_x_max=n_x+1)
                # move(m, i, j)

                # n_x means
                ## move somewhere at least as good
                # move(m, i, j, n_x_max=n_x)

                move_intended += 1
            if self.m[i][j] == 'x' and n_o > self.threshold:
                self._move(self.m, i, j, n_o_max=n_o+1)
                # move(m, i, j)

                move_intended += 1
        return move_intended

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("Schelling’s model of segregation")
 
        self.label = QLabel()
        self.label.setFont(QFont("courier new"))

        button = QPushButton("Go")
        # button.setDefault(True)
        button.clicked.connect(self.game_go)

        self.parameters = QTextEdit()
        self.parameters.setText("threshold:4")
        self.parameters.textChanged.connect(self.update_parameters)

        vbox = QVBoxLayout()
        vbox.addWidget(self.parameters)
        vbox.addWidget(self.label)
        vbox.addWidget(button)

        self.setLayout(vbox)
        self.setGeometry(500, 500, 550, 100)

        # TODO:
        # Control from keyboard.
        # Example: enter would press a button.
        # Now it gives no response.

    
    def register_game(self, game):
        self.game = game
        self.update_map()

    def update_map(self):
        s_list = []
        for l in self.game.m:
            s_list.append(''.join(l))
        self.label.setText("\n".join(s_list))

    def game_go(self):
        self.update_parameters()
        self.game.tick()
        self.update_map()

    def update_parameters(self) -> None:
        parameter_dict = {}
        parameter_str = self.parameters.toPlainText()
        try:
            parameters = parameter_str.split(';')
            for s in parameters:
                k, v = s.split(':')
                k = k.strip()
                v = v.strip()
                parameter_dict[k] = v
            print(parameter_dict)
        except ValueError:
            print(f"malformed parameter string {parameter_str}")
            return

        try:
            if "threshold" in parameter_dict:
                self.game.threshold = int(parameter_dict["threshold"])
        except ValueError as e:
            print(f"malformed parameter {parameter_dict}")
            print(f"{e}")
            return
        


def main():
    game = game_board()

    app = QApplication(sys.argv)
    window = Window()
    window.register_game(game)

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()