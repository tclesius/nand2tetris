import argparse
import re
from pathlib import Path

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
    "add": C_ARITHMETIC,
    "sub": C_ARITHMETIC,
    "neg": C_ARITHMETIC,
    "eq": C_ARITHMETIC,
    "gt": C_ARITHMETIC,
    "lt": C_ARITHMETIC,
    "and": C_ARITHMETIC,
    "or": C_ARITHMETIC,
    "not": C_ARITHMETIC,

    "push": C_PUSH,
    "pop": C_POP,
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


class Parser:
    def __init__(self, inputFile):
        self.File = open(inputFile, "r")
        self.inputFile = self.File.readlines()
        self.File.close()
        self.inputFilePosition = 0
        self.currentCommand = ""

    def hasMoreCommands(self):
        return self.inputFilePosition < len(self.inputFile)

    def advance(self):
        self.currentCommand = re.sub("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)", "",
                                     self.inputFile[self.inputFilePosition]).strip()
        self.inputFilePosition += 1

    def commandType(self):
        if self.currentCommand:
            return COMMAND_TYPE[self.currentCommand.split()[0]]

    def arg1(self):
        if self.commandType() == C_ARITHMETIC:
            return self.currentCommand
        else:
            return self.currentCommand.split()[1]

    def arg2(self):
        if self.commandType() in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            return int(self.currentCommand.split()[2])


