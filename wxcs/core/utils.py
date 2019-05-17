"""Core component utility functions."""
import os
from flask import current_app, json
from wxcs import db
from wxcs.models import UserLog


def load_cases():
    """Load the weather cases from JSON."""
    filename = os.path.join(current_app.static_folder, 'cases.json')
    with open(filename) as cases:
        data = json.load(cases)
    return data


def get_cases_list(cases):
    """Output the filtered list of cases."""
    return [(i['id'], i['title']) for i in cases]


def add_userlog(userlog):
    """Add the log to the database."""
    userlog_obj = UserLog(
        name=userlog['name'],
        post=userlog['post'],
        wxid=userlog['wxid'],
        role=userlog['role'])
    db.session.add(userlog_obj)
    db.session.commit()
    return True

# TODO: Change time function
# ENHANCE: Sync mini station Time (Kwong)

# TODO: Sync back time function
