// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
//@24576 KeyboardIO
//@16384 Screen Start
//@24575 Screen End

(LOOP)
@16383
D=A
@R0
M=D

@24576
D=M
@BLACK
D;JGT
@WHITE


(WHITE)
@R0
AMD=M+1
M=0
@24575
D=D-A
@WHITE
D;JNE

@LOOP
0;JMP

(BLACK)
@R0
AMD=M+1
M=-1
@24575
D=D-A
@BLACK
D;JNE

@LOOP
0;JMP
