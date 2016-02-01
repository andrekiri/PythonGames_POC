"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui
import math

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for man in self._human_list:
            yield man
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        if entity_type == ZOMBIE :
            current_list = self._zombie_list
        elif entity_type == HUMAN :
            current_list = self._human_list
        else: return  
        
        # create visited (copy of the original) grid and fill it with the obstacles
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        for row in range(len(self._cells)) :
            for col in range(len(self._cells[row])):
                if self.is_empty(row, col) == False:
                    visited.set_full(row,col) 
        
        # create 2D distance list
        distance_field = [[self._grid_height*self._grid_width for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        
        # create boundary_queue which contains the current_list
        self._boundary = poc_queue.Queue() 
        for cell in current_list :
            self._boundary.enqueue(cell)
            distance_field[cell[0]][cell[1]] = 0
            visited.set_full(cell[0],cell[1])
            
        while len(self._boundary) != 0:
            current_cell  =  self._boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0],neighbor[1]):
                    distance_field[neighbor[0]][neighbor[1]] = abs(neighbor[0] - current_cell[0]) + abs(neighbor[1] - current_cell[1]) + distance_field[current_cell[0]][current_cell[1]]
                    visited.set_full(neighbor[0],neighbor[1])
                    self._boundary.enqueue((neighbor))       
        return distance_field       
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        humans = list(self._human_list)
        for man in range(len(humans)):
            neighbors = self.eight_neighbors(self._human_list[man][0],self._human_list[man][1])
            max_dist = zombie_distance[self._human_list[man][0]][self._human_list[man][1]]
            for neigh in neighbors:
                dist = zombie_distance[neigh[0]][neigh[1]]
                if  dist > max_dist and dist < self._grid_height*self._grid_width:
                    humans[man] = neigh
                    max_dist = dist 
        self._human_list = list(humans)
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombies = list(self._zombie_list)
        for zom in range(len(zombies)):
            neighbors = self.four_neighbors(self._zombie_list[zom][0],self._zombie_list[zom][1])
            min_dist = human_distance[self._zombie_list[zom][0]][self._zombie_list[zom][1]]
            for neigh in neighbors:
                dist = human_distance[neigh[0]][neigh[1]]
                if  dist < min_dist:
                    zombies[zom] = neigh
                    min_dist = dist 
        self._zombie_list = list(zombies)
#print [[EMPTY for dummy_col in range(3)] for dummy_row in range(2)]
##zom = Zombie(4, 6, [(0,1),(1,1), (2,1)], [], [(1, 5)])
#zom = Zombie(3, 3, [(0,1), (2,1)], [], [(0, 0), (1, 0)])
#zom.compute_distance_field(HUMAN)
##print zom



# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Zombie(30, 40))
