import json
import csv
import random
import datetime
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import code.classes.house
import code.classes.cable 
import code.classes.battery
from code.classes.district import District
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.nearest_object_rand import nearest_object_rand
from code.algorithm.nearest_object_x import nearest_object_x
from code.algorithm.nearest_object_y import nearest_object_y
from code.helpers.visualize import visualize
from code.algorithm.nearest_battery import nearest_battery
from code.algorithm.dijckstra import dijckstra
from code.experiments.experiment2 import experiment2
from code.experiments.experiment1 import experiment

#Creators: Team YakuzAI

def main():
    ### Drawing cables for all districts
    districts_houses = ['data/Huizen&Batterijen/district_1/district-1_houses.csv', 'data/Huizen&Batterijen/district_2/district-2_houses.csv', 'data/Huizen&Batterijen/district_3/district-3_houses.csv']
    districts_batteries = ['data/Huizen&Batterijen/district_1/district-1_batteries.csv', 'data/Huizen&Batterijen/district_2/district-2_batteries.csv', 'data/Huizen&Batterijen/district_3/district-3_batteries.csv']
    
    #Iterations for simulate    
    iterations = 10

    # for each district
    for i in range(0, 1):
        print(f'District {i+1}')

        # set up experiment To test all algorithms
        experiment(districts_houses[i], districts_batteries[i], iterations)    
    
        
        
        # check experiment
        # output_data = experiment.check_50()
       

if __name__ == "__main__":
    main()