"""Core component utility functions."""
import sys
import os
from flask import current_app, json, session, flash
from datetime import datetime
from ntplib import NTPClient
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


def get_case_details(cases, id):
    """Return the case detail with specifies id."""
    return next(item for item in cases if item['id'] == id)


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


def set_time(time_str):
    """Set system time."""
    if sys.platform == 'win32':
        from .privileged.win32_util import _win_set_time
        ret = _win_set_time(time_str)
    elif sys.platform.startswith('linux'):
        ret = True
    return ret


def request_ntp(server='ntp.nict.jp', version=3):
    """Request time from time server."""
    c = NTPClient()
    response = c.request('ntp.nict.jp', version=3)
    return datetime.fromtimestamp(response.tx_time).strftime('%Y-%m-%d %H:%M:%S')


def init_drill(wxid):
    """Initialize drill: change time and set drill session."""
    cases = load_cases()
    selected_case = get_case_details(cases, wxid)

    if set_time(selected_case['start_at']):
        session['drill'] = True
        flash(f'Welcome to the drill...', 'success')
    else:
        session['drill'] = False
        flash(f'The time has not setup correctly...', 'success')
    # TODO: refine session['drill'] info


def end_drill():
    """Procedure for terminating the drill."""
    time_str = request_ntp('ntp.nict.jp', version=3)
    set_time(time_str)
    session.pop('userlog', None)
    session.pop('drill', None)

# ENHANCE: Sync mini station Time (Kwong)
# TODO: Sync time function, returns time tuple
