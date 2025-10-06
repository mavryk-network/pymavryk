from unittest import TestCase

import pytest

from pymavryk import pymavryk


# TODO: Fix when Mavryk mainnet is deployed
class TestMetadata(TestCase):
    def test_usds_all_tokens_view(self):
        ...
        # usds = pymavryk.using('mainnet').contract('KT1REEb5VxWRjcHm5GzDMwErMmNFftsE5Gpf')
        # res = usds.metadata.allTokens().storage_view()
        # self.assertEqual([0], res)

    @pytest.mark.skip
    def test_domains(self):
        ...
        # td = pymavryk.using('mainnet').contract('KT1GBZmSxmnKJXGMdMLbugPfLyUPmuLSMwKS')
        # res = td.metadata.resolveAddress('mv2SWyttJCrigv3XdHaS8XJF33AMoLGYLttC').storage_view()
        # self.assertEqual('mv2SWyttJCrigv3XdHaS8XJF33AMoLGYLttC', res['address'])
