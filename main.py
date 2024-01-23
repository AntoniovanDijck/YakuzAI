import json
import csv
import numpy as np
import random
import datetime
import code.classes.house
import code.classes.cable 
import code.classes.battery
import code.helpers.smart_grid 
from code.classes.district import District
from code.algorithm.random_alg import RandomAlgorithm
from code.algorithm.greedy import Greedy
from code.helpers.visualize import visualize


def main():
        ### Drawing cables for all districts
    districts_houses = ['data/Huizen&Batterijen/district_1/district-1_houses.csv', 'data/Huizen&Batterijen/district_2/district-2_houses.csv', 'data/Huizen&Batterijen/district_3/district-3_houses.csv']
    districts_batteries = ['data/Huizen&Batterijen/district_1/district-1_batteries.csv', 'data/Huizen&Batterijen/district_2/district-2_batteries.csv', 'data/Huizen&Batterijen/district_3/district-3_batteries.csv']
 
    # for each district
    for i in range(0, 3):
        print(f'District {i+1}')
        # set up experiment
        experiment = District(districts_houses[i], districts_batteries[i])
        random_instance = Greedy(experiment)
        random_instance.connect_houses_to_batteries()
        experiment.calculate_totals()
        
         # check experiment
        output_data = experiment.check_50()



        # export to json file
        with open(f'data/output_data/district_{i+1}_output-{datetime.datetime.now():%Y-%m-%d-%H:%M}.json','w') as outfile:
            json.dump(output_data, outfile)

        visualize(experiment, i+1)
    
    
if __name__ == "__main__":
    main()