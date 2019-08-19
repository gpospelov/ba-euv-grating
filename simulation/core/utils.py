"""
Collection of utilities to load json description
"""

import os
import json


def load_setup(json_filename, config_name=None):
    """
    Loads json description from given filename corresponding to given config_name
    """
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", json_filename)
    print("{0}".format('-'*80))
    print("'{0}' ==> '{1}'".format(json_filename, config_name))
    print("{0}".format('-'*80))
    with open(filename) as json_file:
        data = json.load(json_file)
        if config_name:
            return data[config_name]
        else:
            return data
