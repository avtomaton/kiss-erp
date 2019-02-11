from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from erpfil.auth import login_required
from erpfil.db import get_db

bp = Blueprint('deals', __name__, url_prefix='/deals')


@bp.route('/')
def index():
    """Show all the deals, most recent first."""
    db = get_db()
    deals = db.execute(
        'SELECT p.id, p.title, body, p.created, p.manager_id, customer_id,'
        ' username, c.title AS customer_title'
        ' FROM deal p'
        ' JOIN user u ON p.manager_id = u.id'
        ' JOIN customer c ON p.customer_id = c.id'
        ' ORDER BY p.created DESC'
    ).fetchall()
    return render_template('deals/index.html', deals=deals)


def get_deal(id, check_manager=True):
    """Get a deal and its manager by id.

    Checks that the id exists and optionally that the current user is
    the deal's owner.

    :param id: id of the deal to get
    :param check_manager: require the current user to be the owner
    :return: the deal with manager information
    :raise 404: if a deal with the given id doesn't exist
    :raise 403: if the current user isn't the owner
    """
    deal = get_db().execute(
        'SELECT p.id, p.title, body, p.created, p.manager_id, customer_id, username'
        ' FROM deal p'
        ' JOIN user u ON p.manager_id = u.id'
        ' JOIN customer c ON p.customer_id = c.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if deal is None:
        abort(404, "Deal id {0} doesn't exist.".format(id))

    if check_manager and deal['manager_id'] != g.user['id']:
        abort(403)

    return deal


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new deal for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        customer_id = request.form['customer']
        error = None

        if not title:
            error = 'не указано название.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO deal (title, body, manager_id, customer_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], customer_id)
            )
            db.commit()
            return redirect(url_for('deals.index'))

    db = get_db()
    customers = db.execute(
        'SELECT id, title FROM customer ORDER BY title'
    ).fetchall()

    return render_template('deals/create.html', customers=customers)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a deal if the current user is the deal's manager."""
    deal = get_deal(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Не указано название.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE deal SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('deals.index'))

    return render_template('deals/update.html', deal=deal)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a deal.

    Ensures that the deal exists and that the logged in user is the
    deal's manager.
    """
    get_deal(id)
    db = get_db()
    db.execute('DELETE FROM deal WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('deals.index'))
