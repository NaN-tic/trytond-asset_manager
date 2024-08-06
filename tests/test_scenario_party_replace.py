import unittest

from proteus import Model, Wizard
from trytond.modules.company.tests.tools import create_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install asset_maintenance
        activate_modules('asset_manager')

        # Create company
        _ = create_company()

        # Create a party
        Party = Model.get('party.party')
        party = Party(name='Customer')
        party.save()
        party2 = Party(name='Customer')
        party2.save()

        # Create asset
        Asset = Model.get('asset')
        Manager = Model.get('asset.manager')
        asset = Asset()
        asset.name = 'Asset'
        asset.save()
        manager = Manager()
        manager.asset = asset
        manager.manager = party
        manager.contact = party
        manager.save()

        # Try replace active party
        replace = Wizard('party.replace', models=[party])
        replace.form.source = party
        replace.form.destination = party2
        replace.execute('replace')

        # Check fields have been replaced
        manager.reload()
        self.assertEqual(manager.manager, party2)
        self.assertEqual(manager.contact, party2)
