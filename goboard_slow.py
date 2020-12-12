import copy
from dlgo.gotypes import Player

class Move():
    #the standard phrase for a turn - three options - play, pass, or resign (i.e. quit)
    #in reality, we will always initialize with Move.play/resign/pass_turn

    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign=True)


class GoString():
    #this essentially represents a clustor of stones
    #you can then keep track of liberties of the cluster
    #and merge with other clusters
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):#remove free spaces next to the group
        self.liberties.remove(point)
    
    def add_liberty(self, point):#laid down a point that added free spaces
        self.liberties.add(point)

    def merged_with(self, go_string): #combine the cluster (represented by touples I believe)
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(self.color, combined_stones, (self.liberties | go_string.liberties)-combined_stones)
    
    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties)

class Board():
    def __init__(self, num_rows, num_cols):#initialize with size of the board
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = ()

    def place_stone(self, player, point): #placing a stone down on the board ;)
        assert self.is_on_grid(point) #checks if stone is even on board
        assert self._grid.get(point) is None #returns what is on that position (player or None)
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors(): #start out by examining direct neighbors
            if not self.is_on_grid(neighbor): # i think this is saying that if the point is off the board - NEXT!
                continue
            neighbor_string = self._grid.get(neighbor) #assign what the neibor cluster is
            if neighbor_string is None: #if the neighbor string doesnt exist - it's a free space!
                liberties.append(neighbor) 
            elif neighbor_string.color == player: #if it does exist - and is the same color - add to list of same
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color: 
                    #if it does exist but is not yet listed, add to list of opposite color
                    adjacent_opposite_color.append(neighbor_string)
        #now update the string with the new data
        new_string = GoString(player, [point], liberties)
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def is_on_grid(self, point): #checks if point is within the board params
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols
    
    def get(self, point): #finds if the point is empty or a player
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point): #returns cluster at point - and is helpful to stop self capture
        string = self._grid.get(point)
        if string is None:
            return None
        return string            