#!/usr/bin/python3
import fileinput, sys
import logging as log
import tty, termios
import binascii

log.basicConfig(stream=sys.stderr, level=log.ERROR)

f = open(sys.argv[1],"rb")
code_bin = f.read()
code = binascii.hexlify(code_bin).decode('utf-8')
code_len = len(code)

log.debug(f"Hex code: {code}")
log.debug(f"Code string len: {len(code)}")

pc = 0 # Program counter
stack = []
bstack = []


def lib_func(id):
	if id == 1:
		stack.append(pc)
	elif id == 2:
		stack.pop()
	elif id == 3:
		item = stack.pop()
		stack.append(item + 1)
	elif id == 4:
		item = stack.pop()
		print(item)
	return

while pc < code_len:
	inst = code[pc]
	if inst == '1':
		log.debug(f"PC = {hex(pc)},Inst 0x1 push byte to stack")
		# Nibbles stored in big endian order
		next_hn = int(code[pc+1], 16)
		next_ln = int(code[pc+2], 16)
		next_byte = (next_hn << 4) + next_ln
		log.debug(f"Byte to push: {hex(next_byte)}")
		stack.append(next_byte)
		pc += 2
	elif inst == '2':
		log.debug(f"PC = {hex(pc)},Inst 0x2 add two bytes off stack")
		a = stack.pop()
		b = stack.pop()
		stack.append(a + b)
	elif inst == '3':
		log.debug(f"PC = {hex(pc)},Inst 0x3 subtract two bytes off stack")
		a = stack.pop()
		b = stack.pop()
		stack.append(a - b)
	elif inst == '4':
		log.debug(f"PC = {hex(pc)},Inst 0x4 mul two bytes off stack")
		a = stack.pop()
		b = stack.pop()
		stack.append(a * b)
	elif inst == '5':
		log.debug(f"PC = {hex(pc)},Inst 0x5 Jump to addr on B-stack if two items on stack are equal")
		a = stack[-1]
		b = stack[-2]
		addr = bstack[-1]
		log.debug(f"A = {a}")
		log.debug(f"B = {b}")
		log.debug(f"addr = {hex(addr)}")
		if a == b:
			pc = addr - 1
	elif inst == '6':
		log.debug(f"PC = {hex(pc)},Inst 0x6 Jump to addr on B-stack if A > B")
		a = stack[-1]
		b = stack[-2]
		addr = bstack[-1]
		log.debug(f"A = {a}")
		log.debug(f"B = {b}")
		log.debug(f"addr = {hex(addr)}")
		if a > b:
			pc = addr - 1
	elif inst == '7':
		log.debug(f"PC = {hex(pc)},Inst 0x7 Jump to addr if A < B")
		a = stack[-1]
		b = stack[-2]
		addr = bstack[-1]
		log.debug(f"A = {a}")
		log.debug(f"B = {b}")
		log.debug(f"addr = {hex(addr)}")
		if a < b:
			pc = addr - 1
	elif inst == '8':
		log.debug(f"PC = {hex(pc)},Inst 0x8 Unconditional jump to addr")
		pc = bstack[-1] - 1
	elif inst == '9':
		log.debug(f"PC = {hex(pc)},Inst 0x9 Read char and push to stack")
		# Make char input work without newline
		old_settings = termios.tcgetattr(0)
		tty.setcbreak(0)
		c = sys.stdin.read(1)
		termios.tcsetattr(0, termios.TCSADRAIN, old_settings)
		stack.append(ord(c))
	elif inst == 'a':
		log.debug(f"PC = {hex(pc)},Inst 0xA Write char from stack")
		sys.stdout.write(chr(stack[-1]))
	elif inst == 'b':
		log.debug(f"PC = {hex(pc)},Inst 0xB Call library (8-bit) func")
		next_hn = int(code[pc+1], 16)
		next_ln = int(code[pc+2], 16)
		next_byte = (next_hn << 4) + next_ln
		log.debug(f"Calling library function {hex(next_byte)}")
		lib_func(next_byte)
		pc += 2
	elif inst == 'c':
		log.debug(f"PC = {hex(pc)},Inst 0xC Pop off B-stack and push on A-stack")
		stack.append(bstack.pop())
	elif inst == 'd':
		log.debug(f"PC = {hex(pc)},Inst 0xD Pop off A-stack and push on B-stack")
		bstack.append(stack.pop())
	elif inst == 'e':
		log.debug(f"PC = {hex(pc)},Inst 0xE Duplicate item on top of stack")
		item = stack.pop()
		stack.append(item)
		stack.append(item)
	elif inst == 'f':
		log.debug(f"PC = {hex(pc)},Inst 0xF Delete item off of top of stack")
		stack.pop()
	pc += 1
