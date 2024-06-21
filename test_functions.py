def getTestFunctionParameters(testFunctionID):
    testFunctions = {
        'f1':{
            'code': 'F1',
            'name': 'Sphere',
            'dimension': 30,
            'ranges': [-100, 100]
        },
        'f2':{
            'code': 'F2',
            'name': 'Schwefel 2.22',
            'dimension': 30,
            'ranges': [-10, 10]
        },
        'f3':{
            'code': 'F3',
            'name': 'Schwefel 1.2',
            'dimension': 30,
            'ranges': [-100, 100]
        },
        'f4':{
            'code': 'F4',
            'name': 'Schwefel 2.21',
            'dimension': 30,
            'ranges': [-100, 100]
        },
        'f5':{
            'code': 'F5',
            'name': 'Rosenbrock',
            'dimension': 30,
            'ranges': [-30, 30]
        },
        'f6':{
            'code': 'F6',
            'name': 'Step',
            'dimension': 30,
            'ranges': [-100, 100]
        },
        'f7':{
            'code': 'F7',
            'name': 'Step',
            'dimension': 30,
            'ranges': [-100, 100]
        },
        'f8':{
            'code': 'F8',
            'name': 'Schwefel2_26',
            'dimension': 30,
            'ranges': [-500, 500]
        },
        'f9':{
            'code': 'F9',
            'name': 'Rastrigin',
            'dimension': 30,
            'ranges': [-5.12, 5.12]
        },
        'f10':{
            'code': 'F10',
            'name': 'Ackley',
            'dimension': 30,
            'ranges': [-32, 32]
        },
        'f11':{
            'code': 'F11',
            'name': 'Griewank',
            'dimension': 30,
            'ranges': [-600, 600]
        },
        'f12':{
            'code': 'F12',
            'name': 'Penalized',
            'dimension': 30,
            'ranges': [-50, 50]
        }
    }
    return testFunctions[testFunctionID]