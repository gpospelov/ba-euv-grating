"""
Collection of utilities to load json description
"""

import os
import json


def load_experimental_setup(config_name):
    """
    Loads json description of 3 experiments from current directory.
    """
    return load_setup("experiments.json", config_name)


def load_sample_setup(config_name):
    """
    Loads json description of 3 experiments from current directory.
    """
    return load_setup("gratings.json", config_name)


def load_setup(json_filename, config_name):
    """
    Loads json description from given filename corresponding to given config_name
    """
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", json_filename)
    print("{0}".format('-'*80))
    print("'{0}' ==> '{1}'".format(json_filename, config_name))
    print("{0}".format('-'*80))
    with open(filename) as json_file:
        return json.load(json_file)[config_name]
