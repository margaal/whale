#!/usr/bin/env python3
import logging as logg
from whale.src.choiceHeuristic import VariableChoiceHeuristic, LevelTwoVariableChoiceHeuristic

"""This module contains class which implemented DPLL iterative algorithm """

class Dpll:
    """ In this class, we have implemented the main functions of dpll algorithm """
    def __init__(self, C, nbVars, choiceHeuristicClass, ALLMODEL=False, CSAT=False):
        """
        Args:
            C (list(tuple(int))): a set of clauses program must analyze.
            nbVars (int): number of variables used in all clauses.
            choiceHeuristicClass (VariableChoiceHeuristic): Variable choice Heuristic class on which the program will be based to do analyze.
            ALLMODEL (bool): It is a flag to know if we must return all models for a set of clauses or one complete model.
            CSAT (bool): Flag to check if set of clauses C is SAT or UNSAT.

        """
        #: list(tuple(int)): that contains all clauses program will analize (It will not change during running of model searching algorithm)
        self.C = C
        #: int: Number of distinct variables containing the set of clauses program must be analyzed
        self._nbVars = nbVars
        #: VariableChoiceHeuristic: Variable choice Heuristic class on which the program will be based to do analyze
        self._choiceHeuristicClass:VariableChoiceHeuristic = choiceHeuristicClass
        #: list: Assignment stack that contains litterals which make a set of clauses satisfiable(It will change durant model searching)
        self._S = []
        #: set: index of clauses which are satisfiable, example: (0,2,3) so 0, 2 and 3 clauses are SAT among 4 clauses . It enables to know if assignment _S value make C satisfiable
        self._clauseSat = set() 
        #: list: store all models find during the running of DPLL algorithm
        self.models = []
        #: int: attribute to know number of failureNode. It will be useful to compare variable choice heuristic
        self.failureNode = 0
        #: bool: Boolean attribute. It is a flag to know if we must return all models for a set of clauses or one complete model
        self.ALLMODEL = ALLMODEL
        #: bool: Flag to check if set of clauses C is SAT or UNSAT
        self.CSAT:bool = CSAT 
        
    
    def _consistencyTest(self):
        """Method which enables consistency test of a set of clauses depending on assignment stack 
        
        Returns:
            True if C(set of clauses) is consistent else False
        """
        # reset clauseSat set before the checking of consistency
        self._clauseSat = set()        

        # make dictionnary to avoid to loop over S each time
        S_to_dict = {item[0]:item[1] for item in self._S}
        tmp = []
        for i in range(len(self.C)):
            cpt, lit = self._countNotNegLit(i, S_to_dict)
            if cpt == 0: # inconsistency
                return False
            elif cpt==1 and lit!=0 and abs(lit) not in S_to_dict:
                tmp.append(lit)
        
        # add unitary clauses if variable choice Heuristic is LevelTwoVariableChoiceHeuristic
        if isinstance(self._choiceHeuristicClass, LevelTwoVariableChoiceHeuristic):
            for l in tmp:
                self._choiceHeuristicClass.unitClauseLitteral.add((abs(l), -1 if l<0 else 1, None))
        
        if self.ALLMODEL:
            # To force searching of all models
            s = list(item[0]*item[1] for item in self._S)
            if len(s)==self._nbVars and len(self.models)>0 and sorted(s)==sorted(self.models[-1]):
                return False

        return True
    
    def _countNotNegLit(self, i, Sdict):
        """This private method counts a no negative litteral

        Args:
            i: index of clause in C
            Sdict: S in dictionnary like {"X":v} without v', by this way we avoid to loop over S each time

        Returns:
            Number of no negative litterals in clause according to S stack and possible unitary clause
        
        """
        cpt = 0
        possibleUnitClause = 0
        for l in self.C[i]:
            if abs(l) not in Sdict:
                possibleUnitClause = l
                cpt+=1
            else:
                if Sdict[abs(l)]*l > 0:
                    cpt+=1
                    self._clauseSat.add(i)
        return cpt, possibleUnitClause

    def checkSetOfClauses(self):
        """Check if a set of clauses is SAT or UNSAT. In case it is SAT, this method return all or one complete models
        according to flag ALLMODEL value 
        """
        if self.ALLMODEL and not self.CSAT:
            self._getAllModels()
        
        return self._getFirstCompleteModel()

    def _getFirstCompleteModel(self):
        """Private method which look for one complete model

        Returns:
            True if set of clause C is SAT else False

        """
        self._S = []
        while True:
            if self._consistencyTest():
                if self.CSAT and len(self._clauseSat)==len(self.C): # SAT 
                    s = list(item[0]*item[1] for item in self._S)
                    self.models.append(tuple(s))
                    return True # break when we are looking for SAT or UNSAT
                        
                if len(self._S) == self._nbVars:
                    s = list(item[0]*item[1] for item in self._S)
                    self.models.append(tuple(s))
                    return True
                else:
                    # choose (X, v, v') et append
                    if isinstance(self._choiceHeuristicClass, LevelTwoVariableChoiceHeuristic):
                        if len(self._choiceHeuristicClass.unitClauseLitteral)!=0:
                            for var in self._choiceHeuristicClass.getVariableTriplet(self._S):
                                self._S.append(var)
                            self._choiceHeuristicClass.unitClauseLitteral.clear()
                        else:
                            self._S.append(self._choiceHeuristicClass.getVariableTriplet(self._S))
                            
                    else:
                        new_var = self._choiceHeuristicClass.getVariableTriplet(self._S)
                        self._S.append(new_var)

            else:
                self.failureNode += 1
                item = self._S.pop()
                while len(self._S)>0 and item[2] is None:
                    item = self._S.pop()
                if item[2] is not None:
                    self._S.append((item[0], item[2], None))
                else:
                    return False

        return True

    def _getAllModels(self):
        """Method to get all models from a set of clauses
        
        Returns:
            all models of set of clauses C if exist or []

        """
        finished = False
        self._S = []
        while not finished:
            if self._consistencyTest():
                if len(self._S) == self._nbVars:
                    s = list(item[0]*item[1] for item in self._S)
                    self.models.append(tuple(s))
                    print(s)
                else:
                    # choose (X, v, v') et append
                    if isinstance(self._choiceHeuristicClass, LevelTwoVariableChoiceHeuristic):
                        if len(self._choiceHeuristicClass.unitClauseLitteral)!=0:
                            for var in self._choiceHeuristicClass.getVariableTriplet(self._S):
                                self._S.append(var)
                            self._choiceHeuristicClass.unitClauseLitteral.clear()
                        else:
                            self._S.append(self._choiceHeuristicClass.getVariableTriplet(self._S))
                            
                    else:
                        new_var = self._choiceHeuristicClass.getVariableTriplet(self._S)
                        self._S.append(new_var)
            else:
                self.failureNode += 1
                item = self._S.pop()
                while len(self._S)>0 and item[2] is None:
                    item = self._S.pop()
                if item[2] is not None:
                    self._S.append((item[0], item[2], None))
                else:
                    finished = True
          
        return self.models

    def summary(self, filen, OUTPUT_FILE=True):
        """Formatter method. It enables production of analysis reports

        Args:
            filen(str): report filepath to know where generate report
            OUTPUT_FILE(bool): FLAG to know if we must generate report or no, default True (generate report)

        """
        
        file_content = []
        if self.ALLMODEL:
            #file_content.append("Failure nodes: "+str(self.failureNode-(0 if len(self.models)==0 else len(self.models)-1))) # beceause we are forcing at least 1 time failure to find all models
            if len(self.models)==0:
                file_content.append("The set of clauses is UNSAT")
            else:
                complets = []
                unique_models = list(set(self.models))
                for item in unique_models:
                    complets.append(item)                    
            
                file_content.append("================ "+str(len(complets))+" Complete model(s). ================")
                file_content.append(self._displayList(complets))
        else:
            #file_content.append("Failure nodes: "+str(self.failureNode))
            if len(self.models)>0:
                file_content.append("The set of clauses is SAT")
                file_content.append("Complete model" if len(self.models[0])==self._nbVars else "partial model")
                file_content.append(self._displayList(list(self.models)))
            else:
                file_content.append("The set of clauses is UNSAT")
        
        if OUTPUT_FILE:
            with open(filen, 'w') as f:
                f.write("\n".join(file_content))
            print("===Analysis is done and we can find report: '"+filen+"'")
        else:
            print("******************REPORT******************")
            print('\n'.join(file_content))
            

    def _displayList(self, liste:list):
        """Formatter Method to display list value
        Returns: 
            String
        """
        stri = ""
        for item in liste:
            stri+="=> "+ ' '.join(map(str, item))+"\n"
        return stri
        
