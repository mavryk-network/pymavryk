import re
from contextlib import suppress
from typing import Dict
from typing import List
from typing import Type
from typing import cast

import strict_rfc3339  # type: ignore

from pymavryk.context.abstract import AbstractContext
from pymavryk.context.mixin import nodes
from pymavryk.michelson.instructions.base import MichelsonInstruction
from pymavryk.michelson.instructions.base import format_stdout
from pymavryk.michelson.micheline import MichelineLiteral
from pymavryk.michelson.micheline import MichelsonRuntimeError
from pymavryk.michelson.sections import ParameterSection
from pymavryk.michelson.sections import StorageSection
from pymavryk.michelson.stack import MichelsonStack
from pymavryk.michelson.types import ListType
from pymavryk.michelson.types import OperationType
from pymavryk.michelson.types import PairType
from pymavryk.michelson.types.base import MichelsonType
from pymavryk.michelson.types.core import FalseLiteral
from pymavryk.michelson.types.core import TrueLiteral
from pymavryk.rpc.node import RpcMultiNode
from pymavryk.rpc.node import RpcNode
from pymavryk.rpc.shell import ShellQuery


class DumpAllInstruction(MichelsonInstruction, prim='DUMP'):
    def __init__(self, items: List[MichelsonType]):
        super().__init__(stack_items_added=len(items))
        self.items = items

    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        items = stack.items[:]
        stdout.append(f'DUMP => {items}')
        return cls(items)


class DumpInstruction(MichelsonInstruction, prim='DUMP', args_len=1):
    def __init__(self, items: List[MichelsonType]):
        super().__init__(stack_items_added=len(items))
        self.items = items

    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        literal: Type[MichelineLiteral] = cls.args[0]  # type: ignore
        count = cast(int, literal.literal)
        count = min(count, len(stack))
        items = stack.items[:count]
        stdout.append(f'DUMP => {items}')
        return cls(items)


class PrintInstruction(MichelsonInstruction, prim='PRINT', args_len=1):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        literal: Type[MichelineLiteral] = cls.args[0]  # type: ignore

        template = literal.get_string()

        def format_stack_item(match):
            i = int(match.groups()[0])
            assert i < len(stack), f'requested {i}th element, got only {len(stack)} items'
            return repr(stack.items[i])

        message = re.sub(r'{(\d+)}', format_stack_item, template)
        stdout.append(message)
        return cls()


class DebugInstruction(MichelsonInstruction, prim='DEBUG', args_len=1):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        literal = cls.args[0]
        if issubclass(literal, (TrueLiteral, FalseLiteral)):
            debug = literal.literal
        else:
            debug = bool(literal.get_int())  # type: ignore

        context.debug = debug  # type: ignore
        return cls()


class DropAllInstruction(MichelsonInstruction, prim='DROP_ALL'):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        stack.items = []
        return cls()


class BeginInstruction(MichelsonInstruction, prim='BEGIN', args_len=2):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        # FIXME: MichelsonProgram copypaste
        parameter_literal, storage_literal = cls.args  # type: ignore

        parameter_type_expr = context.get_parameter_expr()
        storage_type_expr = context.get_storage_expr()
        if parameter_type_expr is None:
            raise Exception('parameter type is not initialized')
        if storage_type_expr is None:
            raise Exception('storage type is not initialized')

        parameter_type = ParameterSection.match(parameter_type_expr)
        storage_type = StorageSection.match(storage_type_expr)
        parameter = parameter_type.from_micheline_value(parameter_literal.as_micheline_expr())
        storage = storage_type.from_micheline_value(storage_literal.as_micheline_expr())

        parameter.attach_context(context)
        storage.attach_context(context)
        res = PairType.from_comb([parameter.item, storage.item])
        stack.items = []
        stack.push(res)
        stdout.append(format_stdout(f'BEGIN %default', [], [res]))
        return cls(stack_items_added=1)


class CommitInstruction(MichelsonInstruction, prim='COMMIT'):
    def __init__(self, lazy_diff: List[Dict[str, str]], result, stack_items_added: int = 0) -> None:
        super().__init__(stack_items_added)
        self.lazy_diff = lazy_diff
        self.result = result

    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        # FIXME: MichelsonProgram copypaste
        debug, context.debug = context.debug, False  # type: ignore

        res = cast(PairType, stack.pop1())
        if len(stack):
            raise Exception(f'Stack is not empty: {stack}')
        res.assert_type_equal(
            PairType.create_type(
                args=[
                    ListType.create_type(args=[OperationType]),
                    StorageSection.match(context.get_storage_expr()).args[0],
                ],
            ),
            message='list of operations + resulting storage',
        )
        operations = ListType(items=list(res.items[0]))  # type: ignore
        lazy_diff = []  # type: ignore
        storage = res.items[1].aggregate_lazy_diff(lazy_diff)
        stdout.append(format_stdout(f'END %default', [res], []))

        result = PairType.from_comb([operations, storage])
        context.debug = debug  # type: ignore
        return cls(lazy_diff=lazy_diff, result=result)


