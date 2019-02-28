#!/usr/bin/env python3


def do_the_computation(lines):
	return lines


def read(filename):
	lines = []
	with open(filename) as f:
		for line in f:
			line = line.strip()
			if len(line) <= 0:
				continue
			lines.append(line)
	return lines


def write(filename: str, lines):
	with open(filename, 'w') as f:
		for line in lines:
			f.write(f"{line}\n")
