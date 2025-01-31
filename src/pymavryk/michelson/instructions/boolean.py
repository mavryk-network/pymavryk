from typing import Callable
from typing import List
from typing import Tuple
from typing import Union
from typing import cast

from pymavryk.context.abstract import AbstractContext
from pymavryk.michelson.instructions.base import MichelsonInstruction
from pymavryk.michelson.instructions.base import dispatch_types
from pymavryk.michelson.instructions.base import format_stdout
from pymavryk.michelson.stack import MichelsonStack
from pymavryk.michelson.types import BoolType
from pymavryk.michelson.types import IntType
from pymavryk.michelson.types import NatType


def execute_boolean_add(prim: str, stack: MichelsonStack, stdout: List[str], add: Callable):
    a, b = cast(Tuple[Union[BoolType, NatType], ...], stack.pop2())
    res_type, convert = dispatch_types(
        type(a),
        type(b),
        mapping={
            (BoolType, BoolType): (BoolType, bool),
            (NatType, NatType): (NatType, int),
        },
    )
    val = add((convert(a), convert(b)))
    res = res_type.from_value(val)
    stack.push(res)
    stdout.append(format_stdout(prim, [a, b], [res]))


class OrInstruction(MichelsonInstruction, prim='OR'):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        execute_boolean_add(cls.prim, stack, stdout, lambda x: x[0] | x[1])  # type: ignore
        return cls(stack_items_added=1)


class XorInstruction(MichelsonInstruction, prim='XOR'):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        execute_boolean_add(cls.prim, stack, stdout, lambda x: x[0] ^ x[1])  # type: ignore
        return cls(stack_items_added=1)


class AndInstruction(MichelsonInstruction, prim='AND'):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        a, b = cast(Tuple[Union[BoolType, NatType, IntType], ...], stack.pop2())
        res_type, convert = dispatch_types(
            type(a),
            type(b),
            mapping={
                (BoolType, BoolType): (BoolType, bool),
                (NatType, NatType): (NatType, int),
                (NatType, IntType): (NatType, int),
                (IntType, NatType): (NatType, int),
            },
        )
        res = res_type.from_value(convert(a) & convert(b))
        stack.push(res)
        stdout.append(format_stdout(cls.prim, [a, b], [res]))  # type: ignore
        return cls(stack_items_added=1)


class NotInstruction(MichelsonInstruction, prim='NOT'):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        a = cast(Union[IntType, NatType, BoolType], stack.pop1())
        res_type, convert = dispatch_types(
            type(a),
            mapping={
                (NatType,): (IntType, lambda x: ~int(x)),
                (IntType,): (IntType, lambda x: ~int(x)),
                (BoolType,): (BoolType, lambda x: not bool(x)),
            },
        )
        res = res_type.from_value(convert(a))
        stack.push(res)
        stdout.append(format_stdout(cls.prim, [a], [res]))  # type: ignore
        return cls(stack_items_added=1)
