import pytest
from parameterized import parameterized  # type: ignore

from pymavryk.crypto.encoding import base58_decode
from pymavryk.crypto.encoding import base58_encode
from pymavryk.crypto.encoding import is_bh
from pymavryk.crypto.encoding import is_l2_pkh
from pymavryk.crypto.encoding import is_pkh
from pymavryk.crypto.encoding import is_sig
from pymavryk.crypto.encoding import scrub_input


class TestEncoding:
    @pytest.mark.parametrize(
        ('base58', 'prefix'),
        [
            ('NetXdQprcVkpaWU', 'Net'),
            ('BKjWN8ALguCJ3oAjzMjZCNcFfUf1p9BfVAwYiVHs1QW3yMB9RNb', 'B'),
            ('oop1fbAVi2ZwEt3vpu4uKpYGbbxumyMBSWwWf9qbByeM4JYAu92', 'o'),
            ('LLoabcny4pVg1k6x3AktnNhwe1KSVBZh5Di45JeZPhUCmCu5Xj6ND', 'LLo'),
            ('PtCJ7pwoxe8JasnHY8YonnLYjcVHmhiARPJvqcC6VfHT5s8k8sY', 'P'),
            ('CoUeRwFZbV7NaAYRTz6n4ZLUkwiWcm7oKYdKCGcsEYHgVxSQxa4h', 'Co'),
            ('mv1ShDp4Q4aFEcFwyhPkr7YZ8nd6cNbxntvN', 'mv1'),
            ('mv2LFe6Haxk32BC5xgEmK6QGocGqXdAtJDHT', 'mv2'),
            ('mv3P3rSvb1Ky736e7sLwgupCSLbiKGgm4EDJ', 'mv3'),
            ('mv4SpAYtPZMDa55PczcxEnMnmu9fURPbnkiA', 'mv4'),
            ('txr1YNMEtkj5Vkqsbdmt7xaxBTMRZjzS96UAi', 'txr1'),
            ('edpku976gpuAD2bXyx1XGraeKuCo1gUZ3LAJcHM12W1ecxZwoiu22R', 'edpk'),
            ('sppk7aMNM3xh14haqEyaxNjSt7hXanCDyoWtRcxF8wbtya859ak6yZT', 'sppk'),
            ('p2pk679D18uQNkdjpRxuBXL5CqcDKTKzsiXVtc9oCUT6xb82zQmgUks', 'p2pk'),
            ('edsk3nM41ygNfSxVU4w1uAW3G9EnTQEB5rjojeZedLTGmiGRcierVv', 'edsk'),
            ('spsk1zkqrmst1yg2c4xi3crWcZPqgdc9KtPtb9SAZWYHAdiQzdHy7j', 'spsk'),
            ('p2sk3PM77YMR99AvD3fSSxeLChMdiQ6kkEzqoPuSwQqhPsh29irGLC', 'p2sk'),
            ('edesk1zxaPJkhNGSzgZDDSphvPzSNrnbmqes8xzUrw1wdFxdRT7ePiQz8D2Q18fMjn6fC9ZRS2rUbg8d8snxxznE', 'edesk'),
            ('spesk21cruoqtYmxfq5fpkXiZZRLRw4vh7VFJauGCAgHxZf3q6Q5LTv9m9dnMxyVjna6RzWQL45q4ppGLh97xZpV', 'spesk'),
            ('p2esk1rqdHRPz4xQh8uP8JaWSVnGFTKxkh2utdjK5CPDTXAzzh5sXnnobLkGrXEZzGhCKFDSjv8Ggrjt7PnobRzs', 'p2esk'),
            (
                'edsigtzLBGCyadERX1QsYHKpwnxSxEYQeGLnJGsSkHEsyY8vB5GcNdnvzUZDdFevJK7YZQ2ujwVjvQZn62ahCEcy74AwtbA8HuN',
                'edsig',
            ),
            (
                'spsig1RriZtYADyRhyNoQMa6AiPuJJ7AUDcrxWZfgqexzgANqMv4nXs6qsXDoXcoChBgmCcn2t7Y3EkJaVRuAmNh2cDDxWTdmsz',
                'spsig',
            ),
            ('sigUdRdXYCXW14xqT8mFTMkX4wSmDMBmcW1Vuz1vanGWqYTmuBodueUHGPUsbxgn73AroNwpEBHwPdhXUswzmvCzquiqtcHC', 'sig'),
            ('sr1JZsZT5u27MUQXeTh1aHqZBo8NvyxRKnyv', 'sr1'),
            ('src13FVgJq88nGcd3xmjtPr4j3wq9VJGkGZ3LaVKZ3PUT8dKbByviq', 'src1'),
            ('srs1257rrkFCsjuDS5enYG37uSas1J25daCaMQ2y5gPwwtoy8FqvDP', 'srs1'),
            ('BLsk1ijYmTDL6hfUvrFCqgwbetg6FTpHLbzPDKLAfP9tB9Cej8dME5', 'BLsk'),
            ('BLpk1q8T9TqRSNTacJU1WvTVtj62LZ8WZtGzZ3tQoQANzoXHwAPtxpJCY79TfoNu2m9N6RbFfh7s', 'BLpk'),
            (
                'BLsigB2azuvvpWDifK3xCMGDXUcF17V1R7NGfKQsUVrzm7718uvbjtrXpS3KMq5CSJiAWAS9Rjj79Zak3TskGGwDGfHnm52rvdb9rpJxtyXK39FNadwGX4EGtqXVDge9eDRjSm8bVNxJE6',
                'BLsig',
            ),
            ('BLesk1a3e2vNGbbPV5rFRHZZCHvZEvvtGP5Puer4yRfRVLR8E1xVyk5owiUeudZcaa31mGDmvbr9LH6ZPTUdi66z', 'BLesk'),
        ],
    )
    def test_b58_decode_encode(self, base58: str, prefix: str):
        expected: bytes = base58.encode()
        decoded: bytes = base58_decode(expected)
        print(decoded.hex())
        re_encoded = base58_encode(decoded, prefix.encode())
        assert re_encoded == expected

    @pytest.mark.parametrize(
        ('input_data', 'expected'),
        [
            ('test', b'test'),
            (b'test', b'test'),
            ('0x74657374', b'test'),
            ('74657374', b'test'),
        ],
    )
    def test_scrub_input(self, input_data, expected):
        assert scrub_input(input_data) == expected

    @pytest.mark.parametrize(
        ('value', 'expected'),
        [
            ('mv1ShDp4Q4aFEcFwyhPkr7YZ8nd6cNbxntvN', True),
            ('mv2LFe6Haxk32BC5xgEmK6QGocGqXdAtJDHT', True),
            ('mv3P3rSvb1Ky736e7sLwgupCSLbiKGgm4EDJ', True),
            ('mv4SpAYtPZMDa55PczcxEnMnmu9fURPbnkiA', True),
            ('txr1YNMEtkj5Vkqsbdmt7xaxBTMRZjzS96UAi', False),
            ('KT1ExvG3EjTrvDcAU7EqLNb77agPa5u6KvnY', False),
            ('qwerty', False),
            ('mv1eKkWU5hGtfLUiq', False),
        ],
    )
    def test_is_pkh(self, value, expected):
        assert is_pkh(value) == expected

    @pytest.mark.parametrize(
        ('value', 'expected'),
        [
            ('mv1ShDp4Q4aFEcFwyhPkr7YZ8nd6cNbxntvN', False),
            ('mv2LFe6Haxk32BC5xgEmK6QGocGqXdAtJDHT', False),
            ('mv3P3rSvb1Ky736e7sLwgupCSLbiKGgm4EDJ', False),
            ('txr1YNMEtkj5Vkqsbdmt7xaxBTMRZjzS96UAi', True),
            ('KT1ExvG3EjTrvDcAU7EqLNb77agPa5u6KvnY', False),
            ('qwerty', False),
            ('mv1eKkWU5hGtfLUiq', False),
        ],
    )
    def test_is_l2_pkh(self, value, expected):
        assert is_l2_pkh(value) == expected

    @pytest.mark.parametrize(
        ('value', 'expected'),
        [
            (
                'edsigtzLBGCyadERX1QsYHKpwnxSxEYQeGLnJGsSkHEsyY8vB5GcNdnvzUZDdFevJK7YZQ2ujwVjvQZn62ahCEcy74AwtbA8HuN',
                True,
            ),
            (
                'spsig1RriZtYADyRhyNoQMa6AiPuJJ7AUDcrxWZfgqexzgANqMv4nXs6qsXDoXcoChBgmCcn2t7Y3EkJaVRuAmNh2cDDxWTdmsz',
                True,
            ),
            (
                'BLsigB2azuvvpWDifK3xCMGDXUcF17V1R7NGfKQsUVrzm7718uvbjtrXpS3KMq5CSJiAWAS9Rjj79Zak3TskGGwDGfHnm52rvdb9rpJxtyXK39FNadwGX4EGtqXVDge9eDRjSm8bVNxJE6',
                True,
            ),
            ('BLsigB2azuvvpWDifK3xCMGDXUcF17V1R7NGfKQsUVrzm7718uvbjtrXpS3KMq5CSJiAWAS9Rjj79Zak3TskGGwDGfHnm52r', False),
            ('sigUdRdXYCXW14xqT8mFTMkX4wSmDMBmcW1Vuz1vanGWqYTmuBodueUHGPUsbxgn73AroNwpEBHwPdhXUswzmvCzquiqtcHC', True),
            ('qwerty', False),
            ('sigUdRdXYCXW14xqT8mFTMkX4wSmDMBmcW1Vuz1vanGWqYT', False),
        ],
    )
    def test_is_sig(self, value, expected):
        assert is_sig(value) == expected

    @pytest.mark.parametrize(
        ('value', 'expected'),
        [
            ('BLrbVv8rUfkpDZZ6efByhgjyDgPUFeKAfTMq8mWPmjXb9c5m8LJ', True),
            ('qwerty', False),
        ],
    )
    def test_is_bh(self, value, expected):
        assert is_bh(value) == expected
