#!/usr/bin/python3
from time import time

# finds the positions of 1s in the binary representation of a number
def findExponents(number):
	found_exps = []
	max_exp = 0
	while (number >> max_exp) != 0:
		max_exp += 1
	for potential_exp in range(max_exp-1, -1, -1):
		if (number >> potential_exp) == 1:
			found_exps.append(potential_exp)
			number -= 1 << potential_exp
	return found_exps

def bitShiftMul_expsNotKnown(left_factor, right_factor):
	found_exps = findExponents(right_factor)
	product = 0
	for exp in found_exps:
		product += left_factor << exp
	return product

def bitShiftMul_precomputedExps(left_factor, right_exps):
	product = 0
	for exp in right_exps:
		product += left_factor << exp
	return product

def regularMul(left_factor, right_factor):
	return left_factor * right_factor


def benchmark(title, left_factor, right_factors, method, repeat=500):
	start_seconds = time()
	for i in range(repeat):
		for right_factor in right_factors:
			method(left_factor, right_factor)
	elapsed_seconds = time() - start_seconds
	
	# repeated last time to get the solutions	
	products = []
	for right_factor in right_factors:
		products.append(method(left_factor, right_factor))
	print(title)
	print(products)
	print("Repeating the computation {} times took: {:.6f}s\n".format(repeat, elapsed_seconds))


right_factors = [5, 12150009512, 442342, 0, 1, 5532, 32523435, 3200985, 347209438]
left_factor = 245432
precomputed_exps = [findExponents(r_factor) for r_factor in right_factors]

benchmark("-- Regular mul:", left_factor, right_factors, regularMul)
benchmark("-- Bit shift mul (unoptimized):", left_factor, right_factors, bitShiftMul_expsNotKnown)
benchmark("-- Bit shift mul (precomputed exps):", left_factor, precomputed_exps, bitShiftMul_precomputedExps)

print("----- the optimistic case with right numbers being the powers of 2")
right_factors = [2**6, 2**23, 2**14, 0, 1, 2**18, 2**40, 2**27, 2**35]
precomputed_exps = [findExponents(r_factor) for r_factor in right_factors]

benchmark("-- Regular mul:", left_factor, right_factors, regularMul)
benchmark("-- Bit shift mul (unoptimized):", left_factor, right_factors, bitShiftMul_expsNotKnown)
benchmark("-- Bit shift mul (precomputed exps):", left_factor, precomputed_exps, bitShiftMul_precomputedExps)

"""
The conclusion: there is no gain in replacing multiplication by an explicit sum of bit shifts in python3. Even the approach with precomupted exponents proves to be around 10x slower than regular multiplication (around 2x worse if only powers of 2 were used).
"""
