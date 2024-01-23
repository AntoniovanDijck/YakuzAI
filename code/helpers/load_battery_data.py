# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def load_battery_data(filename):
    '''
    reads the csv file and returns a dictionary with the positions of the batteries and their capacity

    '''

    # # create new dict
    battery_data = {}

    with open(filename, 'r') as f:

        csv_reader = csv.reader(f)

        # skip the header
        next(csv_reader)
        
        for row in csv_reader:

            position = map(int, row[0].split(','))
            
            capacity = row[1]

            battery_data[tuple(position)] = float(capacity)

    return battery_data