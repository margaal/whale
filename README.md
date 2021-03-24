# Whale
whale is a "small" SAT solver based on DPLL iterative algorithm. Given a set of clauses retrieved from a file in DIMACS format, Whale enables to know if this set of clauses is SATISFIABLE (SAT) or UNSATISFIABLE (UNSAT).

## Features

- Checking of a set of clauses: if it is SAT or UNSAT (it returns partial model if the set of clauses is SAT)
- Finding a partial model or a complete model of a set of clauses
- Finding all complete models of a set of clauses
- Scanning cnf files from a folder
- format the results in a file or on the console

## Installation
According to my tests, this installation method work for Windows, Linux or Mac OS. 
1. Make sure you have python installed
2. Download this project
3. Open your terminal and place current directory in download project root directory `python setup.py install`
*Perhaps on linux you must write *sudo python3* instead of *python*. So, after installation is done, you can execute program*
```
whale -h
```

## Usage
- Check if a set of clauses(which is in .cnf file) is SAT or UNSAT and put the result in file.
`whale --only_check --to_file --input_file ../data/dimacs_test_file.cnf`
**OUTPUT**:
```
===Analysis is done and we can find report: '../data/dimacs_test_file_report_OnlyCheckSAT.txt'
THANK YOU
```
- Check all Dimacs files(.cnf) of a specific directory are SAT or UNSAT 
`whale --only_check --to_file --input_dir ../data`
**OUTPUT**:
```
=== File to analyze: '../data/dimacs_test_file1.cnf'...
===Analysis is done and we can find report: '../data/dimacs_test_file1_report_OnlyCheckSAT.txt'
=== File to analyze: '../data/dimacs_test_file2.cnf'...
===Analysis is done and we can find report: '../data/dimacs_test_file1_report_OnlyCheckSAT.txt'
THANK YOU!!!
```
Hope you will have the pleasure to check out the other features

## Contributing
 
Feel free to contribute in order to improve this program
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
 
## History
 
Version 1.0 (2021-03-23) - DPLL iterative algorithm
 
## Credits
 
- Marcelin SEBLE (contact@margaal.com)
 
## License
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
The MIT License (MIT)

Copyright (c) 2021 Marcelin SEBLE