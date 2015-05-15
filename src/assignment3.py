# -*- coding: utf-8 -*-
"""Contains the classes that represent the Sudoku game state and constraints.

These should not be modified!
"""

__author__ = 'Tomoki Tsuchida'
__email__ = 'ttsuchida@ucsd.edu'

from itertools import combinations
from copy import deepcopy
from math import sqrt

import operator


class Variable(object):
    """Represents a particular variable with the domain. The domain is mutable: that is, it represents the values
    that are currently available."""

    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

    def __repr__(self):
        return "%s('%s',%s)" % (self.__class__.__name__, self.name, repr(self.domain))

    def __str__(self):
        return str(self.name) + str(self.domain)

    def assign(self, value):
        """Assigns the value to the variable by reducing its domain to just one element."""
        self.domain = [value]

    def is_assigned(self):
        """Returns True if the variable is assigned, i.e. its domain has been reduced to a single value."""
        return len(self.domain) == 1

    @property
    def value(self):
        """Returns the assigned value, only if the variable is assigned."""
        assert self.is_assigned(), "The domain of %s is not reduced to a single value" % str(self)
        return self.domain[0]


class Variables(object):
    """A collections object for the variables. This has the ability to perform "transactions", which will
    take a backup and restore the current assignments and domains.

    You can use it by

    >>> csp.variables.begin_transaction()

    >>> csp.variables[0].assign(some_value)  # Assigning changes the domain of the variable to [some_value]

    >>> csp.variables[0].domain = [1,2,3]    # Possibly changing the domain

    >>> csp.variables.rollback()  # Undoes all the changes since the transaction began

    The transactions can be nested, so it can surround recursive calls (of the backtracking algorithm.)
    """

    def __init__(self, variable_list):
        self._variable_list = variable_list
        self._stack = []

    def __iter__(self):
        return iter(self._variable_list)

    def __len__(self):
        return len(self._variable_list)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._variable_list))

    def begin_transaction(self):
        """Creates a backup of the current domain values so that it can be rolled back."""
        self._stack.append([(variable, deepcopy(variable.domain)) for variable in self._variable_list])

    def rollback(self):
        """Rolls back any changes in the variable domains."""
        for variable, domain in self._stack.pop():
            variable.domain = domain


class Constraint(object):
    """Defines a particular constraint with  "var1 (relation) var2".
    For example, if relation is "not equal" (operator.ne), then it represents the constraint that
    "var1 is not equal to var2."
    """

    def __init__(self, var1, var2, relation):
        self.var1 = var1
        self.var2 = var2
        self.relation = relation

    def __eq__(self, other):
        return self.var1 == other.var1 and self.var2 == other.var2 and self.relation == other.relation

    def __hash__(self):
        return hash((self.var1, self.var2, self.relation))

    def __str__(self):
        return "(%s %s %s)" % (str(self.var1), self.relation.__name__, str(self.var2))

    def __repr__(self):
        return "%s(%s,%s,%s)" % (self.__class__.__name__, repr(self.var1), repr(self.var2), self.relation.__name__)

    inverse = {
        operator.ne: operator.ne,
        operator.gt: operator.lt,
        operator.lt: operator.gt
    }

    def _flip(self):
        """Returns the flipped version (var1 and var2 swapped) of the constraint.
        """
        return Constraint(self.var2, self.var1, Constraint.inverse[self.relation])

    def is_satisfied(self, val1, val2):
        """Returns True if the constraint is satisfied by the values (val1, val2) assigned to (var1, var2)."""
        return val1 in self.var1.domain and val2 in self.var2.domain and self.relation(val1, val2)


