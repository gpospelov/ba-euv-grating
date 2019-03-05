"""
Collection of utilities to load json description
"""

import os
import json


def load_setup(self, config_name="exp1"):
    """
    Loads json description of 3 experiments from current directory.
    """
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments.json")
    print("{0}\n{1}: '{2}'\n{3}".format('-' * 80, "Experiment", config_name, '-' * 80))
    with open(filename) as json_file:
        return json.load(json_file)[config_name]
