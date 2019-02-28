#!/usr/bin/env python3
import argparse
import multiprocessing
import random
import time
from threading import Thread, Lock

import myio

lock = Lock()
global_variable_yeha = 10


def compute_it(id):
	# COMPUTE IT
	global global_variable_yeha

	lock.acquire()
	print(f"{id} in da' lock: {global_variable_yeha}")
	global_variable_yeha += 1
	lock.release()


def main(input_file: str, output_file: str):
	lines = myio.read(input_file)

	workers = []
	for i in range(0, multiprocessing.cpu_count()):
		workers.append(Thread(target=compute_it, args=(str(i))))
		workers[-1].start()

	for worker in workers:
		# Workers of the world, unite!
		worker.join()

	myio.write(output_file, lines)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Do awesome computations, yeha.')
	parser.add_argument('input', type=str, help="Input file name")
	parser.add_argument('output', type=str, help="Output file name")

	args = parser.parse_args()

	main(args.input, args.output)
