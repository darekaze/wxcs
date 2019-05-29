"""Click commands."""
import os
import click
from flask import current_app, json
from flask.cli import with_appcontext
from wxcs import db
from wxcs.models import Case, Link
from datetime import datetime


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
