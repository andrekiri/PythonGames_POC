"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # check 0 tile
        if self._grid[target_row][target_col] != 0 :
            return False
        # check current row
        for col in range(target_col + 1, self._width):
            if self._grid[target_row][col] != col + self._width * target_row :
                return False
        # check below rows
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + self._width * row :
                    return False       
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        string = ""
        string2 = ""
        # find tile which should be moved
        tile_pos = self.current_position(target_row, target_col)
        if target_row !=  tile_pos[0]:
            # solves interio tile if it is not in the same row
            string = self.move_tile_above_target(target_row, target_col, tile_pos)  
        else:
            # case where tile is in the same row as target
            for dummy_col in range(target_col, tile_pos[1], -1):
                string += "l"
            for dummy_col in range(target_col, tile_pos[1] +1, -1):
                string += "urrdl"        
            self.update_puzzle(string)
       
        return string + string2

    def move_tile_above_target(self, target_row, target_col, tile_pos):
        """
        solves interio tile if it is not in the same row
        return the moving string
        """
        string = ""
        string2 = ""
        for dummy_row in range(target_row, tile_pos[0] + 1, -1):
            string += "u"
        if tile_pos[1] != target_col:
            string += "u"                
            if tile_pos[1] > target_col:
                for dummy_col in range(target_col, tile_pos[1] -1):
                    string += "r"             
                if tile_pos[0] == 0:
                        string += "druld"
                for dummy_col in range(target_col, tile_pos[1]):
                    string += "rulld"
                string += "dr"                                
            else :
                for dummy_col in range(target_col, tile_pos[1], -1):
                    string += "l"
                if tile_pos[0] == 0:
                    string += "druld"
                for dummy_col in range(target_col, tile_pos[1] +1, -1):
                    string += "urrdl"
                string += "dr" 
        self.update_puzzle(string)
        tile_pos = self.current_position(target_row, target_col)
        for dummy_row in range(target_row, tile_pos[0] + 1, -1):
            string2 += "ulddr"
        string2 += "uld"
        self.update_puzzle(string2)
        return string + string2
            
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        string = ""
        string2 = ""
        tile_pos = self.current_position(target_row, 0)
        if tile_pos == (target_row -1 , 0):
            string += "u"
            for dummy_col in range(self._width - 1):
                string += "r"
            self.update_puzzle(string)
            return string
        for dummy_row in range(target_row, tile_pos[0] + 1, -1):
            string += "u"
        if tile_pos[1] != 0:
            string += "u"
            for dummy_col in range(tile_pos[1] -1):
                string += "r"             
            if tile_pos[0] == 0:
                string += "druld"
            for dummy_col in range(tile_pos[1] -1):
                string += "rulld"
            string += "ruld"
        self.update_puzzle(string)
        tile_pos = self.current_position(target_row, 0)
        for dummy_row in range(target_row, tile_pos[0] + 2 , -1):
            string2 += "urddl"
        string2 += "urdlruldrdlurdluurddlur"
        for dummy_col in range(self._width - 2):
                    string2 += "r"
        self.update_puzzle(string2)
        return string + string2

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0 or self._grid[1][target_col] != target_col + self._width:
            return False
        for col in range(target_col + 1, self._width):
            if self._grid[0][col] != col:
                return False
        test_puzzle = self.clone()
        test_puzzle.update_puzzle("d")
        if test_puzzle.row1_invariant(target_col):
            return True
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.lower_row_invariant(1, target_col):
            return True
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        string = ""
        tile_pos = self.current_position(0, target_col)
        if tile_pos[0] == 0 and tile_pos[1] == target_col - 1 :
            string += "ld"
        else:
            if tile_pos[0] ==  0:
                for dummy_col in range(target_col, tile_pos[1], -1):
                    string += "l"
                for dummy_col in range(target_col, tile_pos[1] +2, -1):
                    string += "drrul" 
                string += "druld"
            else:
                for dummy_col in range(target_col, tile_pos[1] , -1):
                    string += "l"
                for dummy_col in range(target_col, tile_pos[1] + 1, -1):
                    string += "rdlur"
                string += "ld"
            string += "urdlurrdluldrruld"
        self.update_puzzle(string)        
        return string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        string = ""
        tile_pos = self.current_position(1, target_col)
        if tile_pos[0] ==  1:
            for dummy_col in range(target_col, tile_pos[1], -1):
                string += "l"
            for dummy_col in range(target_col, tile_pos[1] +1, -1):
                string += "urrdl"     
        else:
            string += "ul"
            for dummy_col in range(target_col, tile_pos[1] + 1, -1):
                string += "l"
            
            string += "d"
            if tile_pos[1] != target_col:
                string += "ruld"
                for dummy_col in range(target_col, tile_pos[1] + 1, -1):
                    string += "urrdl" 
        string += "ur"  
        self.update_puzzle(string)        
        return string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        string = "ul"
        self.update_puzzle("ul")
        while self._grid[0][1] != 1:
            self.update_puzzle("drul")
            string += "drul"
        return string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        tmp = ""
        string = ""
        zero_pos = self.current_position(0,0)
        for dummy_row in range(zero_pos[0], self._height - 1):
            tmp += "d"
        for dummy_col in range(zero_pos[1], self._width - 1):
            tmp += "r"
        self.update_puzzle(tmp)
        for row in range(self._height -1, 1, -1):
            for col in range(self._width -1, 0, -1):
                assert self.lower_row_invariant(row,col)
                string += self.solve_interior_tile(row, col)
                assert self.lower_row_invariant(row, col -1)
            self.lower_row_invariant(row, 0)
            string += self.solve_col0_tile(row)
        for col in range(self._width -1, 1, -1):
            assert self.row1_invariant(col)
            string += self.solve_row1_tile(col)
            assert self.row0_invariant(col)
            string += self.solve_row0_tile(col)
        string +=self.solve_2x2()
        return tmp + string

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 2))
#
#A = [[8, 7, 13, 14],
#     [15, 6, 1, 2],
#     [5, 9, 10, 11],     
#     [12, 3, 4, 0]]
#
#B = [[3, 1, 2, 0],
#     [4, 5, 6, 7],
#     [8, 9, 10, 11],     
#     [12, 13, 14, 15]]
#
#C = [[1,2],
#     [0,4],
#     [3,5]]
#
#D = [[3,4,1],
#     [0,2,5]]
#
#F = [[4, 1, 2, 3],
#     [5, 0, 6, 7],
#     [8, 9, 10, 11],
#     [12, 13, 14, 15]]
##
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj
#print obj.solve_puzzle()
###
#print obj
######print test1.current_position(3,2)
####print test1
####print test1.solve_row1_tile(3)
####print test1
#####print test1
#####print E.row0_invariant(2)
#####print E.solve_puzzle()
#######test2 = Puzzle(4, 4, B)
#######print test2.lower_row_invariant(2, 3)
##poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, F))
###print test1.solve_puzzle()
###print test1