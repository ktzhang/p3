# -*- coding: utf-8 -*-
__author__ = 'Yoon Ho Han, Kevin Zhang'
__email__ = 'yhhan@ucsd.edu, ktzhang@ucsd.edu'


def is_complete(csp):
    """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""
    for x in csp.variables:
    	if (not x.is_assigned()):
    		return False;

    return True;