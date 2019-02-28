#!/usr/bin/env python3
import sys

import argparse
import multiprocessing
import random
from dataclasses import dataclass
from threading import Thread, Lock
from typing import List, Set, Optional
import simanneal

import myio

lock = Lock()
photos = []
vertical_photos = []
horizontal_photos = []
best = -1


def delta_for_swap(sol, a, b):
	if a > b:
		a, b = b, a

	previous = 0
	next = 0

	if a > 0:
		previous += transition_score(sol[a - 1], sol[a])
		next += transition_score(sol[a - 1], sol[b])
	if a < len(sol) - 1:
		previous += transition_score(sol[a], sol[a + 1])
		next += transition_score(sol[b], sol[a + 1])
	if b > 0:
		previous += transition_score(sol[b - 1], sol[b])
		next += transition_score(sol[b - 1], sol[a])
	if b < len(sol) - 1:
		previous += transition_score(sol[b], sol[b + 1])
		next += transition_score(sol[a], sol[b + 1])
	return next - previous


class AnnealIt(simanneal.Annealer):
	def __init__(self, id, state, score: int):
		super().__init__(state)
		self.copy_strategy = 'method'
		self.steps = 42  # TODO: asd
		self.current_obj = score
		self.id = str(id)

		print(f"Thread {self.id}: Score for x0 = {self.current_obj}, annealing begins")

	def move(self):
		a = random.randint(0, len(self.state) - 1)
		b = random.randint(0, len(self.state) - 1)
		while b == a:
			b = random.randint(0, len(self.state) - 1)

		delta = delta_for_swap(self.state, a, b)

		self.current_obj += delta
		self.state[a], self.state[b] = self.state[b], self.state[a]

	def energy(self):
		return -self.current_obj


def compute_it(id, output_file: str):
	# global vertical_photos
	global best
	v = vertical_photos.copy()
	h = horizontal_photos.copy()
	iv = 0
	ih = 0

	local_random = random.Random()
	seeeeeeeeed = random.randint(0, sys.maxsize) + (id*100)**3
	local_random.seed(seeeeeeeeed)
	print(f"Thread {str(id)} has seed {str(seeeeeeeeed)}")
	local_random.shuffle(v)
	local_random.shuffle(h)
	print(f"Thread {str(id)}: shuffled")

	x0 = []

	vmax = len(v) - (len(v) % 2)

	while iv < vmax or ih < len(h):
		if iv < vmax:
			slide = Slide(v[iv], v[iv + 1])
			iv += 2
			x0.append(slide)
		if ih < len(h):
			slide = Slide(h[ih])
			ih += 1
			x0.append(slide)

	print(f"Thread {str(id)}: x0 ready")

	score = objective(x0)

	print(f"Thread {str(id)}: score for x0 ready")
	# annealer = AnnealIt(id, x0, score)
	# auto_schedule = annealer.auto(minutes=0.2)
	score = local_search(x0, score)
	for i in range(0, 3):
		annealer = AnnealIt(id, x0, score)
		# annealer.set_schedule(auto_schedule)
		local_best, score = annealer.anneal()
		score = -score
		print(f"Thread {str(id)}: Annealed it! {score}")
		prev_score = score
		score = local_search(x0, score)
		if prev_score == score:
			print("Giving up")
			break

		if score > best:
			lock.acquire()
			if score > best:
				print(f"New best by {str(id)}: {str(score)}")
				best = score
				write_output(output_file, local_best)
			lock.release()

	# COMPUTE IT
	# for x in sorted(listone, key=lambda el: el.cose, reverse=True)


def main(input_file: str, output_file: str):
	file_lines = myio.read(input_file)

	nlines = int(file_lines[0])

	for i, line in enumerate(file_lines[1:]):
		pieces = line.split(' ')
		photo = Foto(i, pieces[0], pieces[1], set(pieces[2:]))
		photos.append(photo)
		if photo.is_vertical():
			vertical_photos.append(photo)
		else:
			horizontal_photos.append(photo)

	workers = []
	for i in range(0, multiprocessing.cpu_count()):
		workers.append(Thread(target=compute_it, args=(i, output_file)))
		workers[-1].start()

	for worker in workers:
		# Workers of the world, unite!
		worker.join()

	# compute_it(-1, output_file)


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
			self.vertical = False
		else:
			if self.photo1.id > self.photo2.id:  # swap swap swap
				self.photo1, self.photo2 = self.photo2, self.photo1
			self.tags = self.photo1.tags.union(self.photo2.tags)
			self.vertical = True

	def ids(self):
		if self.vertical:
			return f"{str(self.photo1.id)} {str(self.photo2.id)}"
		else:
			return str(self.photo1.id)


def local_search(sol: List[Slide], current_obj: int) -> int:
	prev_obj = current_obj
	tot = len(sol)
	for i in range(1, tot):
		j = i - 1
		delta = delta_for_swap(sol, j, i)
		if delta > 0:
			current_obj += delta
			sol[i - 1], sol[i] = sol[i], sol[i - 1]
	print(f"Local search done: from {prev_obj} to {current_obj}")
	return current_obj


def write_output(output_file, slides: List[Slide]):
	# noinspection PyListCreation
	file_lines = []
	file_lines.append(str(len(slides)))
	for slide in slides:
		file_lines.append(slide.ids())
	myio.write(output_file, file_lines)


def transition_score(first: Slide, second: Slide):
	n1 = len(first.tags.intersection(second.tags))
	n2 = len(first.tags.difference(second.tags))
	n3 = len(second.tags.difference(first.tags))

	return min(n1, n2, n3)


def objective(sol: List[Slide]):
	if len(sol) == 0:
		return 0
	score = 0
	for i in range(0, len(sol) - 1):
		score += transition_score(sol[i], sol[i+1])
	#print(f"Nice score, dude: {str(score)}")
	return score


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Do awesome computations, yeha.')
	parser.add_argument('input', type=str, help="Input file name")
	parser.add_argument('output', type=str, help="Output file name")

	args = parser.parse_args()

	main(args.input, args.output)
