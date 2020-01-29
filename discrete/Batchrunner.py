""""Run simulation in batch for sensitivity analysis"""
from IPython.core.display import clear_output
from os import listdir
from SALib.sample import saltelli
from model import Classroom
from agents import Human
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

floor_plans = [f for f in listdir("../floorplans")]

variables = {'num_vars': 3,
             'names': ['human_count', 'human_weight', 'human_panic'],
             'bounds': [[2, 20], [1, 3], [0, 0.7]]}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 2
max_steps = 10
distinct_samples = 2

# We get all our samples here
param_values = saltelli.sample(variables, distinct_samples)

# Set the outputs
model_reporters = {'Escaped': lambda m: m.schedule_Human.get_agent_count()}

batch = BatchRunner(Classroom,
                    max_steps=max_steps,
                    variable_parameters={name: [] for name in variables['names']},
                    model_reporters=model_reporters)

count = 0
for i in range(replicates):
    for vals in param_values:
        # Change parameters that should be integers
        vals = list(vals)
        vals[0] = int(vals[0])

        # Transform to dict with parameter names and their values
        variable_parameters = {}
        for name, val in zip(variables['names'], vals):
            variable_parameters[name] = val

        variable_parameters['floorplan'] = floor_plans[0]

        batch.run_iteration(variable_parameters, tuple(vals), count)
        count += 1

        clear_output()
        print(f'{count / (len(param_values) * replicates) * 100:.2f}% done')

data = batch.get_model_vars_dataframe()
print(data)

escape = sobol.analyze(variables, data['Escaped'].as_matrix(), print_to_console=True)

def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')

# First order
plot_index(escape, variables['names'], '1', 'First order sensitivity')
plt.show()

# Second order
plot_index(escape, variables['names'], '2', 'Second order sensitivity')
plt.show()

# Total order
plot_index(escape, variables['names'], 'T', 'Total order sensitivity')
plt.show()