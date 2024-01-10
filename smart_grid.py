# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # new dictionary maken
data_district1 = {}

csv_file = '/Users/antoniovandijck/Downloads/Huizen&Batterijen/district_1/district-1_batteries.csv'

with open(csv_file, 'r') as file:

    csv_reader = csv.reader(file)

    next(csv_reader)
    
    for row in csv_reader:

        positie = map(int, row[0].split(','))
        
        capaciteit = row[1]

        data_district1[tuple(positie)] = capaciteit

print(data_district1)