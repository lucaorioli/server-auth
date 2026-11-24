# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.modules.neutralize import get_neutralization_queries

from odoo.addons.base.tests.common import BaseCommon


class TestNeutralize(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vault = cls.env["vault"].create({"name": "Vault"})
        cls.entry = cls.env["vault.entry"].create(
            {"vault_id": cls.vault.id, "name": "Entry"}
        )
        cls.env["vault.field"].create(
            {"entry_id": cls.entry.id, "name": "Password", "value": "secret"}
        )
        cls.env["vault.file"].create(
            {"entry_id": cls.entry.id, "name": "Key file", "value": b"c2VjcmV0"}
        )
        cls.env["vault.inbox"].create(
            {
                "name": "Inbox",
                "user_id": cls.env.uid,
                "secret": "secret",
                "key": "key",
                "iv": "iv",
            }
        )

    def test_neutralize(self):
        self.env.flush_all()
        for query in get_neutralization_queries(["vault"]):
            self.env.cr.execute(query)
        self.env.invalidate_all()

        self.assertFalse(self.env["vault.field"].search([]))
        self.assertFalse(self.env["vault.file"].search([]))
        self.assertFalse(self.env["vault.inbox"].search([]))
        # the structure is kept
        self.assertTrue(self.vault.exists())
        self.assertTrue(self.entry.exists())
        self.assertTrue(self.vault.right_ids)
