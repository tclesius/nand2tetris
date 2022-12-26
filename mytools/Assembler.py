import argparse
import re
from pathlib import Path

C_COMMAND = 0
A_COMMAND = 1
L_COMMAND = 2

# MNEMONICS
COMP = {
    "0": '0101010',
    "1": '0111111',
    "-1": '0111010',
    "D": '0001100',
    "A": '0110000',
    "!D": '0001101',
    "!A": '0110001',
    "-D": '0001111',
    "-A": '0110011',
    "D+1": '0011111',
    "A+1": '0110111',
    "D-1": '0001110',
    "A-1": '0110010',
    "D+A": '0000010',
    "D-A": '0010011',
    "A-D": '0000111',
    "D&A": '0000000',
    "D|A": '0010101',

    "M": '1110000',
    "!M": '1110001',
    "-M": '1110011',
    "M+1": '1110111',
    "M-1": '1110010',
    "D+M": '1000010',
    "D-M": '1010011',
    "M-D": '1000111',
    "D&M": '1000000',
    "D|M": '1010101',

}
DEST = {
    "null": '000',
    "M": '001',
    "D": '010',
    "MD": '011',
    "A": '100',
    "AM": '101',
    "AD": '110',
    "AMD": '111',
}
JUMP = {
    "null": '000',
    "JGT": '001',
    "JEQ": '010',
    "JGE": '011',
    "JLT": '100',
    "JNE": '101',
    "JLE": '110',
    "JMP": '111',
}
# MNEMONICS END

PREDEFINED_SYMBOLS = {
    "SP": 0x0000,
    "LCL": 0x0001,
    "ARG": 0x0002,
    "THIS": 0x0003,
    "THAT": 0x0004,
    "R0": 0x0000,
    "R1": 0x0001,
    "R2": 0x0002,
    "R3": 0x0003,
    "R4": 0x0004,
    "R5": 0x0005,
    "R6": 0x0006,
    "R7": 0x0007,
    "R8": 0x0008,
    "R9": 0x0009,
    "R10": 0x000A,
    "R11": 0x000B,
    "R12": 0x000C,
    "R13": 0x000D,
    "R14": 0x000E,
    "R15": 0x000F,
    "SCREEN": 0x4000,
    "KBD": 0x6000,
}


class Parser:

    def __init__(self, inputFile):
        self.File = open(inputFile, "r")
        self.inputFile = self.File.readlines()
        self.File.close()
        self.inputFilePosition = 0
        self.currentCommand = ""

    def hasMoreCommands(self):
        return self.inputFilePosition < len(self.inputFile) - 1

    def advance(self):
        self.inputFilePosition += 1
        self.currentCommand = re.sub("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)", "",
                                     self.inputFile[self.inputFilePosition]).strip()

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
