from bytecode import BinaryOp, Bytecode, Instr

from xdsl.dialects.builtin import FunctionType, NoneAttr
from xdsl.dialects.py import (
    Operator,
    PyBinOp,
    PyConstOp,
    PyFuncOp,
)
from xdsl.ir import Block, Region, SSAValue
from xdsl.irdl import Operand

BinaryOp_Mapping = {
    Operator.ADD: BinaryOp.ADD,
    Operator.SUB: BinaryOp.SUBTRACT,
    Operator.MULT: BinaryOp.MULTIPLY,
    Operator.MAT_MULT: BinaryOp.MATRIX_MULTIPLY,
    Operator.DIV: BinaryOp.TRUE_DIVIDE,
    Operator.MOD: BinaryOp.REMAINDER,
    Operator.POW: BinaryOp.POWER,
    Operator.L_SHIFT: BinaryOp.LSHIFT,
    Operator.R_SHIFT: BinaryOp.RSHIFT,
    Operator.BIT_OR: BinaryOp.OR,
    Operator.BIT_XOR: BinaryOp.XOR,
    Operator.BIT_AND: BinaryOp.AND,
    Operator.FLOOR_DIV: BinaryOp.FLOOR_DIVIDE,
}


def expect_name_hint(ssa: SSAValue | Block) -> str:
    assert ssa.name_hint is not None
    return ssa.name_hint


def gen_const(op: PyConstOp):
    return


def gen_binop_operand(ope: Operand):
    owner = ope.owner
    if isinstance(owner, PyConstOp):
        return [Instr("LOAD_CONST", owner.value)]
    elif owner.name_hint:
        return [Instr("LOAD_FAST", owner.name_hint)]
    else:
        raise NotImplementedError("")


def gen_binOp(op: PyBinOp) -> list[Instr]:

    gen_lhs = gen_binop_operand(op.lhs)
    gen_rhs = gen_binop_operand(op.rhs)

    return (
        gen_lhs
        + gen_rhs
        + [
            Instr("BINARY_OP", BinaryOp_Mapping[op.op.data.value]),
        ]
    )


def print_pretty(lst):
    for l in lst:
        print(l)


def gen_funcOp(op: PyFuncOp):

    body = Bytecode(
        [Instr("RESUME", 0), *gen(op.body.first_block), Instr("RETURN_VALUE")]
    )
    print_pretty(body)

    func = Bytecode(
        [
            Instr("RESUME", 0),
            Instr("LOAD_CONST", body.to_code()),
            Instr("MAKE_FUNCTION", 0),
            Instr("STORE_NAME", op.func_name.data),
            Instr("RETURN_CONST", None),
        ]
    )

    return func


def gen(op):
    match op:
        case PyFuncOp():
            return gen_funcOp(op)

        case PyBinOp():
            return gen_binOp(op)

        case Block():
            lst = []
            for b in op.walk():
                if b == op:
                    continue

                lst += gen(b)

            return lst


if __name__ == "__main__":
    py_prg = PyFuncOp(
        "f",
        FunctionType.from_lists([], [NoneAttr()]),
        Region(
            Block(
                [
                    PyBinOp(
                        op=Operator.ADD,
                        lhs=PyConstOp.from_value(1).results[0],
                        rhs=PyConstOp.from_value(2).results[0],
                    )
                ]
            )
        ),
    )
    print(py_prg)

    # py_prg =
    prg = gen(py_prg)
    print("---")
    print_pretty(prg)
    print(eval(Bytecode(prg).to_code()))
