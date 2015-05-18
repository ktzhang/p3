# -*- coding: utf-8 -*-
__author__ = 'Please write your names, separated by commas.'
__email__ = 'Please write your email addresses, separated by commas.'


def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    For P3, *you do not need to modify this method.*
    """
    return next((variable for variable in csp.variables if not variable.is_assigned()))


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    For P3, *you do not need to modify this method.*
    """
    return [value for value in variable.domain]


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P3, *you do not need to modify this method.*
    """
    return True


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P3, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns the successful assignment; otherwise, it returns None.
    """
    # csp is is complete
    if (is_complete(csp)):
        return csp.assignment;
    else:
        var = select_unassigned_variable(csp);
        # Loop through all possible values for var
        for value in order_domain_values(csp, var):
            # assign if value is consistent with var
            if (is_consistent(csp, var, value)):
                csp.variables.begin_transaction();
                var.assign(value);
                result = backtrack(csp);
                if (result != None):
                    return result;
                else:
                    # Value didn't work, so backtrack
                    csp.variables.rollback();
        return None;

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

def is_complete(csp):
    """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""
    for x in csp.variables:
        if (not x.is_assigned()):
            return False;

    return True;
