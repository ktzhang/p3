# -*- coding: utf-8 -*-
__author__ = 'Yoon Ho Han, Kevin Zhang'
__email__ = 'yhhan@ucsd.edu, ktzhang@ucsd.edu'

from collections import deque


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    # loop through the arcs
    while (queue_arcs):
        arc = queue_arcs.popleft();
        # check if arc needs to be revised
        if (revise(csp, arc[0], arc[1])):
            # if no more in domain, arc consistency fails
            if (len(arc[0].domain) == 0):
                return False;
            else :
                # loop through all arcs with arc[0]
                for neighbor in csp.constraints[arc[0]].arcs():
                    # skip if neighbor is the same arc
                    if (neighbor[0] == arc[0] or neighbor[1] == arc[0]):
                        continue;
                    # add arc to queue if current arc has been revised
                    queue_arcs.append(neighbor);
    return True;

def revise(csp, xi, xj):
    revised = False;
    # loop through domain of xi
    for xVal in xi.domain:
        found = False;
        # loop through domain of xj
        for yVal in xj.domain:
            # check if domain for xj satisfies constraints
            satisfied = True;
            for constraint in csp.constraints[xi, xj]:
                if (not constraint.is_satisfied(xVal, yVal)):
                    # satisfied is false if value of xj doesn't satisfy any of the constraints
                    satisfied = False;
                    break;
            # if any value of domain for xj is consistent, don't have to check any other values
            if (satisfied):
                found = True;
                break;
        # none of the domain of xj satisfies constraint with xi
        if (not found):
            xi.domain.remove(xVal);
            revised = True;
    return revised;
