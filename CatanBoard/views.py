# Author: Grzegorz Milka
# Date 03.03.2013
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import random

HEIGHT=100 # Half of the height of one tile
WIDTH=170 # Length of left and center portion of a file

# positions where we can place tiles
positions = [(i, 2*j) for i in [0,4] for j in range(1,4)] + \
    [(i, 2*j + 1) for i in [1,3] for j in range(0,4)] + \
    [(2, 2*i) for i in range(0,5) ]
positions = [(pos[0] * WIDTH, pos[1] *HEIGHT) for pos in positions]

# possible dice tags on fields
dice = [2,12] + 2* (range(3,7) + range(8,12))

# Tiles available in game. Also names of images containing those tiles
tiles = 3*['brick', 'rock'] + 4 * ['wood', 'grain', 'sheep'] + ['desert']

def home(request):
    random.shuffle(positions)
    random.shuffle(dice)
    pos_tiles = [{'tile': tile, 'pos': pos} for (tile, pos) in
            zip(tiles,positions)]

    # Add dice info to each position, if it is a desert than it doesn't have a
    # tag
    pos_dices = []
    dice_idx = 0
    for tile in pos_tiles:
        if tile['tile'] != 'desert':
            pos_dices.append({'dice': str(dice[dice_idx]), 'pos': tile['pos'],
                'color': 'black' if dice[dice_idx] not in [6,8] else 'red',
                'size': 35  + (9 * (13 - dice[dice_idx] if dice[dice_idx] > 7
                    else (dice[dice_idx] - 1))) })
            dice_idx += 1
        else:
            pos_dices.append({'dice': '', 'pos': tile['pos']})

    c = RequestContext(request, {'tiles': pos_tiles, 'dices': pos_dices})
    return render_to_response("index.html", c)

