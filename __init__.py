# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import asset
from . import party


def register():
    Pool.register(
        asset.Asset,
        asset.AssetManager,
        module='asset_manager', type_='model')
    Pool.register(
        party.PartyReplace,
        module='asset_manager', type_='wizard')
