"""Core component utility functions."""
import os
from flask import current_app, json


def load_cases():
    """Load the weather cases from JSON."""
    filename = os.path.join(current_app.static_folder, 'cases.json')
    with open(filename) as cases:
        data = json.load(cases)
    return data


def get_cases_list(cases):
    """Output the filtered list of cases."""
    return [(i['id'], i['title']) for i in cases]
