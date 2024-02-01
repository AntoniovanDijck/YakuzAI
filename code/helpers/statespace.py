# statespace.py
# Antonio, Mec, Vincent
# YakuzAI

#Simple statespace which only calculates how many different connections (only amount) there can be per battery given a max 
#amount of connections 
def simple_state_space(houses, batteries, max_connections_per_battery):
    """
    Calculates the amount of possible connections given a certain amount of houses and batteries
    
    """
    if batteries == 0:
        if houses == 0:
            return 1
        else:
            return 0
    
    # If there are more houses than batteries * max_connections_per_battery, there are no possible connections
    if houses > batteries * max_connections_per_battery:

        #return 0
        return 0
    
    count = 0

    # For every possible amount of connections
    for i in range(min(houses, max_connections_per_battery)+1):
        count += simple_state_space(houses - i, batteries - 1, max_connections_per_battery)
    
    return count

state_space = simple_state_space(150, 5, 50)
print(state_space)
        
# Cable state space
counter = 0
for i in range (10):
    counter += (i+3)**2

# Battery state space
print(counter*2) 
