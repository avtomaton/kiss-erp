import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def format_post_val(s):
    """Return string if not empty or None otherwise.
    """
    s = s.strip()
    return s if s else None


def format_db_val(val):
    """Return stripped string for string type or the the other value as is.
    """
    if isinstance(val, str):
        return val.strip()
    else:
        return val


def update_db_str(table, key_val):
    """
    Construct UPDATE statement string and corresponding tuple of values.

    :param key_val:
    :return: data prepared for db_execute.
    """
    prefix = "UPDATE {} SET ".format(table)
    values = []
    for key, val in key_val.items():
        prefix += "{} = ?, ".format(key)
        values.append(val)
    prefix = prefix[:-2] + " "
    return prefix, tuple(values)


def insert_db_str(table, key_val):
    """
    Construct INSERT statement string and corresponding tuple of values.

    :param key_val: field names and values
    :return: data prepared for db_execute.
    """
    prefix = "INSERT INTO {} ".format(table)
    field_names = ''
    field_val_str = ''
    values = []
    for key, val in key_val.items():
        field_names += "{}, ".format(key)
        field_val_str += '?, '
        values.append(val)
    field_names = field_names[:-2] + ' '
    field_val_str = field_val_str[:-2] + ' '
    prefix += '(' + field_names + ') VALUES (' + field_val_str + ') '
    return prefix, tuple(values)


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    with current_app.open_resource('initial-data-ru.sql') as f:
        db.executescript(f.read().decode('utf8'))


def db_ru_defaults():
    """Fill the database with the default preset."""
    db = get_db()
    db.execute('DELETE FROM user')
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        ('VP', generate_password_hash('123456'))
    )
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        ('TT', generate_password_hash('123456'))
    )
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        ('YS', generate_password_hash('123456'))
    )
    db.commit()

    with current_app.open_resource('initial-data-ru.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('db-ru-defaults')
@with_appcontext
def db_ru_defaults_command():
    """Clear existing data and fill the db with default data."""
    db_ru_defaults()
    click.echo('The database was reset to defaults.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(db_ru_defaults_command)
