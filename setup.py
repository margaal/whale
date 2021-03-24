from setuptools import setup, find_packages

setup( 
    name='whale', 
    version='1.0', 
    author='Marcelin SEBLE', 
    author_email="contact@margaal.com",
    description="Simple SAT solver based on DPLL algorithm",
    license="MIT License",
    keywords="Solver SAT DPLL",
    packages=find_packages(), 
    entry_points={ 
        'console_scripts': [ 
            'whale = whale.solvsat:main' 
        ] 
    }, 
    classifiers=[ 
        'Programming Language :: Python :: 3',  
        'Operating System :: OS Independent', 
    ], 
)