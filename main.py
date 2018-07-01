#!/usr/bin/env python

"""
Создать программу, позволяющую вычислять систему линейных уравнений. 
"""

__author__ = "___Kalinina ___"
__copyright__ = "___Copyright 2018, Kalinina Ariana"
__email__ = "__rishkolin@gmail.com___"

import sys

import numpy
from numpy.linalg import solve

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QDesktopWidget, QHBoxLayout, QGridLayout

class Solver(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # clear grid layout from widgets
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # create data grid and results grid
    def create_grid(self, n):
        self.clear_layout(self.coeffs)
        self.coeffs_data = [[None for i in range(0,n+1)] for i in range(0,n)]
        for row in range(0,n):
            for col in range(0,2*n+1):
                #labels in odd columns
                label_text = f"*x{int((col+1)/2)}"
                if col==2*n-1:
                    label_text+="="
                else:
                    label_text+="+"
                lab = QLabel(label_text)
                coeff = QLineEdit()

                if col % 2:
                    self.coeffs.addWidget(lab, row, col)
                else:
                    self.coeffs_data[row][int(col/2)]=coeff
                    self.coeffs.addWidget(coeff, row, col)

        # fill the result grid (and save widgets reference for later)
        self.results_widget = [None for i in range(0,n)]
        for row in range(0,n):
            self.results.addWidget(QLabel(f"x{row+1}="), row, 0)
            result_label = QLabel("")
            self.results_widget[row] = result_label
            self.results.addWidget(result_label, row, 1)

    def initUI(self):
        # set size
        self.resize(600,400)
        # move to center
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())
        # window title
        self.setWindowTitle('Linear Solver')

        label = QLabel("Введите количество переменных")
        label.move(10,10)

        self.n_field = QLineEdit()
        self.n_field.resize(self.n_field.sizeHint())

        applySize = QPushButton('Применить')
        applySize.resize(applySize.sizeHint())
        applySize.clicked.connect(self.apply_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.n_field)
        hbox.addWidget(applySize)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.coeffs = QGridLayout()
        vbox.addLayout(self.coeffs)

        solveButton = QPushButton('Решить')
        solveButton.resize(solveButton.sizeHint())
        solveButton.clicked.connect(self.solver)
        vbox.addWidget(solveButton)

        self.results = QGridLayout()
        vbox.addLayout(self.results)

        self.setLayout(vbox)
        self.show()

    # create grids
    def apply_clicked(self):
        self.create_grid(int(self.n_field.text()))

    # solve with numpy
    def solver(self):
        n = int(self.n_field.text())
        a = numpy.zeros((n,n))
        b = numpy.zeros((n))
        for row in range(0,n):
            for col in range(0,n+1):
                if col==n:
                    # right part
                    b[row] = float(self.coeffs_data[row][col].text())
                else:
                    a[row][col] = float(self.coeffs_data[row][col].text())
        res = solve(a,b)
        for row in range(0,n):
            self.results_widget[row].setText(str(res[row]))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    solver = Solver()
    sys.exit(app.exec_())


  
