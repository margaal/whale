#!/usr/bin/env python3
from whale.src.dataProcessing import DataProcessing
from whale.src.choiceHeuristic import LevelTwoVariableChoiceHeuristic
from whale.src.dpll import Dpll
import argparse
from os import path

"""Solvsat Module

This module contains main functions including entry point function. You can execute this file.
Example:
    literal blocks::

        $ python3 solvsat.py --help
"""

def analyzeOneFile(filename:str, check_sat:bool, all_models:bool, to_file:bool):
    """Analyze one file 
    
    Args:
        filename: name of file to analyze.
        check_sat: tell if we must only check set of clause or if we will generate all models.
        all_models: enables to know if all models will be generated or no.
        to_file: if it is True it enables to redirect output result to a file which is automatically created in the same directory with input_file.

    Returns:
        None

    """
    d = DataProcessing()
    C = d.getClauseFromFile(filename)
    d.countVars(C)
    varHeuristic = LevelTwoVariableChoiceHeuristic(d.vars)

    dpll = Dpll(C, d.nb_vars, varHeuristic, ALLMODEL=all_models, CSAT=check_sat)
    dpll.checkSetOfClauses()
    report_name = filename[:-4] + "_report_"+("OnlyCheckSAT" if check_sat else "Model")+".txt"
    dpll.summary(report_name, to_file)

    print("THANK YOU")

def analyzeFilesFromDir(input_dir:str, check_sat:bool, all_models:bool, to_file:bool):
    """Analyze all files in a specified directory

    Args:
        filename: name of file to analyze.
        check_sat: tell if we must only check set of clause or if we will generate all models.
        all_models: enables to know if all models will be generated or no.
        to_file: if it is True it enables to redirect output result to a file which is automatically created in the same directory with input files.
    
    Returns:
        None

    """

    d = DataProcessing()
    files = d.getCnfFilesFromDirectory(input_dir)

    for f in files:
        print("=== File to analyze: '"+f+"'...")
        C = d.getClauseFromFile(f)
        d.countVars(C)
        varHeuristic = LevelTwoVariableChoiceHeuristic(d.vars)
        dpll = Dpll(C, d.nb_vars, varHeuristic, ALLMODEL=all_models, CSAT=check_sat)
        dpll.checkSetOfClauses()
        report_name = f[:-4] + "_report_"+("OnlyCheckSAT" if check_sat else "Model")+".txt"
        dpll.summary(report_name, to_file)
    print("THANK YOU!!!")

def main():
    """Entry point of program
    
    Note: 
        - only_check 
        - input_file (file cnf which will be analyzed)
        - input_dir (folder in which contains all cnf files)
        - to_file (bool)
        - all_model (bool)

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--all_model", help="Get all complete models of set of clause (C)", action="store_true")
    parser.add_argument("--only_check", help="Only check set of clause (C) if it is SAT or UNSAT", action="store_true")
    parser.add_argument("--to_file", help="Generate analyze report in file (file will be automatically created in same directory like input file) or in terminal", action="store_true")
    parser.add_argument("--input_file", help="Path to file cnf which will be analyzed")
    parser.add_argument("--input_dir", help="Path of folder in which contains all cnf files")
    args = parser.parse_args()


    if args.input_file:
        if not path.isfile(args.input_file):
            print("Input file specified doesn't exist")
            return
        analyzeOneFile(args.input_file, args.only_check, args.all_model, args.to_file)

    elif args.input_dir:
        if not path.isdir(args.input_dir):
            print("Input dir specified doesn't exist")
            return
        analyzeFilesFromDir(args.input_dir, args.only_check, args.all_model, args.to_file)
    else:
        print("Input file or directory must be specified")

if __name__=="__main__":
    main()
