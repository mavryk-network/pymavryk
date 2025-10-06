from unittest import TestCase
from unittest import skip

from pymavryk import pymavryk


class TestRegression(TestCase):
    # def test_tzbtc_get_balance_view(self):
    #     tzbtc = pymavryk.using('mainnet').contract('KT1PWx2mnDueood7fEmfbBDKx1D9BAnnXitn')
    #     res = tzbtc.getBalance(owner='mv1SoL5knJPwP6nCgBSnVSm6a6rduH9psPaT', contract_1=None).view()
    #     self.assertIsNotNone(res)

    # TODO: Fix when Mavryk mainnet is deployed
    def test_kusd_get_balance_view(self):
        ...
        # kusd = pymavryk.using('mainnet').contract('KT1K9gCRgaLRFKTErYt1wVxA3Frb9FjasjTV')
        # res = kusd.getBalance('KT1SorR4UFBkUJeYVbtXZBNivUV1cQM6AqRR', None).view()
        # self.assertIsNotNone(res)

    def test_branch_offset_overflow(self):
        ...
        # bh = pymavryk.using('mainnet').shell.blocks[-1000000000].hash()
        # self.assertEqual("BLockGenesisGenesisGenesisGenesisGenesisf79b5d1CoW2", bh)
