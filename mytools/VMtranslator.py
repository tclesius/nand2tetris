import argparse
import re
from pathlib import Path

# Figure 7.5
C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9

M_ARGUMENT = 10
M_LOCAL = 11
M_STATIC = 12
M_CONSTANT = 13
M_THIS = 14
M_THAT = 15
M_POINTER = 16
M_TEMP = 17

COMMANDS = {
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
    # fehlende hinzufügen...
}

MEMORY_ACCESS_COMMANDS = {
    "argument": M_ARGUMENT,
    "local": M_LOCAL,
    "static": M_STATIC,
    "constant": M_CONSTANT,
    "this": M_THIS,
    "that": M_THAT,
    "pointer": M_POINTER,
    "temp": M_TEMP
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
            return COMMANDS[self.currentCommand.split()[0]]

    def arg1(self):
        if self.commandType() == C_ARITHMETIC:
            return self.currentCommand
        else:
            return self.currentCommand.split()[1]

    def arg2(self):
        if self.commandType() in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            return int(self.currentCommand.split()[2])


POP = "@SP\nM=M-1\nA=M\n"  # pop value from stack (point to it)
PUSH = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"  # push value from D register to stack


class CodeWriter:

    def __init__(self, outputFile):
        self.outputFile = open(Path(outputFile).with_suffix('.asm'), 'w')
        self.eq_label_id = 0
        self.gt_label_id = 0
        self.lt_label_id = 0

    def setFileName(self, fileName):
        ...

    def writeArithmetic(self, command):
        if command == "add":
            self.outputFile.write(POP)
            self.outputFile.write("D=M\n")
            self.outputFile.write(POP)
            self.outputFile.write("D=M+D\n")
            self.outputFile.write(PUSH)
        if command == "sub":
            self.outputFile.write(POP)
            self.outputFile.write("D=M\n")
            self.outputFile.write(POP)
            self.outputFile.write("D=M-D\n")
            self.outputFile.write(PUSH)
        if command == "neg":
            self.outputFile.write(POP)
            self.outputFile.write("D=!M\n")
            self.outputFile.write("D=D+1\n")
            self.outputFile.write(PUSH)
        if command == "eq":
            self.outputFile.write(POP)
            self.outputFile.write("D=M\n")
            self.outputFile.write(POP)
            self.outputFile.write("D=M-D\n")
            self.outputFile.write(f"@EQ{self.eq_label_id}\n")
            self.outputFile.write("D;JEQ\n")
            self.outputFile.write("D=0\n")
            self.outputFile.write(f"@NEQ{self.eq_label_id}\n")
            self.outputFile.write("0;JMP\n")
            self.outputFile.write(f"(EQ{self.eq_label_id})\n")
            self.outputFile.write("D=-1\n")
            self.outputFile.write(f"(NEQ{self.eq_label_id})\n")
            self.outputFile.write(PUSH)
            self.eq_label_id += 1
        if command == "gt":
            self.outputFile.write(POP)
            self.outputFile.write("D=M\n")
            self.outputFile.write(POP)
            self.outputFile.write("D=M-D\n")
            self.outputFile.write(f"@GT{self.gt_label_id}\n")
            self.outputFile.write("D;JGT\n")
            self.outputFile.write("D=0\n")
            self.outputFile.write(f"@NGT{self.gt_label_id}\n")
            self.outputFile.write("0;JMP\n")
            self.outputFile.write(f"(GT{self.gt_label_id})\n")
            self.outputFile.write("D=-1\n")
            self.outputFile.write(f"(NGT{self.gt_label_id})\n")
            self.outputFile.write(PUSH)
            self.gt_label_id += 1
        if command == "lt":
            self.outputFile.write(POP)
            self.outputFile.write("D=M\n")
            self.outputFile.write(POP)
            self.outputFile.write("D=M-D\n")
            self.outputFile.write(f"@LT{self.lt_label_id}\n")
            self.outputFile.write("D;JLT\n")
            self.outputFile.write("D=0\n")
            self.outputFile.write(f"@NLT{self.lt_label_id}\n")
            self.outputFile.write("0;JMP\n")
            self.outputFile.write(f"(LT{self.lt_label_id})\n")
            self.outputFile.write("D=-1\n")
            self.outputFile.write(f"(NLT{self.lt_label_id})\n")
            self.outputFile.write(PUSH)
            self.lt_label_id += 1
        if command == "and":
            self.outputFile.write(POP)
            self.outputFile.write("D=M\n")
            self.outputFile.write(POP)
            self.outputFile.write("D=M&D\n")
            self.outputFile.write(PUSH)
        if command == "or":
            self.outputFile.write(POP)
            self.outputFile.write("D=M\n")
            self.outputFile.write(POP)
            self.outputFile.write("D=M|D\n")
            self.outputFile.write(PUSH)
        if command == "not":
            self.outputFile.write(POP)
            self.outputFile.write("D=-M\n")
            self.outputFile.write("D=D-1\n")
            self.outputFile.write(PUSH)

    def WritePushPop(self, command, segment, index):
        if MEMORY_ACCESS_COMMANDS[segment] == M_CONSTANT:
            if command == C_PUSH:
                self.outputFile.write(f"@{index}\nD=A\n")
                self.outputFile.write(PUSH)

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

        # print(parser.arg1(), parser.arg2())
        # print(parser.currentCommand)
