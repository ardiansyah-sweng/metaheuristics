def getOptimizerParameter(optimizerID):
    optimizerParameters = {
        # H. Peng, W. Zhu, C. Deng, and Z. Wu, “Enhancing firefly algorithm with courtship learning,” Inf. Sci. (Ny)., vol. 543, pp. 18–42, 2020, doi: 10.1016/j.ins.2020.05.111.
        'fa': {
            'alpha': 0.5,
            'betaMin': 0.2,
            'beta': 1,
            'gamma': 1,
            'minEpsilon': -5,
            'maxEpsilon': 5,
            'populationSize': 20,
            'maxIter': 20
        },
        'pso': {
            'inertiaMax': 0.9,
            'inertiaMin': 0.4,
            'c1': 2,
            'c2': 2,
            'populationSize': 70,
            'maxIter': 20
        },
        'ga': {
            'crossoverRate': 0.25,
            'mutationRate': 0.1,
            'populationSize': 20,
            'maxIter': 20
        },
        # M. H. Nadimi-Shahraki, S. Taghian, and S. Mirjalili, “An improved grey wolf optimizer for solving engineering problems,” Expert Syst. Appl., vol. 166, no. August 2020, p. 113917, 2021, doi: 10.1016/j.eswa.2020.113917.
        'gwo': {
            'populationSize': 100,
            'maxIter': 20
        },
        # [1] L. Abualigah, M. A. Elaziz, P. Sumari, Z. W. Geem, and A. H. Gandomi, “Reptile Search Algorithm (RSA): A nature-inspired meta-heuristic optimizer,” Expert Syst. Appl., vol. 191, no. November, p. 116158, Apr. 2022, doi: 10.1016/j.eswa.2021.116158.
        'rsa': {
            'alpha': 0.1,
            'beta': 0.1,
            'smallNumber': 0.0000001,
            'populationSize': 30,
            'maxIter': 20
        }
    }    
    return optimizerParameters[optimizerID]
