import dis

from xdsl.dialects.builtin import FunctionType, NoneAttr
from xdsl.dialects.py import (
    Operator,
    PyBinOp,
    PyConstOp,
    PyFuncOp,
)
from xdsl.ir import Block, Region

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
    prg = py_prg.bytecode()
    print("---")
    print(dis.dis(prg))
