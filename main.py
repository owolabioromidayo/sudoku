import tkinter as tk
import random
import copy
from choice_window import Choice

class Sudoku:
    def __init__(self, mode, difficulty):
        if mode == 'debug':
            self.gen_puzzle()
            

        else:

            self.width, self.height = 800,800
            self.difficulty = difficulty
            self.game = [[[None for i in range(3)] for i in range(3)] for i in range(9)]
            self.cellsize =  self.width // 9
            self.build()



    def build(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(width=False, height=False)
        self.root.bind("<Button-1>", self.handleclick)  

        self.board = tk.Canvas(self.root,width=self.width, height=self.height)
        self.board.pack()

        self.gen_lines(7,3)
        self.make_puzzle()

        self.root.mainloop()


    def gen_lines_recursive(self, x, y, length,width):
        step = length // 3
        pos = [step*i for i in range(1,3)]

        #main grid lines
        for i in range(2):
            self.board.create_line(x, y+pos[i], x+length, y+pos[i], width=width) #horizontal lines
            self.board.create_line(x+pos[i],y,x+pos[i], y+length, width= width) #vertical lines
    
    def gen_lines(self, b_width,s_width):

        self.gen_lines_recursive(0,0, self.width,  b_width)

        tlc = {} #idx to pos
        for y in range(3):
            for x in range(3):
                tlc[y*3+x] = [y,x] 
        
        print(tlc)

        small_step  = self.width//3
        for i in range(9):
            y,x = [idx*small_step for idx in tlc[i]]
            self.gen_lines_recursive(x, y, small_step, s_width)

    def pos_to_loc(self, x, y):
        loc_x = x// self.cellsize
        loc_y = y// self.cellsize
        return loc_x, loc_y

    def loc_to_pos(self, x, y):
        pos_x, pos_y = x*self.cellsize, y*self.cellsize
        #center positions
        pos_x += self.cellsize // 2
        pos_y += self.cellsize // 2

        return pos_x, pos_y

    def handleclick(self, event):
        x,y = self.pos_to_loc(event.x, event.y)
        cell_id = y*9+x
        print(cell_id)
        Choice(self, cell_id )


        

    def flatten(self,arr):
        return [j for j in i for i in arr]

    def reshape(self, arr, step=3):
        #converts a 1d array to a 2d array, each row of size step, provided step*2 values
        ls = []
        for i in range(step):
            ls.append([j for j in arr[step*i:step*i+step] ] )

        return ls


    def shift_ls(self, ls, shift):

        #shifts flattened array
        for _ in range(shift):
           left = ls.pop(0)
           ls.append(left)

        return ls


    def gen_puzzle(self):
        seed_nums = [i for i in range(1,10)]
        random.shuffle(seed_nums)

        puzzle = []
        shift_vals  = [0,3,3,1,3,3,1,3,3]
        for idx in shift_vals:
           
            seed_nums = self.shift_ls(seed_nums, idx)
            row = copy.copy(seed_nums)
            # row = self.reshape(row)
            puzzle.append(row)

        
        #print puzzle
        # for row in puzzle:
        #     for val in row:
        #         print(str(val) +' ', end='')
        #     print('')

        return puzzle


    def make_puzzle(self):
        diffs = {'easy':0.5, 'medium': 0.6, 'hard': 0.8}

        removal_rate = diffs[self.difficulty]
        num_to_remove = int(removal_rate * 81)
        puzzle = self.gen_puzzle()

        #apply removal rate to puzzle
        for _ in range(num_to_remove):
            _range = [i for i in range(9)]
            x,y = random.choice(_range), random.choice(_range)
            puzzle[y][x] = None


        #print puzzle on board
        for row_idx in range(len(puzzle)):
            for col_idx in range(len(puzzle)):
                x,y = col_idx, row_idx
                pos_x, pos_y = self.loc_to_pos(x,y)
                cell_id = y*9+x

                self.draw(pos_x, pos_y, puzzle[row_idx][col_idx], cell_id )
                


    def draw(self, x, y, text, cell_id):
        if text is not None:
            self.board.create_text(x, y, text=text, font=('Times', 20), tag= "."+str(cell_id) )

        else:
            self.board.create_text(x, y, text='', font=('Times', 20), tag= "."+str(cell_id) )




if __name__ == "__main__":
    s = Sudoku(mode = 'main', difficulty='hard' )