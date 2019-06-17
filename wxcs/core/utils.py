"""Core component utility functions."""
from flask import session, flash
from collections import defaultdict
from datetime import datetime
from ntplib import NTPClient
from wxcs import db
from wxcs.models import Case, UserLog
from wxcs.schemas import CaseSchema, LinkSchema, LinkEnum
from wxcs.core.privileged.time_utils import set_time

case_schema = CaseSchema()
link_schema = LinkSchema()


def get_cases_list():
    """Output the filtered list of cases."""
    return Case.query.with_entities(Case.id, Case.title).all()


def get_case_details(id):
    """Return the case detail with specifies id."""
    return Case.query.get(id)


def get_toolset(id):
    """Return toolsets list."""
    case = get_case_details(id)
    links = defaultdict(list)
    for link in case.links:
        li = link_schema.dump(link).data
        category = LinkEnum(li['ctg']).name
        links[category].append(li)
    return dict(links)


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


def request_ntp(server='ntp.nict.jp', version=3):
    """Request time from time server."""
    c = NTPClient()
    response = c.request('ntp.nict.jp', version=3)
    return datetime.fromtimestamp(response.tx_time).strftime('%Y-%m-%d %H:%M:%S')


def init_drill(wxid):
    """Initialize drill: change time and set drill session."""
    case = get_case_details(wxid)
    time_str = (case.start_at).strftime('%Y-%m-%d %H:%M:%S')
    time_setted = set_time(time_str)

    if time_setted:
        flash('Drill has been initialized! (Clock will refresh within 30s)', 'success')
    else:
        flash('The time has not setup correctly. You may need to sync the time manually...', 'warning')

    session['drill'] = case_schema.dump(case).data
    return time_setted


def end_drill():
    """Procedure for terminating the drill."""
    if 'userlog' in session:
        time_str = request_ntp('ntp.nict.jp', version=3)
        set_time(time_str)
    session.pop('userlog', None)
