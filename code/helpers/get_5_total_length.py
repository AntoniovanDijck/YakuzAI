# Smart_grid.py
# Antonio, Mec, Vincent
# YakuzAI

def get_5_total_length(batteries):
    total_cable_length = 0
    
    battery_list = list(batteries.values())[:5]
    for battery in battery_list:
        #get first 50 batteries
        for cable in battery.cables:
            total_cable_length += cable.length
    
    return total_cable_length