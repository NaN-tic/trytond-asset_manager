======================
Party Replace Scenario
======================

Imports::

    >>> import datetime
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> today = datetime.date(2015, 1, 1)

Install asset_maintenance::

    >>> config = activate_modules('asset_manager')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create a party::

    >>> Party = Model.get('party.party')
    >>> party = Party(name='Customer')
    >>> party.save()
    >>> party2 = Party(name='Customer')
    >>> party2.save()

Create asset::

    >>> Asset = Model.get('asset')
    >>> Manager = Model.get('asset.manager')
    >>> asset = Asset()
    >>> asset.name = 'Asset'
    >>> asset.save()
    >>> manager = Manager()
    >>> manager.asset = asset
    >>> manager.manager = party
    >>> manager.contact = party
    >>> manager.save()

Try replace active party::

    >>> replace = Wizard('party.replace', models=[party])
    >>> replace.form.source = party
    >>> replace.form.destination = party2
    >>> replace.execute('replace')

Check fields have been replaced::

    >>> manager.reload()
    >>> manager.manager == party2
    True
    >>> manager.contact == party2
    True
