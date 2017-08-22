from enum import Enum, unique


@unique
class Prog(Enum):
    INFO = 0
    TESTDATA = 1
    TESTINT = 2
    ELASTICINT = 3
    FINALGRAPH = 4

    @staticmethod
    def from_string(val):
        if val == "INFO":
            return Prog.INFO
        if val == "DATA":
            return Prog.TESTDATA
        if val == "TEST":
            return Prog.TESTINT
        if val == "ELASTIC":
            return Prog.ELASTICINT
        if val == "FINAL":
            return Prog.FINALGRAPH
