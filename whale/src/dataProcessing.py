#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
import re

"""This module contains a class which process data retrieve from files.

    We have some functionnalities implemented like:
    - Reading of file to retrieve clauses
    - Retrieve all cnf files from a directory
    - Retrieve and count(unique) variable from clauses
"""

class DataProcessing:
    """This class allows to process data from .cnf files."""
    def __init__(self):
        #: set: All variables of a set of clauses program must be analyzed
        self.vars:set = set()
        #: int: Number of distinct variables containing the set of clauses program must be analyzed
        self.nb_vars:int = 0

    
    def getClauseFromFile(self, filename:str):
        """Allow to retrieve clauses from a file

        Args:
            filename: path of file to read
        
        Returns: 
            list of clauses

        Example:
            literal blocks::

                dp.getClauseFromFile(filename) => [[1,-2,4], [-3,4], [-1,-3]]
        """
        with open(filename) as fi:
            data = fi.readlines()
        C = list()
        for line in data:
            line = line.strip()
            if re.match(r'((\-?[1-9])|([1-9](\d|\s)))', line[:2]):
                C.append(list(map(int,line.split()[:-1])))
        return C

    def getCnfFilesFromDirectory(self, dirpath:str):
        """Get all cnf files from a specific directory
        
        Args:
            dirpath: path where program can find cnf files

        Returns: 
            list of files path

        """
        try:
            onlyfiles = [join(dirpath, f) for f in listdir(dirpath) if isfile(join(dirpath, f)) and f.endswith('.cnf') ]
            return onlyfiles
        except FileNotFoundError:
            print("Votre dossier n'existe pas")

    def countVars(self, C:list):
        """Count variables of set of clauses

        Args:
            C: a set of clauses

        Returns: 
            return number of variables in the set of clauses
        
        Example:
            literal blocks::

                C = [(1,-2,4), (-3,4), (-1,-3)]
                d = DataProcessing()
                nbVars = d.countVars(C)
                print(nbVars) => 4
                print(d.vars) => (1, 2, 4, 3)
                print(d.nbVars) => 4
        """
        self.nb_vars = 0
        self.vars = set()
        for c in C:
            self.vars = self.vars | set(map(abs, c))
        self.nb_vars = len(self.vars)
        return self.nb_vars

    
