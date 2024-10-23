import hlt
from hlt import EAST, NORTH, SOUTH, STILL, WEST, Move

myID, game_map = hlt.get_init()


# used to log messages to a file while debugging
def log(msg):
    with open("app.log", "a") as f:
        f.write(msg + "\n")
    

def find_nearest_enemy_direction(square, map_copy):
    direction = STILL
    # to avoid getting stuck in an infinite loop
    # the map WRAPS ARROUND!
    max_distance = min(map_copy.width, map_copy.height) / 2
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square

        while current.owner == myID and distance < max_distance:
            distance += 1
            current = map_copy.get_target(current, d)

        if distance < max_distance:
            target = map_copy.get_target(square, d)
            if target.owner != myID or overflows(square, target) is False:
                direction = d
                max_distance = distance
            else:
                direction = STILL

    return direction


def heuristic(square, map_copy):
    if square.owner == 0 and square.strength > 0:
        return square.production
    elif square.owner != myID:
        # return total potential damage caused by overkill when attacking this square
        total_strength = square.strength
        for neighbor in map_copy.neighbors(square):
            if neighbor.owner not in (0, myID):
                total_strength += neighbor.strength
        return total_strength
    

def calculate_effectiveness(square):
    if square.strength == 0:
        return square.production * square.production
    return (square.production * square.production) / square.strength



def overflows(square, target):
    if target.strength + square.strength > 265:
        # punem un prag mai intal de overflow ca sa evitam blocuri blocante
        return True
    return False

# returns the first direction to move to get from square to target
# takes into account that if multiple directions are possible,
# the one with the highest effectiveness is chosen
def find_path_to_target(square, target, map_copy):
    distNorth, distSouth, distEast, distWest = 0, 0, 0, 0
    targets = [game_map.get_target(square, NORTH), game_map.get_target(square, SOUTH),
                game_map.get_target(square, EAST), game_map.get_target(square, WEST)]
    distNorth = map_copy.get_distance(targets[0], target)
    distSouth = map_copy.get_distance(targets[1], target)
    distEast = map_copy.get_distance(targets[2], target)
    distWest = map_copy.get_distance(targets[3], target)

    minDistance = min(distNorth, distSouth, distEast, distWest)

    distances = [distNorth, distSouth, distEast, distWest]
    directionsPossible = [NORTH, SOUTH, EAST, WEST]
    i = 0
    counter = 0
    result = []
    while i < 4:
        if distances[i] == minDistance:
            result.append(directionsPossible[i])
            counter += 1
        i += 1

    if counter == 1:
        return result[0]
    else:
        if(calculate_effectiveness(targets[0]) > calculate_effectiveness(targets[1])):
            if overflows(square, targets[0]):
                if overflows(square, targets[1]):
                    return STILL
                else: 
                    return result[1]
            else:
                return result[0]
        else:
            return result[1]


    
    
