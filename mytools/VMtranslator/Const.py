# COMMANDS
C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9

# ROM SEGMENTS
S_ARGUMENT = 10
S_LOCAL = 11
S_STATIC = 12
S_CONSTANT = 13
S_THIS = 14
S_THAT = 15
S_POINTER = 16
S_TEMP = 17

# STACK ARITHMETIC
A_ADD = "add"
A_SUB = "sub"
A_NEG = "neg"
A_EQ = "eq"
A_GT = "gt"
A_LT = "lt"
A_AND = "and"
A_OR = "or"
A_NOT = "not"

COMMAND_TYPE = {
    #  Arithmetic and Logical Commands
    "add": C_ARITHMETIC,
    "sub": C_ARITHMETIC,
    "neg": C_ARITHMETIC,
    "eq": C_ARITHMETIC,
    "gt": C_ARITHMETIC,
    "lt": C_ARITHMETIC,
    "and": C_ARITHMETIC,
    "or": C_ARITHMETIC,
    "not": C_ARITHMETIC,
    # Stack Commands
    "push": C_PUSH,
    "pop": C_POP,
    # Program Flow Commands
    "label": C_LABEL,
    "goto": C_GOTO,
    "if-goto": C_IF,
    # Function Calling Commands
    "function": C_FUNCTION,
    "call": C_CALL,
    "return": C_RETURN,
}

SEGMENT_TYPE = {
    "argument": S_ARGUMENT,
    "local": S_LOCAL,
    "static": S_STATIC,
    "constant": S_CONSTANT,
    "this": S_THIS,
    "that": S_THAT,
    "pointer": S_POINTER,
    "temp": S_TEMP
}

SEGMENT_POINTER = {
    "argument": "ARG",
    "local": "LCL",
    "this": "THIS",
    "that": "THAT",
}

SEGMENT_BASE = {
    "pointer": 3,
    "temp": 5,
    "static": 16,
}


# Register
class R:
    R0 = SP = 0
    R1 = LCL = 1
    R2 = ARG = 2
    R3 = THIS = PTR = 3
    R4 = THAT = 4
    R5 = TEMP = 5
    R6 = 6
    R7 = 7
    R8 = 8
    R9 = 9
    R10 = 10
    R11 = 11
    R12 = 12
    R13 = FRAME = 13
    R14 = RET = 14
    R15 = COPY = 15


# Memory Segments
class S:
    ARGUMENT = "argument"
    LOCAL = "local"
    STATIC = "static"
    CONSTANT = "constant"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"
    REG = "reg"

    @staticmethod
    def R(segment):
        table = {
            S.ARGUMENT: R.ARG,
            S.LOCAL: R.LCL,
            S.THIS: R.THIS,
            S.THAT: R.THAT,
            S.POINTER: R.PTR,
            S.TEMP: R.TEMP,
            S.REG: R.R0
            # static?
        }
        return table[segment]
