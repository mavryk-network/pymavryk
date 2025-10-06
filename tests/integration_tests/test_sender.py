from unittest import TestCase
from unittest import skip

from pymavryk import ContractInterface

code = """
parameter unit;
storage address;
code { DROP ;
       SENDER ;
       NIL operation ;
       PAIR }
"""
initial = 'mv1FqR6EkLMrTMku3s13Vy2yaCYmeUmLf1MD'
source = 'mv1PbRvVt7gXT9CcGMDw45AAS7dXoh4awkxs'
sender = 'KT1WhouvVKZFH94VXj9pa8v4szvfrBwXoBUj'


class SenderContractTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ci = ContractInterface.from_michelson(code).using(shell='https://atlasnet.rpc.mavryk.network')

    def test_sender(self):
        res = self.ci.default().run_code(storage=initial, source=source, sender=sender)
        self.assertEqual(sender, res.storage)

    def test_no_source(self):
        res = self.ci.default().run_code(storage=initial, sender=sender)
        self.assertEqual(sender, res.storage)

    def test_no_sender(self):
        res = self.ci.default().run_code(storage=initial, source=source)
        self.assertEqual(source, res.storage)
