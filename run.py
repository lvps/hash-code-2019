#!/usr/bin/env python3
import argparse
import myio


def main(input: str, output: str):
	lines = myio.read(input)

	# COMPUTE IT

	myio.write(output, lines)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Do awesome computations, yeha.')
	parser.add_argument('input', type=str, help="Input file name")
	parser.add_argument('output', type=str, help="Output file name")

	args = parser.parse_args()

	main(args.input, args.output)