class CodeWriter:

    def __init__(self, outputFile):
        self.outputFile = open(Path(outputFile).with_suffix('.asm'), 'w')
        self.EQ_ID = 0
        self.GT_ID = 0
        self.LT_ID = 0

    def A_COMMAND(self, address):
        self.outputFile.write("@" + str(address) + "\n")

    def C_COMMAND(self, dest=None, comp=None, jump=None):
        if jump:
            self.outputFile.write(comp + ";" + jump + "\n")
        else:
            self.outputFile.write(dest + "=" + comp + "\n")

    def L_COMMAND(self, xxx):
        self.outputFile.write("(" + xxx + ")" + "\n")

    def POP(self, dest):
        # pop value from stack in d or just point to it
        self.A_COMMAND("SP")
        self.C_COMMAND("AM", "M-1")
        if dest == "D":
            self.C_COMMAND("D", "M")

    def PUSH(self):
        # push value from d in stack
        self.A_COMMAND("SP")
        self.C_COMMAND("A", "M")
        self.C_COMMAND("M", "D")
        self.A_COMMAND("SP")
        self.C_COMMAND("M", "M+1")

    def setFileName(self, fileName):
        ...

    def writeArithmetic(self, command):
        if command == A_ADD:
            self.POP("D")
            self.POP("A")
            self.C_COMMAND("D", "M+D")
            self.PUSH()

        if command == A_SUB:
            self.POP("D")
            self.POP("A")
            self.C_COMMAND("D", "M-D")
            self.PUSH()

        if command == A_AND:
            self.POP("D")
            self.POP("A")
            self.C_COMMAND("D", "M&D")
            self.PUSH()

        if command == A_OR:
            self.POP("D")
            self.POP("A")
            self.C_COMMAND("D", "M|D")
            self.PUSH()

        if command == A_NOT:
            self.POP("D")
            self.POP("A")
            self.C_COMMAND("D", "-M")
            self.C_COMMAND("D", "D-1")
            self.PUSH()

        if command == A_NEG:
            self.POP("A")
            self.C_COMMAND("D", "!M")
            self.C_COMMAND("D", "D+1")
            self.PUSH()

        if command == A_EQ:
            self.POP("D")
            self.POP("A")
            self.C_COMMAND("D", "M-D")
            self.A_COMMAND(f"EQ{self.EQ_ID}")
            self.C_COMMAND(comp="D", jump="JEQ")
            self.C_COMMAND("D", "0")
            self.A_COMMAND(f"NEQ{self.EQ_ID}")
            self.C_COMMAND(comp="0", jump="JMP")
            self.L_COMMAND(f"EQ{self.EQ_ID}")
            self.C_COMMAND("D", "-1")
            self.L_COMMAND(f"NEQ{self.EQ_ID}")
            self.PUSH()

            self.EQ_ID += 1

        if command == A_LT:
            self.POP("D")
            self.POP("A")
            self.C_COMMAND("D", "M-D")
            self.A_COMMAND(f"LT{self.LT_ID}")
            self.C_COMMAND(comp="D", jump="JLT")
            self.C_COMMAND("D", "0")
            self.A_COMMAND(f"NLT{self.LT_ID}")
            self.C_COMMAND(comp="0", jump="JMP")
            self.L_COMMAND(f"LT{self.LT_ID}")
            self.C_COMMAND("D", "-1")
            self.L_COMMAND(f"NLT{self.LT_ID}")
            self.PUSH()

            self.LT_ID += 1

        if command == A_GT:
            self.POP("D")
            self.POP("A")
            self.C_COMMAND("D", "M-D")
            self.A_COMMAND(f"GT{self.GT_ID}")
            self.C_COMMAND(comp="D", jump="JGT")
            self.C_COMMAND("D", "0")
            self.A_COMMAND(f"NGT{self.GT_ID}")
            self.C_COMMAND(comp="0", jump="JMP")
            self.L_COMMAND(f"GT{self.GT_ID}")
            self.C_COMMAND("D", "-1")
            self.L_COMMAND(f"NGT{self.GT_ID}")
            self.PUSH()

            self.GT_ID += 1

    def WritePushPop(self, command, segment, index):


            if SEGMENT_TYPE[segment] == S_CONSTANT:
                if command == C_PUSH:
                    self.A_COMMAND(index)
                    self.C_COMMAND("D", "A")
                    self.PUSH()

            if SEGMENT_TYPE[segment] in [S_LOCAL, S_ARGUMENT, S_THIS, S_THAT]:
                if command == C_PUSH:
                    self.A_COMMAND(index)
                    self.C_COMMAND("D", "A")
                    self.A_COMMAND(SEGMENT_POINTER[segment])  # pointer to where base address is saved
                    self.C_COMMAND("A", "D+M")
                    self.C_COMMAND("D", "M")
                    self.PUSH()
                if command == C_POP:
                    self.A_COMMAND(index)
                    self.C_COMMAND("D", "A")
                    self.outputFile.write(f"@{SEGMENT_POINTER[segment]}\n")
                    self.C_COMMAND("D", "D+M")
                    self.A_COMMAND("R13")  # general purpose register
                    self.C_COMMAND("M", "D")
                    self.POP("A")
                    self.C_COMMAND("D", "M")
                    self.A_COMMAND("R13")  # general purpose register
                    self.C_COMMAND("A", "M")
                    self.C_COMMAND("M", "D")

            if SEGMENT_TYPE[segment] == S_POINTER:
                if command == C_PUSH:
                    self.A_COMMAND(3 + index)
                    self.C_COMMAND("D", "M")
                    self.PUSH()

                if command == C_POP:
                    self.POP("D")
                    self.A_COMMAND(3 + index)
                    self.C_COMMAND("M", "D")

            if SEGMENT_TYPE[segment] == S_TEMP:
                if command == C_PUSH:
                    self.A_COMMAND(5 + index)
                    self.C_COMMAND("D", "M")
                    self.PUSH()
                if command == C_POP:
                    self.POP("D")
                    self.A_COMMAND(5 + index)
                    self.C_COMMAND("M", "D")

            if SEGMENT_TYPE[segment] == S_STATIC:
                if command == C_PUSH:
                    self.A_COMMAND(16 + index)
                    self.C_COMMAND("D", "M")
                    self.PUSH()
                if command == C_POP:
                    self.POP("D")
                    self.A_COMMAND(16 + index)
                    self.C_COMMAND("M", "D")

    def Close(self):
        ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='.vm translator')
    parser.add_argument('vmFile', type=str,
                        help='.vm input file or directory')
    parser.add_argument('--o', type=str,
                        help='output filename')
    args = parser.parse_args()
    parser = Parser(args.vmFile)

    # Output file creation
    if args.o:
        outputFile = Path(args.o).with_suffix('.asm')
    else:
        outputFile = Path(args.vmFile).with_suffix('.asm')

    codeWriter = CodeWriter(outputFile)

    while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() in [C_PUSH, C_POP]:
            codeWriter.WritePushPop(parser.commandType(), parser.arg1(), parser.arg2())

        if parser.commandType() == C_ARITHMETIC:
            codeWriter.writeArithmetic(parser.arg1())
