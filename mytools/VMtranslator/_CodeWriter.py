from pathlib import Path
from Const import *


class CodeWriter:

    def __init__(self, outputFile):
        self.outputFile = open(Path(outputFile).with_suffix('.asm'), 'w')
        self.fileName = ""
        self.EQ_ID = 0
        self.GT_ID = 0
        self.LT_ID = 0

        self.writeInit()

    def setFileName(self, fileName):
        self.fileName = fileName

    def writeInit(self):
        self.A_COMMAND(256)
        self.C_COMMAND("D", "A")
        self.A_COMMAND("SP")
        self.C_COMMAND("M", "D")
        self.writeCall("Sys.init", 0)

    def writeLabel(self, label):
        self.L_COMMAND("null$" + label)

    def writeGoto(self, label):
        self.A_COMMAND("null$" + label)
        self.C_COMMAND(comp="0", jump="JMP")

    def writeIf(self, label):
        self.POP("D")
        self.A_COMMAND("null$" + label)
        self.C_COMMAND(comp="D", jump="JNE")

    def writeCall(self, functionName, numArgs):
        self.A_COMMAND(functionName + "$" + "Return")
        self.C_COMMAND("D", "A")
        self.PUSH()

        self.A_COMMAND("LCL")
        self.C_COMMAND("D", "A")
        self.PUSH()

        self.A_COMMAND("ARG")
        self.C_COMMAND("D", "A")
        self.PUSH()

        self.A_COMMAND("THIS")
        self.C_COMMAND("D", "A")
        self.PUSH()

        self.A_COMMAND("THAT")
        self.C_COMMAND("D", "A")
        self.PUSH()

        self.A_COMMAND("SP")
        self.C_COMMAND("D", "A")
        self.A_COMMAND(numArgs)
        self.C_COMMAND("D", "D-A")
        self.A_COMMAND(5)
        self.C_COMMAND("D", "D-A")

        self.A_COMMAND("ARG")
        self.C_COMMAND("M", "D")

        self.A_COMMAND("LCL")
        self.C_COMMAND("D", "A")
        self.A_COMMAND("SP")
        self.C_COMMAND("M", "D")

        self.writeGoto(functionName)
        self.writeLabel(functionName + "$" + "Return")

    def writeReturn(self):
        # FRAME = LCL
        self.A_COMMAND("LCL")
        self.C_COMMAND("D", "M")
        self.A_COMMAND("R13")
        self.C_COMMAND("M", "D")

        # RET = *(FRAME-5)
        self.A_COMMAND(5)
        self.C_COMMAND("D", "D-A")
        self.A_COMMAND("R14")
        self.C_COMMAND("M", "D")

        # *ARG = pop()
        self.POP("D")
        self.A_COMMAND("ARG")
        self.C_COMMAND("A", "M")
        self.C_COMMAND("M", "D")

        # SP = ARG + 1
        self.A_COMMAND("ARG")
        self.C_COMMAND("D", "M")
        self.A_COMMAND("SP")
        self.C_COMMAND("M", "D+1")

        # THAT = *(FRAME - 1)
        self.A_COMMAND("R13")
        self.C_COMMAND("D", "M")

        self.C_COMMAND("A", "D-1")
        self.C_COMMAND("D", "M")
        self.A_COMMAND("THAT")
        self.C_COMMAND("M", "D")

        # THIS = *(FRAME - 2)
        self.A_COMMAND("R13")
        self.C_COMMAND("D", "M")

        self.C_COMMAND("D", "D-1")
        self.C_COMMAND("A", "D-1")
        self.C_COMMAND("D", "M")
        self.A_COMMAND("THIS")
        self.C_COMMAND("M", "D")

        # ARG = *(FRAME - 3)
        self.A_COMMAND("R13")
        self.C_COMMAND("D", "M")

        self.C_COMMAND("D", "D-1")
        self.C_COMMAND("D", "D-1")
        self.C_COMMAND("A", "D-1")
        self.C_COMMAND("D", "M")
        self.A_COMMAND("ARG")
        self.C_COMMAND("M", "D")

        # LCL = *(FRAME - 4)
        self.A_COMMAND("R13")
        self.C_COMMAND("D", "M")

        self.C_COMMAND("D", "D-1")
        self.C_COMMAND("D", "D-1")
        self.C_COMMAND("D", "D-1")
        self.C_COMMAND("A", "D-1")
        self.C_COMMAND("D", "M")
        self.A_COMMAND("LCL")
        self.C_COMMAND("M", "D")

        self.A_COMMAND("R14")
        self.C_COMMAND("A", "M")
        self.C_COMMAND(comp="0", jump="JMP")

    def writeFunction(self, functionName, numLocals):
        self.L_COMMAND(functionName)
        self.C_COMMAND("D", "0")
        for x in range(numLocals):
            self.PUSH()

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

        if SEGMENT_TYPE[segment] in [S_POINTER, S_TEMP, S_STATIC]:
            if command == C_PUSH:

                self.A_COMMAND(SEGMENT_BASE[segment] + index)
                self.C_COMMAND("D", "M")
                self.PUSH()

            if command == C_POP:
                # --->
                self.POP("D")
                self.A_COMMAND(SEGMENT_BASE[segment] + index)
                self.C_COMMAND("M", "D")

    def Close(self):
        self.outputFile.close()

    # HELPER FUNCTIONS
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

    # HELPER FUNCTIONS END
