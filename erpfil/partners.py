from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from erpfil.auth import login_required
from erpfil.db import get_db

bp = Blueprint('partners', __name__, url_prefix='/partners')


@bp.route('/')
def index():
    """Show all partners."""
    db = get_db()
    partners = db.execute(
        'SELECT p.id, p.title, manager_id, username, partner_type_id, t.title'
        ' FROM partner p'
        ' JOIN user u ON p.manager_id = u.id'
        ' JOIN partner_type t ON partner_type_id = t.id'
        ' ORDER BY p.title'
    ).fetchall()
    return render_template('partners/index.html', partners=partners)


def get_partner(id, check_manager=False):
    """Get a partner and its manager by id.

    Checks that the id exists and optionally that the current user is
    the partner's manager.

    :param id: id of the partner to get
    :param check_manager: require the current user to be the partner's manager
    :return: the partner with manager information
    :raise 404: if a partner with the given id doesn't exist
    :raise 403: if the current user cannot get the partner
    """
    partner = get_db().execute(
        'SELECT p.id, title, body, created, manager_id, username'
        ' FROM partner p'
        ' JOIN user u ON p.manager_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if partner is None:
        abort(404, "Контрагент id {0} не существует.".format(id))

    if check_manager and partner['manager_id'] != g.user['id']:
        abort(403)

    return partner


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new partner for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        partner_type_id = request.form['partner_type']
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
                'INSERT INTO partner '
                ' (title, partner_type_id, full_name,'
                ' phone, website, contact_person, address, note, manager_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, partner_type_id,
                 full_name, phone, website, contact_person, address, note, g.user['id'])
            )
            db.commit()
            return redirect(url_for('partners.index'))

    db = get_db()
    partner_types = db.execute(
        'SELECT id, title'
        ' FROM partner_type p'
        ' ORDER BY title'
    ).fetchall()

    return render_template('partners/create.html', partner_types=partner_types)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a partner if the current user is logged in."""
    deal = get_partner(id)

    if request.method == 'POST':
        title = request.form['title']
        full_name = request.form['full_name']
        error = None

        if not title:
            error = 'Не указано название контрагента.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE partner SET title = ?, full_name = ? WHERE id = ?',
                (title, full_name, id)
            )
            db.commit()
            return redirect(url_for('partners.index'))

    return render_template('partners/update.html', deal=deal)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a partner.

    Ensures that the partner exists.
    """
    get_partner(id)
    db = get_db()
    db.execute('DELETE FROM partner WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('partners.index'))
