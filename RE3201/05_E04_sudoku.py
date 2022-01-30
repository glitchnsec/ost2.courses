# Challenge by @barbieauglend
# Course: https://p.ost2.fyi/courses/course-v1:OpenSecurityTraining2+RE3201_symexec+2021_V1/about
# Solution to: 05_E04_sudoku

#!/usr/bin/env python
# coding: utf-8

# <img align='center' src='images/background_up.png' width='10000000' overflow='hidden'/>

# # Exercise 0x4
# 
# ### z3 Distinct

# ## Documentation

# ### [Distinct](http://z3prover.github.io/api/html/namespacez3py.html#a9eae89dd394c71948e36b5b01a7f3cd0)

# ## Code Snippet
""" Sudoku board example
_ _ _ _ 1 _ _ 3 _
_ _ 9 _ _ 5 _ _ 8
8 _ 4 _ _ 6 _ 2 5
_ _ _ _ _ _ 6 _ _
_ _ 8 _ _ 4 _ _ _
1 2 _ _ 8 7 _ _ _
3 _ _ 9 _ _ 2 _ _
_ 6 5 _ _ 8 _ _ _
9 _ _ _ _ _ _ _ _
"""
# ## Solution

# In[1]:


# Set up the environment
# and import z3 python-bindings
from z3 import *
import itertools

# Create a solver
s = z3.Solver()


# In[2]:


# import the sudoku game
puzzle_file = 'Exercises/04_sudoku/my_sudoku.txt'


# In[3]:


# Create the sudoku blank sudoku board as a matrix
cells = []
for row in range(0,9):
    cells += [[]]
    for col in range(0, 9):
        # initialize each cell as an In
        cells[row] += [z3.Int(f'{row}{col}')]


# In[4]:


# Add the sudoku board values
for i, line in enumerate(open(puzzle_file, 'r').read().replace(' ', '').split('\n')):
    for j, value in enumerate(line):
        if value != '_':
            s.add(cells[i][j] == value)


# In[5]:


# Add cell constraints
#Student: cell values must be integers between 1 and 9
cell_req = []
for row in range(0, 9):
    for col in range(0, 9):
        # Student: Maybe this could be simplified?
        cell_req += [cells[row][col] > 0]
        cell_req += [cells[row][col] < 10]
s.add(cell_req)


# In[6]:


# Add column contraints
col_req = []
for col in range(0,9):
    data = []
    for row in range(0,9):
        #Student: construct the column
        data += [cells[row][col]]
    #Student: require distinct values
    col_req += [Distinct(data)]
s.add(col_req)


# In[7]:


# Add row contraints
row_req = []
for row in range(0,9):
    #Student: require distinct values in rows
    row_req += [Distinct(cells[row])]
s.add(row_req)


# In[8]:


# Add 3x3 small squares constraints
#Student:- Probably there's a cooler and faster way
square_req = []
#Student:- Treat the matrix as a group of 3 columns
for col_grp in range(0, 9, 3):
    # all the 3x3 squares in a column group
    col_squares = []
    min_idx = 0 + col_grp
    max_idx = 3 + col_grp
    #Student:  A 3x3 square
    square = []
    for row in range(0, 9):
        for col in range(min_idx, max_idx):
            square += [cells[row][col]]
        #Student: a filled 3x3 square as a row data
        if (row+1) % 3 == 0:
            col_squares += [square]
            square = []
    #Student: require each square (as a row data)
    #Student: To have distinct values
    for squares in col_squares:
        square_req += [Distinct(squares)]
        
s.add(square_req)


# In[9]:


# Check for satisfiability
if s.check() == sat:
    m = s.model()
    print("SOLVABLE!")
    for row in range(0, 9):
        data = []
        for col in range(0, 9):
            data += [m[cells[row][col]]]
        print(data)
    
else:
    print('Not solvable')


# <img align='center' src='images/background_down.png' width='1000000' overflow='hidden'/>
