from unittest import TestCase

from pymavryk import pymavryk


# TODO: Fix when Mavryk mainnet is deployed
class CallbackViewTestCase(TestCase):
    def test_balance_of(self):
        # mvn = pymavryk.using('mainnet').contract('KT1EmkMv4FRTCC4op5Xzf3fcHzwazFXXDHLC')
        mvn = pymavryk.using('atlasnet').contract('KT1EmkMv4FRTCC4op5Xzf3fcHzwazFXXDHLC')
        res = mvn.balance_of(
            requests=[
                {'owner': 'mv1SfxLHQ7KHoa5iNf7uNcCzAujcj8U5bYrV', 'token_id': 0},
                {'owner': 'mv1ExF49bRAGdDXP2a9NyCgTb9XYXg8nJYSC', 'token_id': 0},
                {'owner': 'mv1NsQzbvdMtyf7N1Y7ZM9nvmGnYmp3igYp9', 'token_id': 0},
            ],
            callback=None,
        ).callback_view()
        print(res)

    def test_initial_storage(self):
        # mvn = pymavryk.using('mainnet').contract('KT1EmkMv4FRTCC4op5Xzf3fcHzwazFXXDHLC')
        mvn = pymavryk.using('atlasnet').contract('KT1EmkMv4FRTCC4op5Xzf3fcHzwazFXXDHLC')
        storage = mvn.storage()
        storage['ledger'] = {'mv19MAVgCDwzuNMWprbHrUZhznoH8n9NWGWt': 100000000000000000}
        res = mvn.balance_of(
            requests=[
                {'owner': 'mv19MAVgCDwzuNMWprbHrUZhznoH8n9NWGWt', 'token_id': 0},
            ],
            callback=None,
        ).callback_view(storage=storage)
        self.assertEqual(100000000000000000, res[0]['balance'])

    def test_onchain_view(self):
        # mvn = pymavryk.using('mainnet').contract('KT1F6Amndd62P8yySM5NkyF4b1Kz27Ft4QeT')
        mvn = pymavryk.using('atlasnet').contract('KT1EmkMv4FRTCC4op5Xzf3fcHzwazFXXDHLC')
        res = mvn.total_supply(0).run_view()
        print(res)
