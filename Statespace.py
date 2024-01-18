

#Simple statespace which only calculates how many different connections (only amount) there can be per battery given a max 
#amount of connections 
def simple_state_space(houses, batteries, max_connections_per_battery):
    if batteries == 0:
        if houses == 0:
            return 1
        else:
            return 0
        
    if houses > batteries * max_connections_per_battery:
        return 0
    
    count = 0

    for i in range(min(houses, max_connections_per_battery)+1):
        count += simple_state_space(houses - i, batteries - 1, max_connections_per_battery)
    
    return count

state_space = simple_state_space(150, 5, 50)
print(state_space)
        
