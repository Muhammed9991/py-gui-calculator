#!/usr/bin/env python3

# Filename: pycalc.py

'''
Simple calculator created using PyQt5
'''

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

# Used to create buttons and layout of calculator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

# Adding functionality when buttons pressed
from functools import partial

# Global error message
ERROR_MSG = 'ERROR'

# Subclass of QMainWindow. Setting up calculator GUI
class PyCalcGui(QMainWindow):
    
    def __init__(self):
        
        super().__init__() #View initialisation

        self.setWindowTitle('Calculator') #Widget Title
        self.setFixedSize(235,235)

        # Seeting central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self._centralWidget.setLayout(self.generalLayout)

        # Creating the display and buttons
        self._createDisplay()
        self._createButtons() 
    

    def _createDisplay(self):
        # Create the display widget
        self.display = QLineEdit()

        # Set some display's properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)
    

    def _createButtons(self):
        # Empty dictionary to store calculator buttons
        self.buttons = {}
        # Temp dictionary to store labels and position of each button
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                  }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)

        # Adding methods for each function of a calculator

    ''' Function updates text on the calculator screen '''
    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    '''Getter function. Returns displays current text'''
    def displayText(self):
        return self.display.text()

    ''' Sets display to empty string '''
    def clearDisplay(self):
        self.setDisplayText('')

    
# Create a Model to handle the calculator's operation
def evaluateExpression(expression):
    '''
    NOT the most secure way to do this. General adivce is to only use eval()
    on trusted inputs. But as example code. This should suffice.
    '''
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG

    return result

# Create a Controller class to connect the GUI and the model
class PyCalcCtrl:
    
    def __init__(self, model , view):
        
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    ''' Handles creation of maths expression '''
    def _buildExpression(self, sub_exp):

        expression = self._view.displayText() + sub_exp
        # Updates screen with expression
        self._view.setDisplayText(expression)

        # Invalid input e.g. 0/0 clears display
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

    ''' Connecting printable buttons with function _buildExpression '''
    def _connectSignals(self):

        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        # Connecting '=' to calculating equal result function
        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        # Connecting 'C' to clear display
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
    
    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)


'''Main Function'''
def main():
    # Creating an instance of QApplication
    pycalc = QApplication(sys.argv)

    # Displaying calc GUI
    view = PyCalcGui()
    view.show()

    # Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)

    # Executing main loop
    sys.exit(pycalc.exec())


if __name__ == '__main__':
    main()
