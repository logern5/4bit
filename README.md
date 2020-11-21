# 4bit
## Compilation and running
To compile:

`cat program.4b | xxd -r -p > program.bin`

To run:

`python3 4bit.py program.bin`

Example programs can be found in the `examples` folder.

## Language
### Instructions
Each instruction is 4 bits and is represented by a single character. There are two stacks, the A stack (the main
stack, sometimes just referred to as the stack), and the secondary B stack. Most operations are done on the A stack,
while items from the B stack are used for temporary storage and for addresses.
The instructions are as follows.
* 0x1 Push next byte in the code to the A stack
* 0x2 Add 2 items off the A stack and push result onto A stack
* 0x3 Subtract 2 items off the A stack and push result to A stack
* 0x4 Mul two items off the A stack and push result to the A stack
* 0x5 Jump to addr on B stack if top 2 items on A stack are equal
* 0x6 Jump to addr on B stack if A0 > A1 (first and second items off top of A stack)
* 0x7 Jump to addr on B stack if A0 < A1
* 0x8 Unconditional jump to addr on B stack
* 0x9 Read char from stdin and push to A stack
* 0xA Write char to stdout from stack
* 0xB Call library (8-bit addr) function
* 0xC Pop off B-stack and push on A-stack
* 0xD Pop off A-stack and push on B-stack
* 0xE Duplicate item on top of A stack
* 0xF Delete item off top of A stack

### Library functions
Library functions take various arguments, and are called with the 0xB instruction. The instructions are as follows:
* 0x01 Push the program counter onto the A stack
* 0x02 Delete item off top of A stack
* 0x03 Increment item on top of A stack
* 0x04 Print string on top of A stack
