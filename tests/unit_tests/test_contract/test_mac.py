from os.path import dirname
from os.path import join
from unittest import TestCase

from pymavryk import ContractInterface
from pymavryk import Unit
from pymavryk import pymavryk

initial_storage = {
    'admin': {'admin': pymavryk.key.public_key_hash(), 'paused': False},
    'assets': {
        'hook': {
            'hook': """
                { DROP ;
                  PUSH address "KT1V4jijVy1HfVWde6HBVD1cCygZDtFJK4Xz" ; 
                  CONTRACT (pair
                             (pair
                               (list %batch (pair (pair (nat %amount) (option %from_ address))
                                                  (pair (option %to_ address) (nat %token_id))))
                               (address %fa2))
                             (address %operator)) ;
                  IF_NONE { FAIL } {} }
            """,
            'permissions_descriptor': {
                'custom': {
                    'config_api': None,
                    'tag': 'none',
                },
                'operator': 'operator_transfer_permitted',
                'receiver': 'optional_owner_hook',
                'self': 'self_transfer_permitted',
                'sender': 'optional_owner_hook',
            },
        },
        'ledger': {},
        'operators': {},
        'tokens': {},
    },
}


class TestMac(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mac = ContractInterface.from_file(join(dirname(__file__), 'contracts', 'mac.tz'))
        cls.maxDiff = None

    def test_pause(self):
        res = self.mac.pause(True).interpret(
            storage=initial_storage,
            source=pymavryk.key.public_key_hash(),
            sender=pymavryk.key.public_key_hash(),
        )
        self.assertTrue(res.storage['admin']['paused'])

    def test_is_operator_callback(self):
        res = self.mac.is_operator(
            callback='KT1V4jijVy1HfVWde6HBVD1cCygZDtFJK4Xz',  # does not matter
            operator={
                'operator': pymavryk.key.public_key_hash(),
                'owner': pymavryk.key.public_key_hash(),
                'tokens': {'all_tokens': Unit},
            },
        ).interpret(storage=initial_storage)
        self.assertEqual(1, len(res.operations))

    def test_transfer(self):
        pkh = pymavryk.key.public_key_hash()
        initial_storage_balance = initial_storage.copy()
        initial_storage_balance['assets']['ledger'] = {(pkh, 0): 42000}
        res = self.mac.transfer(
            [
                {
                    'amount': 1000,
                    'from_': pkh,
                    'to_': 'mv1Q1GMULqh686DQLWLcdXvnzWiem8k8L19M',
                    'token_id': 0,
                }
            ]
        ).interpret(storage=initial_storage_balance, source=pkh)
        self.assertEqual(len(res.lazy_diff), len(set(map(lambda x: x['id'], res.lazy_diff))))
        self.assertDictEqual(
            {
                (pkh, 0): 41000,
                ('mv1Q1GMULqh686DQLWLcdXvnzWiem8k8L19M', 0): 1000,
            },
            res.storage['assets']['ledger'],
        )
