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