class Constraints(object):
    """The Constraints is a collection of Constraint objects with the ability to look up constraints by the variables.

    For example, to find all constraints involving a variable v1 (neighbors of v1), you can use

    >>> constraints[v1]  # returns all constraints with (v1, some other var)

    You can do other types of lookup:

    >>>constraints[v1, v2] # returns all constraints for the arc (v1, v2)

    >>> constraints[0] # is the first constraint in the list.

    >>> constraints.arcs() # returns the list of all arcs (v1, v2) in the constraints collection.

    Constraints is also iterable, so you can do things like

    >>> for constraint in csp.constraints: # to iterate across all constraints

    >>> for constraint in csp.constraints[V1]: # to iterate through all constraints involving V1, the neighbors

    """

    def __init__(self, constraint_list):
        self._constraint_list = constraint_list
        self._unary_lut_ = None
        self._binary_lut_ = None

    def __iter__(self):
        return iter(self._constraint_list)

    def __len__(self):
        return len(self._constraint_list)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._constraint_list))

    @property
    def _unary_lut(self):
        if self._unary_lut_ is None:
            self._unary_lut_ = {}
            for constraint in self._constraint_list:
                variable = constraint.var1
                if variable in self._unary_lut_ and constraint not in self._unary_lut_[variable]:
                    self._unary_lut_[variable].append(constraint)
                else:
                    self._unary_lut_[variable] = [constraint]

                # Add the flipped constraint
                variable = constraint.var2
                flipped_constraint = constraint._flip()
                if variable in self._unary_lut_ and flipped_constraint not in self._unary_lut_[variable]:
                    self._unary_lut_[variable].append(flipped_constraint)
                else:
                    self._unary_lut_[variable] = [flipped_constraint]

        return self._unary_lut_

    @property
    def _binary_lut(self):
        if self._binary_lut_ is None:
            self._binary_lut_ = {}
            for constraint in self._constraint_list:
                key = (constraint.var1, constraint.var2)
                if key in self._binary_lut_ and constraint not in self._binary_lut_[key]:
                    self._binary_lut_[key].append(constraint)
                else:
                    self._binary_lut_[key] = [constraint]

                key = (constraint.var2, constraint.var1)
                flipped_constraint = constraint._flip()
                if key in self._binary_lut_ and flipped_constraint not in self._binary_lut_[key]:
                    self._binary_lut_[key].append(flipped_constraint)
                else:
                    self._binary_lut_[key] = [flipped_constraint]

        return self._binary_lut_

    def __contains__(self, key):
        lut = self._binary_lut if type(key) is tuple else self._unary_lut
        return key in lut

    def __getitem__(self, key):
        if type(key) is int:
            return self._constraint_list[key]

        lut = self._binary_lut if type(key) is tuple else self._unary_lut
        return Constraints(lut[key]) if key in lut else Constraints([])

    def arcs(self):
        """Returns all arcs ((v1, v2) pairs) for the constraints contained in this list."""
        return self._binary_lut.keys()


class BinaryCSP(object):
    """Defines a binary CSP problem."""

    def __init__(self, variables, constraints):
        self.variables = Variables(variables)
        self.constraints = Constraints(constraints)

    @property
    def assignment(self):
        """returns the successful assignment (a dictionary of variable to value).
        """
        return dict([(variable, variable.value) for variable in self.variables if variable.is_assigned()])

    @staticmethod
    def print_assignment(assignment):
        """A utility method to pretty-print the assignment."""
        sorted_variables = sorted(assignment.keys(), key=operator.attrgetter('name'))
        return ','.join(['%s=%s' % (variable.name, assignment[variable]) \
                         for variable in sorted_variables])


###################################################
## The following are Futoshiki-specific classes. ##
###################################################

class FutoshikiVariable(Variable):
    """A Variable that's specific to the Futoshiki game (used to keep track of the board location)."""

    def __init__(self, N, i, j, v):
        domain = list(range(1, N + 1)) if v == 0 else [v]
        super(FutoshikiVariable, self).__init__('r%dc%d' % (i, j), domain)
        self.i = i
        self.j = j


