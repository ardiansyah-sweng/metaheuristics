import math
import sys, random
from typing import List

class MultimodalFunctionsInterface:
    def multimodal(self):
        pass

class F1Sphere(MultimodalFunctionsInterface):
    def multimodal(self, variables):
        results = [x ** 2 for x in variables]
        return sum(results)

class F2Schwefel2_22(MultimodalFunctionsInterface):
    def multimodal(self, variables:List[float]):
        absolute_numbers = [abs(variable) for variable in variables]
        results = [abs(variable) + abs_product for variable, abs_product in zip(variables, absolute_numbers)]
        absolute_numbers = []
        if sum(results) == 0 or float('inf') in results:
            return 0.00000001
        return sum(results)

class F3Schwefel1_2(MultimodalFunctionsInterface):
    def multimodal(self, variables: List[float]):
        powers = []
        results = []
        for key in range(len(variables)):
            for i in range(key + 1):
                powers.append(variables[i] ** 2)
            results.append(sum(powers))
            powers = []
        return sum(results)

class F4Schwefel2_21(MultimodalFunctionsInterface):
    def multimodal(self, variables: List[float]):
        absolute_numbers = [abs(variable) for variable in variables]
        return max(absolute_numbers)

class F5Rosenbrock(MultimodalFunctionsInterface):
    def multimodal(self, variables: List[float]):
        results = []
        for key, variable in enumerate(variables):
            if key < (len(variables) - 1):
                result = 100 * (variables[key + 1] - variable ** 2) ** 2 + (variable - 1) ** 2
                results.append(result)
        return sum(results)

class F6Step(MultimodalFunctionsInterface):
    def multimodal(self, variables: List[float]):
        results = [(variable + 0.5) ** 2 for variable in variables]
        return sum(results)

class F7QuarticNoise(MultimodalFunctionsInterface):
    def multimodal(self, variables: List[float]):
        results = []
        for key, variable in enumerate(variables):
            key += 1
            result = key * variable ** 4 + random.uniform(0,1)
            results.append(result)
        return sum(results)

class F8Schwefel2_26(MultimodalFunctionsInterface):
    def multimodal(self, variables):
        results = []
        for variable in variables:
            if isinstance(variable, list):
                variable = [float(val) for val in variable]
                results.extend([-val * math.sin(math.sqrt(abs(val)))
                               for val in variable])
            else:
                variable = float(variable)
                results.append(-variable * math.sin(math.sqrt(abs(variable))))
        return sum(results)

class F9Rastrigin(MultimodalFunctionsInterface):
    def multimodal(self, variables):
        results = []
        for variable in variables:
            if isinstance(variable, list):
                variable = [float(val) for val in variable]
                results.extend(
                    [val**2 - 10 * math.cos(2 * math.pi * val) + 10 for val in variable])
            else:
                variable = float(variable)
                results.append(variable**2 - 10 *
                               math.cos(2 * math.pi * variable) + 10)
        return sum(results)


class F10Ackley(MultimodalFunctionsInterface):
    def multimodal(self, variables):
        results = []
        results1 = []
        results2 = []
        for variable in variables:
            if isinstance(variable, list):
                variable = [float(val) for val in variable]
                results1.extend([val**2 for val in variable])
                results2.extend([math.cos(2 * math.pi * val)
                                for val in variable])
                results.extend([-20 * math.exp(-0.2 * math.sqrt(1/len(variable)) * sum(results1)) -
                               math.exp((1/len(variable)) * sum(results2)) + 20 + math.e for val in variable])
            else:
                variable = float(variable)
                results1.append(variable**2)
                results2.append(math.cos(2 * math.pi * variable))
                results.append(-20 * math.exp(-0.2 * math.sqrt(1/len(variables)) * sum(
                    results1)) - math.exp((1/len(variables)) * sum(results2)) + 20 + math.e)
        return sum(results)


class F11Griewank(MultimodalFunctionsInterface):
    def multimodal(self, variables):
        results = []
        results1 = []
        results2 = []
        for key, variable in enumerate(variables):
            if isinstance(variable, list):
                variable = [float(val) for val in variable]
                key = key + 1
                results1.extend([val**2 for val in variable])
                results2.extend(
                    [math.cos(val / (math.sqrt(key))) + 1 for val in variable])
            else:
                variable = float(variable)
                key = key + 1
                results1.append(variable**2)
                results2.append(math.cos(variable / (math.sqrt(key))) + 1)
            results.append((1/4000) * sum(results1) - math.prod(results2))
        return sum(results)


class F12Penalized(MultimodalFunctionsInterface):
    def y(self, variable):
        if isinstance(variable, list):
            return [1 + (float(val) + 1) / 4 for val in variable]
        else:
            return 1 + (float(variable) + 1) / 4

    def calculate_u(self, variable, a, k, m):
        variable = float(variable)
        one = k * (variable - a)**m * variable
        two = k * (-variable - a)**m * variable

        if one > a:
            return one
        elif two < a:
            return two
        else:
            return 0  # Tambahkan pernyataan 'else' untuk mengembalikan 0 jika kondisi di atas tidak terpenuhi

    def u(self, variable, a, k, m):
        if isinstance(variable, list):
            return [self.calculate_u(val, a, k, m) for val in variable]
        else:
            return self.calculate_u(float(variable), a, k, m)

    def multimodal(self, variables):
        a = 10
        k = 100
        m = 4
        results1 = []
        results2 = []
        for key, variable in enumerate(variables):
            if isinstance(variable, list):
                variable = [float(val) for val in variable]
                if key < len(variables) - 1:
                    for val in variable:
                        results1.append(
                            self.y(val)**2 * (1 + 10 * math.sin(math.pi * self.y(val))**2))
                        results2.append(self.u(val, a, k, m))
            else:
                variable = float(variable)
                if key < len(variables) - 1:
                    results1.append(self.y(
                        variable)**2 * (1 + 10 * math.sin(math.pi * self.y(variables[key + 1]))**2))
                    results2.append(self.u(variable, a, k, m))
        y1 = self.y(variables[0])
        return (math.pi / len(variables)) * (10 * math.sin(math.pi * y1)) + sum(results1) + sum(results2)

class MultimodalFunctionsFactory:
    def initializingMultimodalFunctions(function, variableValues):
        functions = [
            {'function': 'f1', 'select': F1Sphere().multimodal(variableValues)},
            {'function': 'f2', 'select': F2Schwefel2_22().multimodal(variableValues)},
            {'function': 'f3', 'select': F3Schwefel1_2().multimodal(variableValues)},
            {'function': 'f4', 'select': F4Schwefel2_21().multimodal(variableValues)},
            {'function': 'f5', 'select': F5Rosenbrock().multimodal(variableValues)},
            {'function': 'f6', 'select': F6Step().multimodal(variableValues)},
            {'function': 'f7', 'select': F7QuarticNoise().multimodal(variableValues)},
            {'function': 'f8', 'select': F8Schwefel2_26().multimodal(variableValues)},
            {'function': 'f9', 'select': F9Rastrigin().multimodal(variableValues)},
            {'function': 'f10', 'select': F10Ackley().multimodal(variableValues)},
            {'function': 'f11', 'select': F11Griewank().multimodal(variableValues)},
            {'function': 'f12', 'select': F12Penalized().multimodal(variableValues)}
        ]
        index = next((i for i, item in enumerate(functions)
                     if item["function"] == function), None)
        return functions[index]['select']
