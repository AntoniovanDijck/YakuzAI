
# YakuzAI Smart Grids![YakuzAI Logo](data/assets/smart_grids1.png)

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Detailed Usage](#detailed-usage)
   - [Running the Script](#running-the-script)
- [Project Structure](#project-structure)
- [Customization Guide](#customization-guide)
- [How to Contribute](#how-to-contribute)
  - [Contributing Steps](#contributing-steps)
  - [Guidelines](#guidelines)
- [Community & Support](#community--support)
- [License](#license-)
- [Acknowledgments](#acknowledgments)

## Overview

YakuzAI's Smart Grid project is a project that aims to connect houses to batteries in a smart way. The project is part of the course Algorithms & Heuristics at the University of Amsterdam. The goal of the project is to connect houses to batteries in a smart way, so that the costs of the connections are as low as possible. This is done by using different algorithms and heuristics to test which one is the most efficient for connecting the houses to the batteries. We have used the following algorithms and heuristics to test which one is the most efficient for connecting the houses to the batteries. 

## Algorithms
- Random algorithm
- Greedy Object algorithm
- Hillclimber algorithm
- Dijkstra variation algorithm

## Heuristics:

- Manhattan distance
- Random houses selection
- Random batteries selection
- Random houses and batteries selection
- Random path selection
- Distance to battery
- Distance to battery and capacity

## Key Features

- **Reading the data**: Intelligently reading the data from the data sets.
- **Connecting the houses**: Connecting the houses to the batteries with different algorithms.
- **Calculating the costs**: Calculating the costs of the connections.
- **Testing the algorithms**: Testing the algorithms with different heuristics.
- **Comparing the algorithms**: Comparing the algorithms with each other using histograms.
- **Running the Experiments**: Running the experiments with the algorithms and heuristics.
- **Plotting the results**: Plotting the results in a graph and grid visualizations.
- **Saving the results**: Saving the results in a JSON file and visualizations in PNG.
- **Recreating the visualisation**: Creating a visualisation of the grid with the connections.
- **Histograms**: A histogram of the costs of the algorithms.


## Getting Started

### Prerequisites

- Python 3.6+
- Advanced understanding of Python
- Advanced knowledge of algorithms and machine learning
- New to Python? Check out [this guide](https://www.proglab.nl) to get started.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AntoniovanDijck/YakuzAI.git
   cd YakuzAI
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Detailed Usage

### Running the Main Script
By running the main.py file, the program will run the default algorithms and with their default heuristics. The results will be saved in the output_data folder and the simulation will run 100 iterations by default.

```bash
python main.py
```

It is also possible to run the main.py file with different input. by speciyfing adding -i, -d and -a to the command line, the user can change the input of the iterations and the district and the algorithms with different heuristics. 

### Example Usage:

When running the main.py file with the flags, the user can choose which algorithm, iteration and district will be used for the run. 

```bash
python main.py --iterations 200 --district 2 --algorithm all
```

- The user can choose between the following algorithms: `RandomAlgorithm`, `Greedy_Object` and `Dijckstra`. The hill_climber will be run on the district with the lowest cost of the algorithms. 

- Whenever you want to see another heuristic in action choose the algorithm `Greedy_Object_Distance_Randomized`, `Greedy_Object_Distance_Reversed`.

- To compare all the algorithms with each other, choose for the algorithm `all`.

- For the --district flag the user can choose between the following districts: `1`, `2` and `3`. 

- For the --iterations flag the user can choose between the following iterations: `1`, `10`, `100`, `1000`, `10000` and `100000`.

advanced usage:

```bash
python main.py --iterations 10000 --district 3 --algorithm all
```


## Project Structure 
- `code folder`: contains the folders for helpers and classes
- `code/algorithm folder`: This folder contains the algorithm classes
- `code/classes folder`: This folder contains classes for houses, batteries, cables and districts.
- `code/experiments folder`: This folder contains helper functions for the visualisations and additional functions.
- `code/helpers folder`: This folder contains helper functions for the visualisations and additional functions.
- `data folder`: This folder contains data for the visualisation, output and input data.
- `data/Huizen&Batterijen/`: Conatins the Datasets used for the positions and battery capacities per district.
- `data/output_data/`: This folder contains the simulation results and the output JSON files.
- `notebooks folder`: This folder contains Jupyter notebooks with the demo's of the project.
- `main.py`: Main script.
- `README.md`: The file you're reading.
- `requirements.txt`: Dependencies.


## Main Classes

| Classes                | Description                              |
| ---------------------- | ---------------------------------------- |
| House                  | x value, y value, connections, route.    | 
| Battery                | Battery capacity, x value, y value,.     | 
| Cable                  | Length, x value, y value, connected      |
| District               | Connected, houses, batteries, cables.    | 

### Main.py
By running the main.py file, the program will run the algorithms and with their following heuristics. The results will be saved in the output_data folder. The results will be saved in a JSON file and the visualisations will be saved in a PNG file.
In the main.py file, the following functions are called:
- `find_lowest_cost_experiment`: This function runs the experiment with the input algorithms and return the district with the lowest resulting cost and saves a hsitorgram of the costs of the algorithms and a plot of the grid with the most efficient connections.
- `hill_climber_experiment`: This function runs the experiment with the input lowest district from the `find_lowest_cost_experiment` function and runs the hill climber algorithm on the district. The function returns the district with the lowest resulting cost and shows a line graph of the costs of the hillclimber and a plot of the grid with the most efficient connections will be saved at the end.

## Customization Guide
By changing the input of the main.py file, the user can change the input of the algorithms and heuristics. The user can change the input of the algorithms and heuristics by changing the following variables: 
- `district_number`: The district number of the district that will be used for the algorithms and heuristics.
- `algorithm`: The algorithm that will be used for the experiment. The user can choose between the following algorithms: `RandomAlgorithm`, `Greedy_Object`, `HillClimber` and `Dijckstra`.
- `heuristic`: The heuristic that will be used for the experiment. The user can choose between the following heuristics: , `random_houses`, `Greedy_distance`, `Random_Path`, `Greedy_Object_Randomized` and `Greedy_Object_Reversed`.
- `iterations`: The number of iterations that will be used for the experiment. The user can choose between the following iterations: `1`, `10`, `100`, `1000`, `10000` and `100000`.

## Algorithms
- `RandomAlgorithm`: This algorithm connects the houses to the batteries in a random way. The way it works is by randomly selecting a house and a battery and connecting them first on the x-axis and then on the y-axis. If the battery is full, the algorithm will select another battery. If the house is connected to a battery, the algorithm will select another house. The algorithm will stop when all the houses are connected to a battery. This algorithm is not very efficient, because it does not take the distance between the houses and the batteries into account results in very high costs.

- `Greedy_Object_Distance`: This algorithm connects the houses to the batteries in a more intuitive way. The way it works is by selecting the house with the highest output and connecting it to the closest battery. If the battery is full, the algorithm will select another battery. If the house is connected to a battery, the algorithm will select another house. The algorithm will stop when all the houses are connected to a battery. This algorithm is more efficient than the random algorithm, because it takes the distance between the houses and the batteries into account but still chooses the x-axis first and then the y-axis and result in high costs but lower than the random algorithm.

- `Greedy_Battery_Distance`: This algorithm connects houses to battery based on the distance of each battery to the houses. The way it works is by selecting the house with the highest output and connecting it to the closest battery. If the battery is full, the algorithm will select another battery. If the house is connected to a battery, the algorithm will select another house. The algorithm will stop when all the houses are connected to a battery. This algorithm is more efficient than the random algorithm, because it takes the distance between the houses and the batteries into account but still chooses the x-axis first and then the y-axis and result in high costs but lower than the random algorithm.

- `Dijckstra`: This algorithm connects the houses to the batteries in a most efficient way, this algorithm connects to houses the same way as the former algorithms but in stead of just taking a step in a random direction or first x or y, it takes the shortest path to the battery or cable by calculating the distance on the x and y-axis the shortest distance will get a cable. This algorithm is the most efficient algorithm of the four algorithms, because it takes the distance between the houses and the batteries into account and chooses the shortest path to the battery and results in the lowest costs for our use case.

- `HillClimber`: This algorithm uses functions from Dijckstra to optimize the connections between the houses and the batteries. The way it works is by selecting a houses based on the depth and disconnecting them and checking if there is a better connection possible. If there is a better connection possible, the algorithm will connect the house to the battery. If there is no better connection possible, the algorithm will select another house. The algorithm will stop when all the houses are connected to a battery. This algorithm is used to optimize the results of the best result from another algorithm

## Heuristics
To test different heuristics, we have made the following changes to the Greedy Object algorithm to compare the results of the algorithms with each other and to see which heuristic is the most efficient for our use case, the best ones are used in the following algorithm Dijckstra and Hillclimber. The following algorithms contain the following heuristics:

Algorithm: `Greedy_Object_Distance`
reversed_step: the algorithm first chooses the x-axis and then the y-axis when connecting the houses to the batteries.

Algorithm: `Greedy_Object_Distance_Randomized`
random_step: The algorithm randomly chooses the x-axis or the y-axis when connecting the houses to the batteries.

Algorithm: `Greedy_Object_Distance_Reversed`
reversed_step: the algorithm first chooses the y-axis and then the x-axis when connecting the houses to the batteries.

## Results
After running our simulation for each district with the different algorithms and heuristics, we have found the following results:
The best overall performing algorithm is the Dijckstra for each district, resulting in a 32000 average costs overall. After running an hillclimber on the best district the best resulting cost was 29000 on average. 


## How to Contribute

### Contributing Steps

1. **Clone the Repository**
2. **Add Your Changes**
3. **Commit Your Changes**
4. **Push to the Branch**

### Guidelines

- Code must follow the project's style and standards.
- Clear, commented, and testable code is essential.
- Documentation updates are appreciated.

## Community & Support

- **Forum**: [Join discussions](https://student.uva.nl)
- **FAQs**: [Common questions](https://www.uva.nl/onderwijs/bachelor/inschrijven/doe-mee-aan-uva-matching/veelgestelde-vragen/veelgestelde-vragen.html)

## License ![License Badge](https://img.shields.io/badge/License-Hippocratic_3.0-lightgrey.svg)

This project is licensed under the UvA License - see the [LICENSE](https://uba.uva.nl/en/support/open-data/licences/licences.html) page for details.

## Acknowledgments

- Special thanks to all our contributors and the open-source community. 
