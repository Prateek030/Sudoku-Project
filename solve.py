import itertools
import numpy as np

def findZero(sudoku):
    return next(
        (
            [i, j]
            for i, j in itertools.product(range(9), range(9))
            if sudoku[i, j] == 0
        ),
        None,
    )

def is_num_valid(num,loc,sudoku):
    # sourcery skip: invert-any-all, use-any, use-itertools-product
    if num in sudoku[loc[0],:] or num in sudoku[:,loc[1]]:
        return False
    pos_0 = loc[0]//3*3
    pos_1 = loc[1]//3*3
    
    for i in range(pos_0,pos_0+3):
        for j in range(pos_1,pos_1+3):
            if sudoku[i][j]==num:
                return False
            
    return True

                
def tryNum(sudoku):
    loc = findZero(sudoku)
    if loc != None:
        for num in range(1,10):
            if is_num_valid(num,loc,sudoku):
                sudoku[loc[0],loc[1]] = num
                result = tryNum(sudoku=sudoku)
                if result:
                    print(sudoku)
                    exit(0)
                    
                else:
                    sudoku[loc[0],loc[1]] = 0

            else: 
                continue
            
        return False
    return True

def solver(sudoku):
    print(tryNum(sudoku))



sudoku =[[5,3,0,0,7,0,0,0,0],
         [6,0,0,1,9,5,0,0,0],
         [0,9,8,0,0,0,0,6,0],
         
         [8,0,0,0,6,0,0,0,3],
         [4,0,0,8,0,3,0,0,1],
         [7,0,0,0,2,0,0,0,6],
         
         [0,6,0,0,0,0,2,8,0],
         [0,0,0,4,1,9,0,0,5],
         [0,0,0,0,8,0,0,7,9]]

solver(np.array(sudoku))
# sudoku = np.zeros((9,9),dtype=int)
solver(sudoku)
