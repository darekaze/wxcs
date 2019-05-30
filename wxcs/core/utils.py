"""Core component utility functions."""
import sys
from flask import session, flash
from datetime import datetime
from ntplib import NTPClient
from wxcs import db
from wxcs.models import Case, UserLog
from wxcs.schemas import CaseSchema

case_schema = CaseSchema()


def get_cases_list():
    """Output the filtered list of cases."""
    return Case.query.with_entities(Case.id, Case.title).all()


def get_case_details(id):
    """Return the case detail with specifies id."""
    return Case.query.get(id)


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
    case = get_case_details(wxid)
    time_setted = set_time(case.start_at)
    session['drill'] = case_schema.dump(case).data

    # ENHANCE: Sync mini station Time (Kwong)
    if time_setted:
        flash(f'Drill has been initialized! (Clock will refresh within 30s)', 'success')
    else:
        flash('The time has not setup correctly. You may need to sync the time manually...', 'warning')


def end_drill():
    """Procedure for terminating the drill."""
    if 'drill' in session:
        time_str = request_ntp('ntp.nict.jp', version=3)
        set_time(time_str)
    session.pop('userlog', None)
    session.pop('drill', None)
