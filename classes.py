import numpy as np
import csv
#Main classes for github
# Antonio, Mec, Vincent
# YakuzAI

class Object():
    def __init__(self, pos_x, pos_y, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = "black"

class House(Object):
    def __init__(self, pos_x, pos_y, color):
        super.__init__(pos_x, pos_y, color)
