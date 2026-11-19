import dis

from bytecode import Bytecode

from xdsl.dialects.builtin import (
    FunctionType,
)
from xdsl.dialects.py import (
    PyConstOp,
    PyFuncOp,
    PyObjectType,
    PyReturnOp,
)
from xdsl.ir import (
    Block,
    Region,
)


def foo():
    return 1


if __name__ == "__main__":
    dis.dis(foo)
    const = PyConstOp.from_value(1)
    py_prg = PyFuncOp(
        "foo",
        FunctionType.from_lists([PyObjectType(), PyObjectType()], [PyObjectType()]),
        Region(Block([const, PyReturnOp(const.results[0])])),
    )
    print(py_prg)

    prg = [instr for instr in py_prg.bytecode()]
    print(prg)

    dis.dis(Bytecode(prg).to_code())
    print(eval(Bytecode(prg).to_code()))
