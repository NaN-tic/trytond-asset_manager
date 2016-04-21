# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from datetime import datetime
from sql import Literal
from sql.conditionals import Coalesce

from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.transaction import Transaction
from trytond.modules.asset.asset import AssetAssignmentMixin

__all__ = ['Asset', 'AssetManager']
__metaclass__ = PoolMeta


class AssetManager(AssetAssignmentMixin):
    'Asset Manager'

    __name__ = 'asset.manager'

    manager = fields.Many2One('party.party', 'Manager')
    contact = fields.Many2One('party.party', 'Contact')
    asset = fields.Many2One('asset', 'Asset')
    manager_reference = fields.Char('Manager Reference')


class Asset:

    __name__ = 'asset'
    managers = fields.One2Many('asset.manager', 'asset', 'Managers')
    current_manager = fields.Function(fields.Many2One('party.party',
        'Current Manager'), 'get_current_manager',
        searcher='search_current_manager')
    current_manager_contact = fields.Function(fields.Many2One('party.party',
        'Current Manager Contact'), 'get_current_manager')

    @classmethod
    def get_current_manager(cls, assets, names):
        pool = Pool()
        AssetManager = pool.get('asset.manager')
        assigments = cls.get_current_values(assets, AssetManager)
        result = {}
        for name in names:
            result[name] = dict((i.id, None) for i in assets)

        for asset, assigment_id in assigments.iteritems():
            if not assigment_id:
                continue
            assigment = AssetManager(assigment_id)
            result['current_manager'][asset] = assigment.manager and  \
                assigment.manager.id
            result['current_manager_contact'][asset] = assigment.contact and \
                assigment.contact.id
        return result

    @classmethod
    def search_current_manager(cls, name, clause):
        pool = Pool()
        Date = pool.get('ir.date')
        AssetManager = pool.get('asset.manager')
        Party = pool.get('party.party')
        transaction = Transaction()
        table = AssetManager.__table__()
        party = Party.__table__()
        condition = party.id == table.manager
        tables = {
            None: (table, None),
            'manager': {
                None: (party, condition),
                }
            }
        date = transaction.context.get('_datetime', Date.today())
        if isinstance(date, datetime):
            date = date.date()
        clause[0] = 'manager'
        expression = AssetManager.manager.convert_domain(clause, tables,
            AssetManager)
        query = party.join(table, condition=condition).select(
            table.asset, where=(
                (Literal(date) >= Coalesce(table.from_date, date.min))
                & (Literal(date) <= Coalesce(table.through_date, date.max))
                & expression))
        return [('id', 'in', query)]
