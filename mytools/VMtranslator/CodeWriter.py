from Converter import *
from Const import *


class CodeWriter(Converter):
    def __init__(self, file):
        self.filename = None
        self.file = open(file, 'w')
        super().__init__(self.file)

    def setFileName(self, fileName):
        self.filename = fileName

    def writeInit(self):
        ...

    def writeLabel(self, label):
        ...

    def writeGoto(self, label):
        ...

    def writeIf(self, label):
        ...

    def writeCall(self, functionName, numArgs):
        return_address = self.gen_label(functionName)
        self.push(S.CONSTANT, return_address)  # push return_address
        self.push(S.REG, R.LCL)  # push LCL
        self.push(S.REG, R.ARG)  # push ARG
        self.push(S.REG, R.THIS)  # push THIS
        self.push(S.REG, R.THAT)  # push THAT

        self._a_command(R.SP)
        self._c_command("D", "A")
        self.
        

        ...

    def writeReturn(self):
        self.push()

    def writeFunction(self, functionName, numLocals):
        self._l_command(functionName)
        for local in range(numLocals):
            self.push(S.CONSTANT, 0)

    def writeArithmetic(self, command):
        if command == 'add':  self.binary('+')
        elif command == 'sub':  self.binary('-')
        elif command == 'and':  self.binary('&')
        elif command == 'or':  self.binary('|')
        elif command == 'neg':  self.unary('-')
        elif command == 'not':  self.unary('!')
        elif command == 'eq':  self.compare('JEQ')
        elif command == 'gt':  self.compare('JGT')
        elif command == 'lt':  self.compare('JLT')

    def writePushPop(self, command, segment, index):
        if command == C_PUSH:   self.push(segment, index)
        elif command == C_POP:  self.pop(segment, index)

    def close(self):
        self.file.close()
