C_COMMAND = 0
A_COMMAND = 1
L_COMMAND = 2


class Parser:
    """ encapsulates access to the input code. Reads an assembly language command parses it, and
        provides convenient access to the commands components (field and symbols). In addition, removes all white
        space and comments"""

    @staticmethod
    def commandType(c: str):
        if c.startswith("@"):
            return A_COMMAND

        elif ("=" in c) or (";" in c):
            return C_COMMAND

        elif c.startswith("(") and c.endswith(")"):
            return L_COMMAND

    @staticmethod
    def symbol(c: str):
        return c.strip("@").strip("(").strip(")")

    @staticmethod
    def dest(c: str):
        if "=" in c:
            return c.split("=")[0]

    @staticmethod
    def comp(c: str):
        if "=" in c:
            return c.split("=")[1]
        elif ";" in c:
            return c.split(";")[0]

    @staticmethod
    def jump(c: str):
        if ";" in c:
            return c.split(";")[1]


comp_lookup = {
    # with a = 0
    "0"  : 0b0101010,
    "1"  : 0b0111111,
    "-1" : 0b0111010,
    "D"  : 0b0001100,
    "A"  : 0b0110000,
    "!D" : 0b0001101,
    "!A" : 0b0110001,
    "-D" : 0b0001111,
    "-A" : 0b0110011,
    "D+1": 0b0011111,
    "A+1": 0b0110111,
    "D-1": 0b0001110,
    "A-1": 0b0110010,
    "D+A": 0b0000010,
    "D-A": 0b0010011,
    "A-D": 0b0000111,
    "D&A": 0b0000000,
    "D|A": 0b0010101,

    "M"  : 0b1110000,
    "!M" : 0b1110001,
    "-M" : 0b1110011,
    "M+1": 0b1110111,
    "M-1": 0b1110010,
    "D+M": 0b1000010,
    "D-M": 0b1010011,
    "M-D": 0b1000111,
    "D&M": 0b1000000,
    "D|M": 0b1010101,

}

dest_lookup = ["null", "M", "D", "MD", "A", "AM", "AD", "AMD"]
jump_lookup = ["null", "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]


class Code:
    """translates hack assembly language mnemonics into binary codes"""

    @staticmethod
    def symbol(c: str):
        if Parser.commandType(c) in [L_COMMAND, A_COMMAND]:
            return int(Parser.symbol(c))

    @staticmethod
    def dest(c: str):
        if Parser.commandType(c) == C_COMMAND:
            if Parser.dest(c):
                return dest_lookup.index(Parser.dest(c))
        return 0

    @staticmethod
    def comp(c: str):
        if Parser.commandType(c) == C_COMMAND:
            return comp_lookup[Parser.comp(c)]
        return 0

    @staticmethod
    def jump(c: str):
        if Parser.commandType(c) == C_COMMAND:
            if Parser.jump(c):
                return jump_lookup.index(Parser.jump(c))
        return 0


class SymbolTable:

    @staticmethod
    def addEntry(symbol: str, address: int):
        ...

    @staticmethod
    def contains(symbol: str) -> bool:
        ...

    @staticmethod
    def GetAddress(symbol: str) -> int:
        ...


from bitstring import BitArray

with open("PongL.asm") as input:
    # TODO:regex to be more specific and have less error-prone code
    # TODO: use input.readline (no array construction less overhead)
    # TODO: work with bytes instead of str

    for line in input.readlines():
        line = line.partition("//")[0].rstrip().strip()  # Ignore Comments, Whitespace
        if line:  # Ignore Empty lines

            if Code.symbol(line) is not None:
                # print("0" + f"{Code.symbol(line):015b}")
                a = BitArray(bin="0" + f"{Code.symbol(line):015b}").hex
                #print(BitArray(bin="0" + f"{Code.symbol(line):015b}").hex)
            if Code.comp(line):
                # print(f"{111}" + f"{Code.comp(line):07b}" + f"{Code.dest(line):03b}" + f"{Code.jump(line):03b}")
                b = BitArray(bin=f"{111}" + f"{Code.comp(line):07b}" + f"{Code.dest(line):03b}" + f"{Code.jump(line):03b}").hex
                #print(BitArray(
                #        bin=f"{111}" + f"{Code.comp(line):07b}" + f"{Code.dest(line):03b}" + f
                #        "{Code.jump(line):03b}").hex)
