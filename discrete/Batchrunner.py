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

floor_plans = [f for f in listdir("floorplans")]

variables = {'num_vars': 1,
             'floorplan': floor_plans[0],
             'names': ['human_count'],
             'bounds': [[1, 80]]}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 10
max_steps = 100
distinct_samples = 10

# We get all our samples here
param_values = saltelli.sample(variables, distinct_samples)

# Set the outputs
model_reporters = {'Escaped': lambda m: m.schedule_Human.get_agent_count()}

batch = BatchRunner(Classroom,
                    max_steps=max_steps,
                    variable_parameters={name: [] for name in variables['names']},
                    fixed_parameters={"floorplan": variables['floorplan']},
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

        batch.run_iteration(variable_parameters, tuple(vals), count)
        count += 1

        clear_output()
        print(f'{count / (len(param_values) * replicates) * 100:.2f}% done')

data = batch.get_model_vars_dataframe()

