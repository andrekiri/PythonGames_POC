# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.

class SolitaireMancala:


    def __init__(self):
        """ """
        self._lst = [0]
      
    def set_board(self, configuration):
        self._lst = list(configuration)
        
    def __str__(self):
        output = list(self._lst)
        output.reverse()
        return str(output)
    
    def get_num_seeds(self, house_num):
        return self._lst[house_num]

    def is_legal_move(self, house_num):
        move_in_range = 0 < house_num < len(self._lst)
        index_matches = self._lst[house_num] == house_num
        return move_in_range and index_matches
        
    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            l = range(house_num)
            l.reverse()
            for i in range(house_num):
                self._lst[i] += 1
            self._lst[house_num] = 0
        return
        
    def choose_move(self):
        for i in range (1, len(self._lst)):
            if self.is_legal_move(i):
                return i
        return 0
         
    def is_game_won(self):
        for i in range(1,len(self._lst)):
            if self._lst[i] != 0:
                return False
        return True
        
    def plan_moves(self):
        lmove = []
        g = SolitaireMancala()
        g.set_board(list(self._lst))
        next_move = g.choose_move()
        while next_move != 0 :
            g.apply_move(next_move)
            lmove.append(next_move)          
            next_move = g.choose_move()
        return lmove
    

game = SolitaireMancala()
#print game.plan_moves()
game.set_board([1, 3, 2, 0])
print str(game)
game.set_board([0,1,2,3])
#print game.plan_moves()
print game
print game.choose_move()

game.apply_move(1)
print game
#print game.choose_move()
game.apply_move(game.choose_move())
print game
print game.choose_move()
#print game.is_game_won()
game.apply_move(1)
print game
print game.choose_move()
#print game.is_game_won()
game.apply_move(3)
print game
print game.choose_move()
#print game.is_game_won()
print game.plan_moves()
            

        
    

