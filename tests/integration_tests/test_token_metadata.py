from unittest import TestCase
from unittest import skip

from pymavryk import pymavryk

#TODO: Fix when Mavryk mainnet is deployed
class TestTokenMetadata(TestCase):
    def test_from_storage(self):
        ...
        # contract = pymavryk.using('mainnet').contract('KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton')
        # token_metadata = contract.token_metadata[24552]
        # self.assertEqual('Ordo Ad Chaos', token_metadata.name)

    def test_from_view(self):
        ...
        # contract = pymavryk.using('mainnet').contract('KT1REEb5VxWRjcHm5GzDMwErMmNFftsE5Gpf')
        # token_metadata = contract.token_metadata[0]
        # self.assertEqual('Stably USD', token_metadata.name)
