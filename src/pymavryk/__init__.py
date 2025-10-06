"""
Welcome to PyMavryk!

To start playing with the Mavryk blockchain you need to get a PyMavrykClient instance.
Just type:

>>> from pymavryk import pymavryk
>>> pymavryk

And follow the interactive documentation.
"""

import importlib.metadata

from pymavryk.client import PyMavrykClient
from pymavryk.contract.interface import Contract
from pymavryk.contract.interface import ContractInterface
from pymavryk.crypto.key import Key
from pymavryk.logging import logger
from pymavryk.michelson.forge import forge_micheline
from pymavryk.michelson.forge import unforge_micheline
from pymavryk.michelson.format import micheline_to_michelson
from pymavryk.michelson.micheline import MichelsonRuntimeError
from pymavryk.michelson.parse import michelson_to_micheline
from pymavryk.michelson.types.base import MichelsonType
from pymavryk.michelson.types.base import Undefined
from pymavryk.michelson.types.core import Unit

__version__ = importlib.metadata.version('pymavryk')

pymavryk = PyMavrykClient()
