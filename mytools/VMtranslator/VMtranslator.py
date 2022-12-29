import argparse
from pathlib import Path

from Parser import Parser
from _CodeWriter import CodeWriter
from Const import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='.vm translator')
    parser.add_argument('vmFiles', type=str,
                        help='.vm input file or directory')
    parser.add_argument('--o', type=str,
                        help='output filename')
    args = parser.parse_args()

    inputPath = Path(args.vmFiles)

    # Output file creation
    if args.o:
        outputFile = Path(args.o).with_suffix('.asm')
        inputFiles = [inputPath]
    else:
        if inputPath.is_dir():
            dirname = Path(Path(args.vmFiles).parts[-1])
            outputFile = Path(args.vmFiles).joinpath(dirname.with_suffix('.asm'))  # asm file has name of dir
            inputFiles = inputPath.glob('*.vm')
        else:
            outputFile = Path(args.vmFiles).with_suffix('.asm')
            inputFiles = [inputPath]

    codeWriter = CodeWriter(outputFile)

    for inputFile in inputFiles:
        codeWriter.setFileName(inputFile)
        parser = Parser(inputFile)

        while parser.hasMoreCommands():
            parser.advance()
            if parser.commandType() in [C_PUSH, C_POP]:
                codeWriter.WritePushPop(parser.commandType(), parser.arg1(), parser.arg2())

            if parser.commandType() == C_ARITHMETIC:
                codeWriter.writeArithmetic(parser.arg1())

            if parser.commandType() == C_LABEL:
                codeWriter.writeLabel(parser.arg1())

            if parser.commandType() == C_GOTO:
                codeWriter.writeGoto(parser.arg1())

            if parser.commandType() == C_IF:
                codeWriter.writeIf(parser.arg1())

            if parser.commandType() == C_FUNCTION:
                codeWriter.writeFunction(parser.arg1(), parser.arg2())

            if parser.commandType() == C_RETURN:
                codeWriter.writeReturn()

            if parser.commandType() == C_CALL:
                codeWriter.writeCall(parser.arg1(), parser.arg2())
