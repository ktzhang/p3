# -*- coding: utf-8 -*-
__author__ = 'Yoon Ho Han, Kevin Zhang'
__email__ = 'yhhan@ucsd.edu, ktzhang@ucsd.edu'

from collections import deque
from operator import itemgetter

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """

    smallestDomain = float("infinity");
    unassignedVars = deque();

    for variable in csp.variables:
        currentDomain = len(variable.domain);
        # length of domain of variable is less than the previous smallest domain, but
        # variable is unassigned
        if (currentDomain < smallestDomain and currentDomain != 1):
            # variable is the new MRV variable
            unassignedVars.clear();
            unassignedVars.append(variable);
            # currentDomain is the new smallestDomain
            smallestDomain = currentDomain;
        # length of domain of variable is equal to smallest domain, so add variable to 
        # queue of variables with the minimum remaining values
        elif (currentDomain == smallestDomain):
            unassignedVars.append(variable);
        # if length of domain is greater than previous smallest domain, skip this variable

    largestConstraints = float("-infinity");
    # unassignedVars holds the variables with MRV ties
    for var in unassignedVars:
        if (len(csp.constraints[var]) > largestConstraints):
            nextVar = var;
    return nextVar;


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """

    # used to sort domain by number of conflicts created
    valueToConflicts = [];
    for value in variable.domain:
        conflicts = 0;
        # check all neighbors for conflicts
        for arc in csp.constraints[variable].arcs():
            conflicts += arc[0].domain.count(value);
            conflicts += arc[1].domain.count(value);
        valueToConflicts.append([value, conflicts]);
        
    # sort by increasing order of conflicts created
    valueToConflicts = sorted(valueToConflicts, key=itemgetter(1));
    newDomain = [];
    for value in valueToConflicts:
        newDomain.append(value[0]);

    return newDomain
