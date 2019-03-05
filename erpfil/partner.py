from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from erpfil.auth import login_required
from erpfil import db as database

bp = Blueprint('partner', __name__, url_prefix='/partner')


def partner_defaults():
    return {
        'title': '',
        'partner_type_id': 1,
        'full_name': '',
        'phone': '',
        'phone_1': '',
        'website': 'http://',
        'contact_person': '',
        'address': '',
        'note': ''
    }


def partner_fields():
    return ['id'] + [k for k, v in partner_defaults().items()]


def post_values(form):
    return {k: form[k] for k in partner_fields() if k != 'id'}


def fields_with_prefix(prefix, fields):
    """Create the string like
    prefix.field_0 as prefix_field_0, prefix.field_1 AS prefix_field_1 ...
    from prefix and fields list.

    It is a damn python magic which I am not sure that I will remember even tomorrow.

    :param prefix:
    :param fields: list of string keys
    :return:
    """
    return ', '.join([prefix + '.' + ' AS {}_'.format(prefix).join([x] * 2) for x in fields])


@bp.route('/')
def index():
    """Show all partners."""
    db = database.get_db()

    partners = db.execute(
        'SELECT ' + fields_with_prefix('p', partner_fields()) +\
        ', p.manager_id, p.created, username'
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
    db = database.get_db()
    partner = db.execute(
        'SELECT ' + fields_with_prefix('p', partner_fields()) +\
        ', p.manager_id, p.created, username'
        ' FROM partner p'
        ' JOIN user u ON p.manager_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if partner is None:
        abort(404, "Контрагент id {0} не существует.".format(id))

    partner_shiny = {}
    for k in partner.keys():
        if k[:2] == 'p_':
            partner_shiny[k[2:]] = partner[k]
        else:
            partner_shiny[k] = partner[k]
    partner = partner_shiny

    if check_manager and partner['manager_id'] != g.user['id']:
        abort(403)

    return partner


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new partner for the current user."""
    if request.method == 'POST':
        values = post_values(request.form)
        error = None

        if not values['title']:
            error = 'Не указано название контрагента.'

        if error is not None:
            flash(error)
        else:
            db = database.get_db()
            values['manager_id'] = g.user['id']
            prefix, fields = database.insert_db_str('partner', values)
            print(prefix)
            db.execute(prefix, fields)
            db.commit()
            return redirect(url_for('partner.index'))

    db = database.get_db()
    partner_types = db.execute(
        'SELECT id, title'
        ' FROM partner_type p'
        ' ORDER BY title'
    ).fetchall()

    return render_template('partners/update.html',
                           form_name='Создать контрагента',
                           partner_types=partner_types,
                           partner=partner_defaults())


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a partner if the current user is logged in."""
    partner = get_partner(id)

    if request.method == 'POST':
        values = post_values(request.form)
        error = None

        if not values['title']:
            error = 'Не указано название контрагента.'

        if error is not None:
            flash(error)
        else:
            db = database.get_db()
            prefix, fields = database.update_db_str('partner', values)
            db.execute(prefix + ' WHERE id = ?', fields + (id,))
            db.commit()
            return redirect(url_for('partner.index'))

    db = database.get_db()
    partner_types = db.execute(
        'SELECT id, title'
        ' FROM partner_type p'
        ' ORDER BY title'
    ).fetchall()

    return render_template('partners/update.html',
                           form_name='Изменить контрагента',
                           partner_types=partner_types,
                           partner=partner)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a partner.

    Ensures that the partner exists.
    """
    get_partner(id)
    db = database.get_db()
    db.execute('DELETE FROM partner WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('partner.index'))
