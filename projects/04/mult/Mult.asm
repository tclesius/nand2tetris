// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

@R0
@R1
@R2
M=0

//R0 > 0?
@R0
D=M
@END // no
D;JEQ

(LOOP)
@R1
D=M
@R2
M=M+D //r2=r2+r1
@R0
MD=M-1 //r0--

@LOOP
D;JGT // r0 > 0 ?

(END)
