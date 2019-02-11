from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from erpfil.auth import login_required
from erpfil.db import get_db

bp = Blueprint('customers', __name__, url_prefix='/customers')


@bp.route('/')
def index():
    """Show all the customers."""
    db = get_db()
    customers = db.execute(
        'SELECT p.id, title, manager_id, username'
        ' FROM customer p JOIN user u ON p.manager_id = u.id'
        ' ORDER BY p.title'
    ).fetchall()
    return render_template('customers/index.html', customers=customers)


def get_customer(id, check_manager=False):
    """Get a customer and its manager by id.

    Checks that the id exists and optionally that the current user is
    the deal's owner.

    :param id: id of the customer to get
    :param check_manager: require the current user to be the customer's manager
    :return: the customer with manager information
    :raise 404: if a customer with the given id doesn't exist
    :raise 403: if the current user cannot get the customer
    """
    customer = get_db().execute(
        'SELECT p.id, title, body, created, manager_id, username'
        ' FROM customer p JOIN user u ON p.manager_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if customer is None:
        abort(404, "Customer id {0} doesn't exist.".format(id))

    if check_manager and customer['manager_id'] != g.user['id']:
        abort(403)

    return customer


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new customer for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        full_name = request.form['full_name']
        phone = request.form['phone']
        website = request.form['website']
        contact_person = request.form['contact_person']
        address = request.form['address']
        note = request.form['note']
        error = None

        if not title:
            error = 'Не указано название контрагента.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO customer '
                '(title, full_name, phone, website, contact_person, address, note, manager_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (title, full_name, phone, website, contact_person, address, note, g.user['id'])
            )
            db.commit()
            return redirect(url_for('customers.index'))

    return render_template('customers/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a customer if the current user is logged in."""
    deal = get_customer(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['full_name']
        error = None

        if not title:
            error = 'Не указано название контрагента.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE customer SET title = ?, full_name = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('customers.index'))

    return render_template('customers/update.html', deal=deal)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a customer.

    Ensures that the customer exists.
    """
    get_customer(id)
    db = get_db()
    db.execute('DELETE FROM customer WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('customers.index'))