class Futoshiki(object):
    """Contains Futoshiki-specific functions."""

    @staticmethod
    def convert(input_text):
        """Converts the string format used in the javascript on futoshiki.org
        to the 'more easily interpretable' format used in this class."""
        charmap = {'.': '0', '_': ' ', ')': '>', '(': '<', 'v': 'v', '^': '^'}
        for i in range(1, 9):
            charmap[str(i)] = str(i)

        K = int(sqrt(len(input_text)))
        N = (K + 1) / 2
        values = []
        inequalities = []
        for i in range(N):
            values.append([int(charmap[input_text[i * K * 2 + j * 2]]) for j in range(N)])
            inequalities.append([charmap[input_text[i * 2 * K + j * 2 + 1]] for j in range(N - 1)])
            if i < N - 1:
                inequalities.append([charmap[input_text[(i * 2 + 1) * K + j * 2]] for j in range(N)])

        return Futoshiki.print_board(N, values, inequalities)

    @staticmethod
    def print_board(N, values, inequalities):
        """Converts the value and inequality lists to a string representation."""
        s = ""
        for i in range(N):
            for j in range(N):
                s += "%d" % values[i][j]
                s += "%s" % inequalities[i * 2][j] if j < N - 1 else ""
            s += "\n"

            if i < N - 1:
                s += ' '.join(["%s" % inequalities[i * 2 + 1][j] for j in range(N)])
                s += "\n"

        return s

    INEQUALITY_MAP = {'>': operator.gt, 'v': operator.gt, '<': operator.lt, '^': operator.lt}

    def __init__(self, board):
        # Parse the board string
        lines = board.split('\n')
        N = int((len(lines) + 1) / 2)

        values = []
        inequalities = []
        for i in range(N):
            values.append([int(lines[i * 2][j * 2]) for j in range(N)])
            inequalities.append([lines[i * 2][j * 2 + 1] if j * 2 + 1 < len(lines[i * 2]) else ' ' \
                                 for j in range(N - 1)])
            if i < N - 1:
                inequalities.append([lines[i * 2 + 1][j * 2] if j * 2 < len(lines[i * 2 + 1]) else ' ' \
                                     for j in range(N)])

            self.values = tuple(map(tuple, values))
            self.inequalities = tuple(map(tuple, inequalities))
            self.N = N

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.board)

    def __str__(self):
        return Futoshiki.print_board(self.N, self.values, self.inequalities)

    def alldiff(self, variable_list):
        """Generate binary constraints for all of the variables in variable_list."""
        return [Constraint(v1, v2, relation=operator.ne) for v1, v2 in combinations(variable_list, 2)]

    def to_binary_csp(self):
        """Generates the Binary CSP from the board."""
        variables = [[FutoshikiVariable(self.N, i, j, v) for j, v in enumerate(row)] \
                     for i, row in enumerate(self.values)]
        constraints = []
        constraints += [constraint for row in variables for constraint in self.alldiff(row)]
        constraints += [constraint for j in range(self.N) \
                        for constraint in self.alldiff([variables[i][j] for i in range(self.N)])]
        for i in range(self.N):
            for j in range(self.N):
                if j < self.N - 1:
                    horizontal_inequality = self.inequalities[i * 2][j]
                    if horizontal_inequality != ' ':
                        constraints.append(Constraint(variables[i][j], variables[i][j + 1],
                                                      Futoshiki.INEQUALITY_MAP[horizontal_inequality]))

                if i < self.N - 1:
                    vertical_inequality = self.inequalities[i * 2 + 1][j]
                    if vertical_inequality != ' ':
                        constraints.append(Constraint(variables[i][j], variables[i + 1][j],
                                                      Futoshiki.INEQUALITY_MAP[vertical_inequality]))

        return BinaryCSP([v for row in variables for v in row], constraints)

    def solve_with(self, method):
        """Solves the game using the given CSP solver method."""
        csp = self.to_binary_csp()
        assignment = method(csp)
        if assignment is not None:
            values = list(map(list, self.values))
            for variable in csp.variables:
                values[variable.i][variable.j] = assignment[variable]
            self.values = tuple(map(tuple, values))
            return True
        else:
            return False
