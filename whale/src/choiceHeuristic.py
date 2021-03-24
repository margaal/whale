#!/usr/bin/env python3
""" This module contains all class to manage variable choice Heuristic """

class VariableChoiceHeuristic:
    """ Super class to handle variable choice heuristic """
    def __init__(self, vars):
        """
        Args:
            vars (set): variables used in all clauses.
        """
        #: set: All variables of a set of clauses program must be analyzed
        self.vars = vars
        
    
    def getVariabeTriplet(self, S):
        """Method to get variable

        Args:
            S: assignment set 
        
        Returns:        
            a triplet (X, v, v') such as X is variable, v is value of X and v' is alternative value of X

        """
        if len(S) == 0:
            return (min(self.vars), 1, -1)
        s = set(list(zip(*S))[0])
        return (min(self.vars-s), 1, -1)

class SimpleVariableChoiceHeuristic(VariableChoiceHeuristic):
    """ First approach to choose variable, it is simple. we choose the first variable wich is not yet in assignment set (S) """
    def __init__(self, vars):
        super().__init__(vars)
    
    def getVariableTriplet(self, S):
        """Method to get variable

        Args:
            S: assignment set 
        
        Returns:        
            a triplet (X, v, v') such as X is variable, v is value of X and v' is alternative value of X

        """
        return super().getVariabeTriplet(S)

class LevelTwoVariableChoiceHeuristic(VariableChoiceHeuristic):
    """ This approach to choose variable is better than  SimpleVariableChoiceHeuristic because it considers unitary clause"""
    def __init__(self, vars):
        super().__init__(vars)
        #: set: All unitary clauses detected in the previous analysis of system of clauses
        self.unitClauseLitteral:set = set() 
    
    def getVariableTriplet(self, S):
        """Method to get variable
        
        Args:
            S(list): assignment set 
        
        Returns:
            a set of tuple, i.e a triplet (X, v, v') such as X is variable, v is value of X and v' is alternative value of X

        """
        if len(self.unitClauseLitteral)!=0:
            return self.unitClauseLitteral
        return super().getVariabeTriplet(S)