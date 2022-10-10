import os
import re
import sys
import typing
import warnings
from bitstring import BitArray
from typing.io import IO

from spec import *
from pathlib import Path


# TODO Refactor / Console runnable "python assembler.py [--asm (filepath relative / absolut)][--o (output filename)][
#  --hack, --raw2]"


class Parser:
    """ encapsulates access to the input code. Reads an assembly language command parses it, and
        provides convenient access to the commands components (field and symbols). In addition, removes all white
        space and comments"""

    def __init__(self, file: typing.Union[str, bytes, os.PathLike]):
        self.input = open(file)
        self.line = None
        self.line_number = 0
        self.eof = False

    def reset(self):
        self.line = None
        self.line_number = 0
        self.eof = False

    def advance(self):
        # returns if eof is reached
        self.line = self.input.readline()
        self.line_number += 1
        self.eof = self.line == ""

    def commandType(self):
        self.line = self.line.partition("//")[0].rstrip().strip()  # strip Comments, Whitespace

        if re.match("^@[a-zA-Z_.$:]+\\d*$", self.line):
            return commandType.A_COMMAND

        elif re.match("^@\\d*$", self.line):
            if re.match("[A-Z]", self.line):
                warnings.warn("The convention is to use lowercase for variables")
            return commandType.A_COMMAND

        elif ("=" in self.line) ^ (";" in self.line):
            # tokenize
            token = re.split('[=;]', self.line)

            if ';' in self.line:
                # must be of format "comp;jump"
                if token[0] in COMP_TABLE:
                    if token[1] in JUMP_TABLE:
                        return commandType.C_COMMAND

            elif '=' in self.line:
                # must be of format "dest=jump"
                if token[0] in DEST_TABLE:
                    if token[1] in COMP_TABLE:
                        return commandType.C_COMMAND

            raise Exception(f"Unexpected command on line: {self.line_number}", f"token: {token}")

        elif re.match("^[(][a-zA-Z_.$:]*\\d*[)]$", self.line):
            if re.match("[a-z]", self.line):
                warnings.warn("The convention is to use uppercase for labels")
            return commandType.L_COMMAND

    def symbol(self):
        return self.line.strip("@").strip("(").strip(")")

    def dest(self):
        if '=' in self.line:
            return self.line.split("=")[0]
        return ""

    def comp(self):
        token = re.split('[=;]', self.line)
        if '=' in self.line:
            return token[1]

        elif ';' in self.line:
            return token[0]
        return ""

    def jump(self):
        if ";" in self.line:
            return self.line.split(";")[1]
        return ""


def found(index):
    if index == -1:
        return False
    return True





if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <file to assemble> options: <--hack,--raw2>")

    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    file: typing.Union[str, bytes, os.PathLike] = sys.argv[0]
    p = Parser(file)
    t = SymbolTable()
    filename = Path(sys.argv[0]).stem
    f = list[IO]
    if "--hack" in opts:
        f += open(filename+".hack", "w")
    elif "--raw2" in opts:
        f += open(filename, "w")
    else:
        f += open(filename + ".hack", "w")

    counter = 0
    # first pass
    while 1:
        p.advance()
        if p.commandType() in [commandType.C_COMMAND, commandType.A_COMMAND]:
            counter += 1

        if p.commandType() is commandType.L_COMMAND:
            if t.contains(p.symbol()):
                raise Exception(f"Symbol already in Symbol table. line: {p.line_number}")
            t.addEntry(p.symbol(), counter)
        if p.eof:
            break

    p.reset()
    newSymbolAddress = 16
    # second pass
    while 1:
        p.advance()
        if p.commandType() is commandType.A_COMMAND:
            if not p.symbol().isnumeric():
                if t.contains(p.symbol()):
                    for s in f:
                        s.write(f"{t.GetAddress(p.symbol()):016b}\n")
                else:
                    t.addEntry(p.symbol(), newSymbolAddress)
                    newSymbolAddress += 1
            else:
                f.write(f"{int(p.symbol()):016b}\n")

        if p.commandType() == commandType.C_COMMAND:
            f.write('111' + Code.comp(p.comp()) + Code.dest(p.dest()) + Code.jump(p.jump()) + "\n")

        if p.eof:
            break
