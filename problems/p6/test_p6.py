"""Test case runner for Sharif Judge.

For each input in in/input*.txt, Sharif Judge will invoke this file as:

    python test_p6.py submitted_file.py <$inputfile >out

and the output file is later diff'ed against out/output*.txt file.
"""

__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'

import os
import sys

from assignment3 import *

def run_code_from(python_file, input_text):
    # Load the class from the specified .py file
    sys.path.append(os.path.abspath(os.path.dirname(python_file)))
    module = __import__(os.path.splitext(os.path.basename(python_file))[0])
    solve_method = getattr(module, 'backtracking_search')
    game = Futoshiki(input_text)
    game.solve_with(solve_method)
    return str(game)


if __name__ == '__main__':
    print(run_code_from(sys.argv[1], sys.stdin.read().strip()))