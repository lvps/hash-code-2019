#!/usr/bin/env python3
import argparse
import multiprocessing
import random
from dataclasses import dataclass
from threading import Thread, Lock
from typing import List, Set, Optional

import myio

lock = Lock()
photos = []
vertical_photos = []
horizontal_photos = []


def compute_it(id):
	# global vertical_photos
	v = vertical_photos.copy()
	h = horizontal_photos.copy()
	iv = 0
	ih = 0

	random.shuffle(v)
	random.shuffle(h)

	x0 = []

	vmax = len(v) - (len(v) % 2)

	while iv < vmax or ih < len(h):
		if iv < vmax:
			slide = Slide(v[iv], v[iv + 1])
			iv += 2
			x0.append(slide)
		if ih < len(h):
			slide = Slide(h[ih])
			h += 1
			x0.append(slide)

	# COMPUTE IT
	# for x in sorted(listone, key=lambda el: el.cose, reverse=True)

	lock.acquire()
	print(f"{id} in da' lock: {global_variable_yeha}")
	global_variable_yeha += 1
	lock.release()


def main(input_file: str, output_file: str):
	file_lines = myio.read(input_file)


	nlines = int(file_lines[0])

	for i, line in enumerate(file_lines[1:]):
		pieces = line.split(' ')
		photo =Foto(i, pieces[0], pieces[1], set(pieces[2:]))
		photos.append(photo)
		if photo.is_vertical():
			vertical_photos.append(photo)
		else:
			horizontal_photos.append(photo)

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
	tags: Set[str]

	def is_vertical(self):
		return self.orientation == 'V'


class Slide:
	def __init__(self, first: Foto, second: Optional[Foto]=None):
		self.photo1 = first
		self.photo2 = second
		if self.photo2 is None:
			self.tags = self.photo1.tags
		else:
			self.tags = self.photo1.tags & self.photo2.tags

	# @property
	# def tags(self):


def write_output(output_file, photos: List[Foto]):
	# noinspection PyListCreation
	file_lines = []
	# TODO: double photoz
	file_lines.append(str(len(photos)))
	for photo in photos:
		file_lines.append(photo.id)
	myio.write(output_file, file_lines)


def transition_score(first: Slide, second: Slide):
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