class RunInstruction(MichelsonInstruction, prim='RUN', args_len=3):
    def __init__(self, lazy_diff: List[Dict[str, str]], result, stack_items_added: int = 0) -> None:
        super().__init__(stack_items_added)
        self.lazy_diff = lazy_diff
        self.result = result

    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        from pymavryk.michelson.program import MichelsonProgram

        stack.clear()
        entrypoint, parameter_literal, storage_literal = cls.args  # type: ignore
        entrypoint_str = entrypoint.get_string()  # type: ignore

        parameter = parameter_literal.as_micheline_expr()
        storage = storage_literal.as_micheline_expr()

        program = MichelsonProgram.load(context, with_code=True).instantiate(entrypoint_str, parameter, storage)  # type: ignore
        program.begin(stack, stdout, context)
        program.execute(stack, stdout, context)  # type: ignore
        operations, storage, lazy_diff, res = program.end(stack, stdout)

        return cls(lazy_diff=lazy_diff, result=res)


class PatchInstruction(MichelsonInstruction, prim='PATCH', args_len=1):
    allowed_primitives = ['AMOUNT', 'BALANCE', 'CHAIN_ID', 'SENDER', 'SOURCE', 'NOW']

    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        res_type: MichelsonType
        res_type = cls.args[0]  # type: ignore

        if res_type.prim == 'AMOUNT':
            context.amount = None  # type: ignore
        elif res_type.prim == 'BALANCE':
            context.balance = None  # type: ignore
        elif res_type.prim == 'CHAIN_ID':
            context.chain_id = None  # type: ignore
        elif res_type.prim == 'SENDER':
            context.sender = None  # type: ignore
        elif res_type.prim == 'SOURCE':
            context.source = None  # type: ignore
        elif res_type.prim == 'NOW':
            context.now = None  # type: ignore
        else:
            raise ValueError(f'Expected one of {cls.allowed_primitives}, got {res_type.prim}')
        return cls()


class PatchValueInstruction(MichelsonInstruction, prim='PATCH', args_len=2):
    allowed_primitives = ['AMOUNT', 'BALANCE', 'CHAIN_ID', 'SENDER', 'SOURCE', 'NOW']

    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        res_type: MichelsonType
        literal: Type[MichelineLiteral]
        res_type, literal = cls.args  # type: ignore

        if res_type.prim == 'AMOUNT':
            context.amount = literal.get_int()  # type: ignore
        elif res_type.prim == 'BALANCE':
            context.balance = literal.get_int()  # type: ignore
        elif res_type.prim == 'CHAIN_ID':
            context.chain_id = literal.get_string()  # type: ignore
        elif res_type.prim == 'SENDER':
            context.sender = literal.get_string()  # type: ignore
        elif res_type.prim == 'SOURCE':
            context.source = literal.get_string()  # type: ignore
        elif res_type.prim == 'NOW':
            try:
                context.now = literal.get_int()  # type: ignore
            # FIXME: Why does TypeError appear to be wrapped?
            except (TypeError, MichelsonRuntimeError):
                context.now = int(strict_rfc3339.rfc3339_to_timestamp(literal.get_string()))  # type: ignore
        else:
            raise ValueError(f'Expected one of {cls.allowed_primitives}, got {res_type.prim}')
        return cls()


class ResetInstruction(MichelsonInstruction, prim='RESET'):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        context.shell = None  # type: ignore
        context.network = None  # type: ignore
        context.chain_id = None  # type: ignore
        context.big_maps = {}  # type: ignore
        stack.items = []
        return cls()


class ResetValueInstruction(MichelsonInstruction, prim='RESET', args_len=1):
    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        literal: Type[MichelineLiteral]
        literal = cls.args[0]  # type: ignore

        shell = literal.get_string()
        if shell not in nodes:
            raise Exception(f'Expected one of {nodes}, got {shell}')

        if shell.endswith('.pool'):
            shell = shell.split('.')[0]
            assert shell in nodes, f'unknown network {shell}'
            context.shell = ShellQuery(RpcMultiNode(nodes[shell]))  # type: ignore
        elif shell in nodes:
            context.shell = ShellQuery(RpcNode(nodes[shell][0]))  # type: ignore
        else:
            context.shell = ShellQuery(RpcNode(shell))  # type: ignore

        context.network = shell  # type: ignore
        context.chain_id = context.shell.chains.main.chain_id()  # type: ignore
        context.big_maps = {}  # type: ignore
        stack.items = []
        return cls()


class BigMapDiffInstruction(MichelsonInstruction, prim='BIG_MAP_DIFF'):
    def __init__(self, lazy_diff: List[Dict[str, str]], stack_items_added: int = 0) -> None:
        super().__init__(stack_items_added)
        self.lazy_diff = lazy_diff

    @classmethod
    def execute(cls, stack: MichelsonStack, stdout: List[str], context: AbstractContext):
        lazy_diff = []  # type: ignore
        # FIXME: AssertionError instead of informational exception
        with suppress(AssertionError):
            stack.peek().aggregate_lazy_diff(lazy_diff)
        stdout.append(f'BIG_MAP_DIFF')
        return cls(lazy_diff=lazy_diff, stack_items_added=1)
