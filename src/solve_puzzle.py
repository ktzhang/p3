#! /usr/bin/python
# -*- coding: utf-8 -*-
"""Invokes the CSP solver to solve the Futoshiki puzzle.

This module reads the Futoshiki puzzle from the standard input and prints the solution and time taken to solve it.
By default, it calls the 'backtracking_search' method in '../solutions/p6_solver.py', but you can optionally
specify a different python filename and a method name to use as the solver.

For example:

    $ python solve_puzzle.py < ../problems/p6/in/input1.txt

Or

    $ python solve_puzzle.py ../solutions/p3_basic_backtracking.py backtracking_search < ../problems/p6/in/input1.txt

to use the basic backtracking solver.

You can also pipe the output from fetch_puzzle.py, for e.g.

    $ python fetch_puzzle.py 4 1 110 | python solve_puzzle.py

"""

__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'

from time import time
import sys
import os.path

from assignment3 import Futoshiki


def solve_puzzle(puzzle, solve_method):
    """Solves the puzzle using the given solution method and returns the approximate time taken in seconds."""
    start_time = time()
    result = puzzle.solve_with(solve_method)
    if result:
        print(puzzle)
    else:
        print("Failed to find the solution.")
    return time() - start_time


if __name__ == '__main__':

    python_file = '../solutions/p6_solver.py' if len(sys.argv) < 2 else sys.argv[1]
    method_name = 'backtracking_search' if len(sys.argv) < 3 else sys.argv[2]

    sys.path.append(os.path.abspath(os.path.dirname(python_file)))
    module = __import__(os.path.splitext(os.path.basename(python_file))[0])
    solve_method = getattr(module, method_name)

    puzzle = Futoshiki(sys.stdin.read().strip())

    start_time = time()
    result = puzzle.solve_with(solve_method)
    if result:
        print(puzzle)
    else:
        print("Failed to find the solution.")
    print("Took %s seconds." % (time() - start_time))