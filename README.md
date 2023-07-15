# Move Representation
A move is represented by two pieces of information being:
- Start square
- Direction

The start square represents the piece that would be picked up. The direction represents the end of the board the piece will be placed at. There are 4 possible options for a direction namely N, S, E and W which are short for North, South, East and West.

# Move Generation Output
The `printValidMoves()` function in Board.h will display the board such that the valid moves will be highlighted over each square. Calling this function with the default starting board configuration will yield:
```
SE_ SEW SEW SEW SW_ 
ENS ___ ___ ___ WNS 
ENS ___ ___ ___ WNS 
ENS ___ ___ ___ WNS 
NE_ NEW NEW NEW NW_ 
Number of valid moves: 44
```