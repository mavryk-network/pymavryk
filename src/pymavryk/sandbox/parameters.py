import json
from pathlib import Path
from typing import Any
from typing import Dict

from pymavryk.crypto.key import Key

ATLAS = 'PtAtLasomUEW99aVhVTrqjCHjJSpFUa8uHNEAEamx9v2SNeTaNp'
BOREAS = 'Pt8h9rz3r9F3Yx3wzJqF42sxsyVoo6kL4FBoJSWRzKmDvjXjHwV'
C_UPDATE = 'Pt8h9rz3r9F3Yx3wzJqF42sxsyVoo6kL4FBoJSWRzKmDvjXjHwV'
LATEST = BOREAS

protocol_hashes = {
    'atlas': ATLAS,
    'boreas': BOREAS,
    'c_update': C_UPDATE,
}

protocol_version = {
    ATLAS: 1,
    BOREAS: 2,
    C_UPDATE: 3,
}


sandbox_commitment = {
    "mnemonic": [
        "arctic",
        "blame",
        "brush",
        "economy",
        "solar",
        "swallow",
        "canvas",
        "live",
        "vote",
        "two",
        "post",
        "neutral",
        "spare",
        "split",
        "fall",
    ],
    "activation_code": "7375ef222cc038001b6c8fb768246c86e994745b",
    "amount": "38323962971",
    "pkh": "mv1JVZzbrGpKfripWo2GiWZ7wkzoeKHna498",
    "password": "ZuPOpZgMNM",
    "email": "nbhcylbg.xllfjgrk@tezos.example.org",
}

sandbox_addresses = {
    'activator': 'mv1FeNQ3gSZoEFp1mr6VTLnMqV5tuNwHTgw5',
    'bootstrap5': 'mv1S14SxfuavHMGDXxZJoBERZafLTyX3Z6Dx',
    'bootstrap4': 'mv1PVMnW8iyYxCoqLfPAha8EAPRxjTx7wqbn',
    'bootstrap3': 'mv1TxMEnmav51G1Hwcib1rBnBeniDMgG8nkJ',
    'bootstrap2': 'mv1V73YiKvinVumxwvYWjCZBoT44wqBNhta7',
    'bootstrap1': 'mv18Cw7psUrAAPBpXYd9CtCpHg9EgjHP9KTe',
    # FIXME: Temporary, see test_sandbox.py
    'alice': 'mv1E2Y8khTrfaRUeErWUBfg6G7zNMKnM4JJL',
}

# NOTE: Run `make sandbox-params` to update this file
sandbox_params = json.loads(
    Path(__file__).parent.joinpath('003-PtCUpdate-parameters', 'test-parameters.json').read_text()
)


def get_protocol_parameters(protocol_hash: str) -> Dict[str, Any]:
    return {**sandbox_params}
