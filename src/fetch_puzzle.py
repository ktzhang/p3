#! /usr/bin/python
# -*- coding: utf-8 -*-
"""Contains routines to fetch puzzles from http://www.futoshiki.org/. """

__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'

import sys
import urllib2

from assignment3 import Futoshiki


def fetch_puzzle(size, difficulty, id, solution=False):
    """Fetches a new puzzle of given size, difficulty (1 - 6), puzzle id (1 to ???)
    from http://www.futoshiki.org/.

    If solution is True, displays the solution to the puzzle.
    """

    input_text = urllib2.urlopen(
        'http://www.futoshiki.org/get.cgi?size=%d&difficulty=%d&id=%d' % (size, difficulty, id)).read()
    input_text = input_text[28:-8]
    input_text = input_text[len(input_text) / 2:] if solution else input_text[:len(input_text) / 2]
    return Futoshiki.convert(input_text)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s size difficulty id")

    import argparse

    parser = argparse.ArgumentParser(description='Plays the Futoshiki game.')
    parser.add_argument('size', metavar='N', type=int, help='size of the board [4 - 10].', choices=xrange(4, 10))
    parser.add_argument('difficulty', metavar='D', type=int, help='difficulty of the game [0 - 4].', choices=xrange(4))
    parser.add_argument('id', metavar='I', type=int, help='the puzzle ID (some random integer).')
    parser.add_argument('--solution', dest='solution', action='store_true',
                        help='Displays the solution of the puzzle.')

    if len(sys.argv) < 4:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    print(fetch_puzzle(args.size, args.difficulty, args.id))
