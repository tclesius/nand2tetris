import argparse
import re
from pathlib import Path
from Const import *


class Parser:

    def __init__(self, inputFile):
        self.File = open(inputFile, "r")
        self.inputFile = self.File.readlines()
        self.File.close()
        self.inputFilePosition = 0
        self.currentCommand = ""

    def hasMoreCommands(self):
        return self.inputFilePosition < len(self.inputFile) - 1

    def removeComments(self):
        self.currentCommand = re.sub("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)", "", self.currentCommand).strip()

    def advance(self):
        self.currentCommand = self.inputFile[self.inputFilePosition]
        self.removeComments()
        self.inputFilePosition += 1

    def commandType(self):
        if self.currentCommand.startswith("@"):
            return A_COMMAND

        elif ("=" in self.currentCommand) or (";" in self.currentCommand):
            return C_COMMAND

        elif self.currentCommand.startswith("(") and self.currentCommand.endswith(")"):
            return L_COMMAND

    def symbol(self):
        return self.currentCommand.strip("@").strip("(").strip(")")

    def dest(self):
        if "=" in self.currentCommand:
            return self.currentCommand.split("=")[0]

    def comp(self):
        if "=" in self.currentCommand:
            return self.currentCommand.split("=")[1]

        if ";" in self.currentCommand:
            return self.currentCommand.split(";")[0]

    def jump(self):
        if ";" in self.currentCommand:
            return self.currentCommand.split(";")[1]

    def reset(self):
        self.inputFilePosition = 0
        self.currentCommand = ""


class Code:
    @staticmethod
    def dest(mnemonic):
        return DEST.get(mnemonic)

    @staticmethod
    def comp(mnemonic):
        return COMP.get(mnemonic)

    @staticmethod
    def jump(mnemonic):
        return JUMP.get(mnemonic)


class SymbolTable:
    def __init__(self, predefinedSymbols):
        self.table = {}
        self.table.update(predefinedSymbols)

    def addEntry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def GetAddress(self, symbol):
        return self.table.get(symbol)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='.asm assembler')
    parser.add_argument('asmFile', type=str,
                        help='.asm input file')
    parser.add_argument('--o', type=str,
                        help='output filename')
    args = parser.parse_args()

    # Initialization
    parser = Parser(args.asmFile)
    symbolTable = SymbolTable(PREDEFINED_SYMBOLS)
    romAddress = 0

    # Output file creation
    if args.o:
        outputFile = open(Path(args.o).with_suffix('.hack'), 'w')
    else:
        outputFile = open(Path(args.asmFile).with_suffix('.hack'), 'w')

    # First pass
    while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() in [C_COMMAND, A_COMMAND]:
            romAddress += 1

        if parser.commandType() == L_COMMAND:
            symbolTable.addEntry(parser.symbol(), romAddress)

    # Second pass
    parser.reset()
    ramAddress = 16

    while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() == A_COMMAND:
            if not parser.symbol().isnumeric():
                address = symbolTable.GetAddress(parser.symbol())
                if address is not None:
                    outputFile.write(f'{address:016b}\n')
                else:
                    symbolTable.addEntry(parser.symbol(), ramAddress)
                    outputFile.write(f"{ramAddress:016b}\n")
                    ramAddress += 1
            else:
                outputFile.write(f"{int(parser.symbol()):016b}\n")

        elif parser.commandType() == C_COMMAND:
            outputFile.write(f'111{Code.comp(parser.comp())}{Code.dest(parser.dest())}{Code.jump(parser.jump())}\n')

    outputFile.close()
