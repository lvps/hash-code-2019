#!/usr/bin/env python3


def do_the_computation(lines):
	return lines


def main():
	lines = []

	with open('input.txt') as f:
		for line in f:
			line = line.strip()
			lines.append(line)

	lines = do_the_computation(lines)

	with open('output.txt', 'w') as f:
		for line in lines:
			f.write(f"{line}\n")


if __name__ == "__main__":
	main()
