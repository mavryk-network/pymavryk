from unittest import TestCase
from unittest import skip

from pymavryk import pymavryk


class TestRegression(TestCase):
    # TODO: Fix when Mavryk mainnet is deployed
    def test_kusd_get_balance_view(self):
        # fa12 = pymavryk.using('mainnet').contract('KT1K9gCRgaLRFKTErYt1wVxA3Frb9FjasjTV')
        fa12 = pymavryk.using('atlasnet').contract('KT1Tj6xhgkMi7oFXGyZK8df5jGjNFB5Bsy1N')
        res = fa12.getBalance('mv1FVuPj34FvgBHnjyNMkmHe4S9Cmnw4aZMz', None).view()
        self.assertIsNotNone(res)

    def test_branch_offset_overflow(self):
        # bh = pymavryk.using('mainnet').shell.blocks[-1000000000].hash()
        bh = pymavryk.using('atlasnet').shell.blocks[-1000000000].hash()
        self.assertEqual("BLockGenesisGenesisGenesisGenesisGenesisd727aarXu1g", bh)
