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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("Schelling’s model of segregation")
 
        self.label = QLabel("Copy and paste an Amazon URL here:", self)
        self.label.setFont(QFont("courier new"))

        button = QPushButton("Go")
        button.clicked.connect(start_game)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(button)

        self.setLayout(vbox)
        self.setGeometry(500, 500, 550, 100)

    def update(self, m):
        self.label.setText("Fish")

def display_map(m):
    s_list = []
    for l in m:
        s_list.append(''.join(l))
    window.label.setText("\n".join(s_list))

def print_map(m):
    n_i = len(m)
    n_j = len(m[0])
    print('-' * (n_j+2))
    for l in m:
        print('|' + ''.join(l) + '|')


def neighbors(m, i, j):
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

def build_map():
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

def move(m, i, j, n_o_max=99, n_x_max=99):
    # Setting the n_o_max to 99 means don't care.
    n_i = len(m)
    n_j = len(m[0])
    for _ in range(90):
        ii = randrange(0, n_i)
        jj = randrange(0, n_j)
        n_o, n_x, _ = neighbors(m, ii, jj)
        if m[ii][jj] == ' ' and n_o <= n_o_max and n_x <= n_x_max:
            m[i][j], m[ii][jj] = m[ii][jj], m[i][j]
            break

def tick(m, threshold):
    n_i = len(m)
    n_j = len(m[0])

    move_intended = 0

    for i, j in product(range(n_i), range(n_j)):
        n_o, n_x, _ = neighbors(m, i, j)
        # print(f"{i=}, {j=}, {n_o=}, {n_x=}, {n_space=}")

        # The number of neighbors is 8 at max.
        if m[i][j] == 'o' and n_x > threshold:
            # n_x+1 means
            ## OK to move to somewhere a little worse
            ## It helps explore better overall pattern
            ## by don't stuck in a local minimal.
            move(m, i, j, n_x_max=n_x+1)

            # n_x means
            ## move somewhere at least as good
            # move(m, i, j, n_x_max=n_x)

            move_intended += 1
        if m[i][j] == 'x' and n_o > threshold:
            move(m, i, j, n_o_max=n_o+1)
            # move(m, i, j, n_o_max=n_o)

            move_intended += 1
    return move_intended

def start_game():
    for threshold in range(4, -1, -1):
        # for n_iter in range(1000):
        for n_iter in range(1):
            if tick(m, threshold) < 4*threshold:
                # Break early and tighten the threshold
                # in the next iteration if no much move.
                print(f"n_iter={n_iter}")
                break
        print()
        print()
        print(threshold)
        # print_map(m)
        display_map(m)
        threshold -= 1

app = QApplication(sys.argv)
window = Window()

m = build_map()
# print_map(m)
display_map(m)

window.show()

sys.exit(app.exec())

# def main():
#     app = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()