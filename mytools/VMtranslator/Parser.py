import re

from Const import *


class Parser:
    def __init__(self, inputFile):
        self.File = open(inputFile, "r")
        self.inputFile = self.File.readlines()
        self.File.close()
        self.inputFilePosition = 0
        self.currentCommand = ""

    def hasMoreCommands(self):
        return self.inputFilePosition < len(self.inputFile)

    def removeComments(self):
        self.currentCommand = re.sub("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)", "", self.currentCommand).strip()

    def advance(self):
        self.currentCommand = self.inputFile[self.inputFilePosition]
        self.removeComments()
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
