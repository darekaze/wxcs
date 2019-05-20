"""Core component utility functions."""
import os
from flask import current_app, json, session
from wxcs import db
from wxcs.models import UserLog
# from .privileged.set_time import


def load_cases():
    """Load the weather cases from JSON."""
    filename = os.path.join(current_app.static_folder, 'cases.json')
    with open(filename) as cases:
        data = json.load(cases)
    return data


def get_cases_list(cases):
    """Output the filtered list of cases."""
    return [(i['id'], i['title']) for i in cases]


def set_userlog(userlog):
    """Add the log to the database and set the session."""
    userlog_obj = UserLog(
        name=userlog['name'],
        post=userlog['post'],
        wxid=userlog['wxid'],
        role=userlog['role'])
    db.session.add(userlog_obj)
    db.session.commit()
    session['userlog'] = userlog
    return None


def init_drill():
    """Initialize drill: change time and set drill session."""
    # Change the local time
    # TODO: If success, change the time and activate session['drilling'] = True
