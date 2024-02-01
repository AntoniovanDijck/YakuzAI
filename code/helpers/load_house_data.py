# load_house_data.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def load_house_data(house_data):
    """
    reads the csv file and returns a dictionary with the x and y positions of the houses and their max output

    """

    house_dict = {}

    with open(house_data, 'r') as file:
            
            reader = csv.reader(file)
    
            # skip the header
            next(reader)
            
            for row in reader:
    
                x = row[0]
                y = row[1]
                maxoutput = row[2]
    
                house_dict[tuple((int(x),int(y)))] = float(maxoutput)

    return house_dict