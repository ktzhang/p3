# -*- coding: utf-8 -*-
__author__ = 'Yoon Ho Han, Kevin Zhang'
__email__ = 'yhhan@ucsd.edu, ktzhang@ucsd.edu'


def is_consistent(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.

    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    # Looks through all the constraints linked to the variable
    for c in csp.constraints[variable]:
        # Loop through all the variable
        for v2 in csp.variables:
            # Check if is assigned and is set
            if(v2 == c.var2 and v2.is_assigned()):
                # Check if satisfied
                if not c.is_satisfied(value, v2.value):
                    return False

    return True
    
