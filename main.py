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
from code.helpers.visualize import visualize
from code.algorithm.nearest_object import nearest_object
from code.algorithm.nearest_battery import nearest_battery

#Creators: Team YakuzAI

def main():
        ### Drawing cables for all districts
    districts_houses = ['data/Huizen&Batterijen/district_1/district-1_houses.csv', 'data/Huizen&Batterijen/district_2/district-2_houses.csv', 'data/Huizen&Batterijen/district_3/district-3_houses.csv']
    districts_batteries = ['data/Huizen&Batterijen/district_1/district-1_batteries.csv', 'data/Huizen&Batterijen/district_2/district-2_batteries.csv', 'data/Huizen&Batterijen/district_3/district-3_batteries.csv']
 
    #Iterations for animation
    iterations = 50

    # for each district
    for i in range(0, 3):
        print(f'District {i+1}')
        # set up experiment
        experiment = District(districts_houses[i], districts_batteries[i])
        random_instance = nearest_battery(experiment)
        random_instance.connect_houses_to_batteries()
        experiment.calculate_totals()
        
         # check experiment
        output_data = experiment.check_50()



        # # export to json file this can be muted
        # with open(f'data/output_data/district_{i+1}_output-{datetime.datetime.now():%Y-%m-%d-%H:%M}.json','w') as outfile:
        #     json.dump(output_data, outfile)
        
        # fig, ax = plt.subplots(figsize=(12, 12))
        # #visualization / animation, this can be muted
        # for n in range(iterations): 
        #     experiment = District(districts_houses[i], districts_batteries[i])
        #     random_instance = nearest_battery(experiment)
        #     random_instance.connect_houses_to_batteries()
        #     experiment.calculate_totals()
        #     frame_fig, frame_ax = visualize(experiment, n)
        #     frames.append([frame_ax])

if __name__ == "__main__":
    main()