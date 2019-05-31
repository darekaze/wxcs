"""Click commands."""
import os
import click
from flask import current_app, json
from flask.cli import with_appcontext
from wxcs import db
from wxcs.models import Case, Link, Usage, Admin
from datetime import datetime
from sqlalchemy.exc import IntegrityError


@click.command()
@with_appcontext
def seed():
    """Seed or update cases and links table in db."""
    cases = get_cases()
    links = get_links()

    db.session.add_all(cases)
    db.session.add_all(links)
    db.session.commit()

    print('Successfully seeded/updated tables in db.')


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


@click.command('sync')
@with_appcontext
def sync_usage():
    """Update usage (case-link relationship) table in db."""
    usage_data = load_json('configs/usage.json')
    for case in usage_data:
        for link_id in case['links']:
            new_entry = Usage(
                codename=case['codename'],
                link_id=link_id
            )
            db.session.merge(new_entry)

    db.session.commit()
    print('Successfully sync/update usage table in db.')


@click.command('mksu')
@click.option('--name', default='su')
@click.option('--pwd', default='secret')
@with_appcontext
def create_su(name, pwd):
    """Create su function."""
    try:
        db.session.add(Admin(username=name, password=pwd))
        db.session.commit()
        print('Account created!')
    except IntegrityError:
        db.session.rollback()
        print('Account creation failed...')


def load_json(paths):
    """Convert Json to dict."""
    filename = os.path.join(current_app.static_folder, paths)
    with open(filename) as cases:
        data = json.load(cases)
    return data


def get_cases():
    """Output cases object list."""
    case_data = load_json('configs/cases.json')
    cases = []
    for item in case_data:
        item['start_at'] = datetime.fromisoformat(item['start_at'])
        item['end_at'] = datetime.fromisoformat(item['end_at'])
        new_entry = Case(**item)
        cases.append(new_entry)
    return cases


def get_links():
    """Output links object list."""
    link_data = load_json('configs/links.json')
    links = []
    for item in link_data:
        new_entry = Link(**item)
        links.append(new_entry)
    return links
