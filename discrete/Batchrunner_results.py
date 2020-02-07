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

"""Change name variable to the variable you want to change"""
"""Bounds are the values which will be varied over"""

variables = {'num_vars': 1,
             'names': ['human_count'],
             'bounds': [[10, 80]]}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 5
max_steps = 1000
distinct_samples = 8

# We get all our samples here
param_values = [[10],[20],[30],[40],[50],[60],[70],[80]]

# Set the outputs
model_reporters = {'Total_steps': lambda m: m.schedule_Human.get_steps()}

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
data.to_csv('data_results.csv')
print(data)

plt.scatter(data['human_count'], data['Total_steps'])
plt.savefig('human_count_total_steps.png')
plt.show()