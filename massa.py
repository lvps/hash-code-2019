#!/usr/bin/env python3
from subprocess import call

print("\nTXT A\n")
call(['./run.py', 'a_example.txt', 'out_a_example.txt'])
print("\nTXT B\n")
call(['./run.py', 'b_lovely_landscapes.txt', 'out_b_lovely_landscapes.txt'])
print("\nTXT C\n")
call(['./run.py', 'c_memorable_moments.txt', 'out_c_memorable_moments.txt'])
print("\nTXT D\n")
call(['./run.py', 'd_pet_pictures.txt', 'out_d_pet_pictures.txt'])
print("\nTXT E\n")
call(['./run.py', 'e_shiny_selfies.txt', 'out_e_shiny_selfies.txt'])
print("CARRARA")
