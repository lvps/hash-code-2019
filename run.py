#!/usr/bin/env python3

import myio


def main():
	lines = myio.read('input.txt')

	# COMPUTE IT

	myio.write('output.txt', lines)


if __name__ == "__main__":
	main()
