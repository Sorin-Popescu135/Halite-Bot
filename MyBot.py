import copy
from MyBotHelpers import * 
import hlt
from hlt import EAST, NORTH, SOUTH, STILL, WEST, Move

hlt.send_init("Spectra")

def get_move(square, map_copy):
    # square too weak to think of any advantageous move so just wait
    if square.strength < square.production * 5 or square.strength < 5:
        return Move(square, STILL)
    
    # check if strength is maxed out
    if square.strength + square.production >= 255:
        return Move(square, find_nearest_enemy_direction(square, map_copy))
    
    # check the neighbors from 3 moves away
    best_effectiveness = None
    target = None
    enemy_close = False
    for neighbor in map_copy.neighbors(square, 3):
        if neighbor.owner == 0:
            # check the efffectiveness of the attack
            move_effectiveness = calculate_effectiveness(neighbor)
            if target is None or move_effectiveness > best_effectiveness:
                best_effectiveness = move_effectiveness
                target = neighbor
        elif neighbor.owner != myID:
            # means we have an enemy nearby
            enemy_close = True
            break

    if enemy_close is False:
        if target is not None:
            # means we have at least one neutral cell nearby
            if target.strength < square.strength:
                return Move(square, find_path_to_target(square, target, map_copy))
            else:
                return Move(square, STILL)
        else:
            # we can't attack anything, so go to nearest edge   
            return Move(square, find_nearest_enemy_direction(square, map_copy))
    else:
        # we have an enemy nearby, so calculate the best move
        target = None
        best_direction = None
        max_heuristic = -1
        for direction, neighbor in enumerate(map_copy.neighbors(square)):
            if neighbor.owner != myID:
                heuristic_value = heuristic(neighbor, map_copy)
                if heuristic_value > max_heuristic:
                    max_heuristic = heuristic_value
                    target = neighbor
                    best_direction = direction

        if target is not None and target.strength < square.strength:
            return Move(square, best_direction)
    
    return Move(square, STILL)


# function that updates the map after a piece has been moved
# it avoids attacking cells multiple times so far 29/04/2024
def update(map_copy, move):
    square = move.square
    direction = move.direction
    target = map_copy.get_target(square, direction)

    if target.owner == myID:
        # ma mut pe celula mea, presupun ca nu ma ataca nimeni
        target.strength += square.strength + target.production
        if target.strength > 255:
            target.strength = 255
        return

    if square.strength > target.strength:
        # atac celula inamica sau neutra si o cuceresc
        target.strength = square.strength - target.strength
        target.owner = myID
    else:
        target.strength -= square.strength
    # trebuie adaugata conditie de verificat daca ultima mutare a provocat overkill

while True:
    game_map.get_frame()
    map_copy = copy.deepcopy(game_map)
    moves = []
    for square in game_map:
        if square.owner == myID:
            move = get_move(square, map_copy)
            update(map_copy, move)
            moves.append(move)
    hlt.send_frame(moves)