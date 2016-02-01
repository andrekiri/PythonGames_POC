"""
Clone of 2048 game.
"""

#import poc_2048_gui  
import numeric
import random
import math

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = line
    for idx in range(len(result)):
        found = True
        # Find the first zero
        if result[idx] == 0:
            # check if there is any non zero after this zero
            found = False # Variable to indicate if a non zero is found after a zero
            dist = 0 # The distance of the non zero from the first zero
            for jdx in range(idx + 1, len(result)):
                if result[jdx] != 0:
                    found = True
                    dist = jdx - idx
                    break           
            if found:
                # Move all element tho the left of the zero found
                for kdx in range(idx, len(result) - dist):
                    result[kdx] = result[kdx + dist]
                    result[kdx + dist] = 0
        # Stop if all elements after result[idx] in the list are 0
        # this block is here for performance reasons - result is the same without this
        if found == False:
            break
    # Add any same neighbor values and slide the rest   
    for ldx in range(len(result) - 1):
        if result[ldx] == result[ldx + 1]:           
            for mdx in range(ldx + 1, len(result) - 1):
                result[mdx] = result[mdx + 1]
            result[ldx] *= 2
            result[len(result)- 1] = 0  
    return result


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self._grid = [[0 for dummy_row in range(self._width)] for dummy_col in range(self._height)]
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        result = ""
        for row in self._grid:
            result += "\n" + str(row)
        return result

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        new_d = {1: 3, 2: 1, 3: 0, 4: 2}
        for dummy_kdx in range(new_d.get(direction)):
            self.transpose()
        for idx in range(self._height):
            merge(self._grid[idx])
        for dummy_jdx in range(4 - new_d.get(direction)):
            self.transpose()
        self.new_tile()
        
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zero_found = False
        row_shuf = range(self._height)
        random.shuffle(row_shuf)
        col_shuf = range(self._width)
        random.shuffle(col_shuf)
        for row in row_shuf:
            for col in col_shuf:
                if self.get_tile(row, col) == 0: 
                    self.set_tile(row, col, random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4]))
                    zero_found = True
                    break
            if zero_found == True:
                break          
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """ 
        return self._grid[row][col]
    
    def transpose(self):
        """
        Transposes the matrix in order to aply merge.
        """
        temp =0
        result = [[0 for dummy_row in range(self._height)] for dummy_col in range(self._width)]
        for row in range(self._height):
            for col in range(self._width):
                result[col][self._height - row - 1] = self._grid[row][col]
        self._grid = result
        temp = self._height
        self._height = self._width
        self._width = temp        
    
    
        
 
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

