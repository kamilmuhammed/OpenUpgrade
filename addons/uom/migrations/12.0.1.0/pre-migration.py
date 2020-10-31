# Copyright 2018 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

column_copies = {
    'uom_uom': [
        ('active', None, None),
    ],
}


def deactivate_uom_constrain_violations(cr):
    openupgrade.logged_query(cr, """SELECT id, category_id FROM uom_uom WHERE uom_type='reference' ORDER BY id;""")
    result = cr.fetchall()
    categories, to_inactive = [], []
    for uom_id, category in result:
        if category in categories:
            to_inactive.append(uom_id)
        categories.append(category)
    if to_inactive:
        openupgrade.logged_query(cr, """UPDATE uom_uom SET active = FALSE WHERE id in %s""", (tuple(to_inactive),))


@openupgrade.migrate(no_version=True, use_env=True)
def migrate(env, version):
    openupgrade.copy_columns(env.cr, column_copies)
    deactivate_uom_constrain_violations(env.cr)
