#!/usr/bin/env python3
import argparse
import multiprocessing
from dataclasses import dataclass
from threading import Thread, Lock
from typing import List

import myio

lock = Lock()
global_variable_yeha = 10


def compute_it(id):
	global global_variable_yeha

	# COMPUTE IT
	# for x in sorted(listone, key=lambda el: el.cose, reverse=True)

	lock.acquire()
	print(f"{id} in da' lock: {global_variable_yeha}")
	global_variable_yeha += 1
	lock.release()


def main(input_file: str, output_file: str):
	file_lines = myio.read(input_file)

	photos = []
	nlines = int(file_lines[0])

	for i, line in enumerate(file_lines[1:]):
		pieces = line.split(' ')
		photos.append(Foto(i, pieces[0], pieces[1], set(pieces[2:])))

	workers = []
	for i in range(0, multiprocessing.cpu_count()):
		workers.append(Thread(target=compute_it, args=(str(i))))
		workers[-1].start()

	for worker in workers:
		# Workers of the world, unite!
		worker.join()

	write_output(output_file, photos)


@dataclass
class Foto:
	id: int
	orientation: str
	n_tags: int
	tags: set[str]


def write_output(output_file, photos: List[Foto]):
	# noinspection PyListCreation
	file_lines = []
	# TODO: double photoz
	file_lines.append(str(len(photos)))
	for photo in photos:
		file_lines.append(photo.id)
	myio.write(output_file, file_lines)


def transition_score(first: Foto, second: Foto):
	n1 = first.tags.intersection(second.tags)
	n2 = first.tags.difference(second.tags)
	n3 = second.tags.difference(first.tags)

	return min(n1, n2, n3)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Do awesome computations, yeha.')
	parser.add_argument('input', type=str, help="Input file name")
	parser.add_argument('output', type=str, help="Output file name")

	args = parser.parse_args()

	main(args.input, args.output)
