"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
def BF(main, pattern):
	main_length = len(main) - 1
	pattern_length = len(pattern) - 1
	if main_length < pattern_length:
		main, pattern = pattern, main
		main_length, pattern_length = pattern_length, main_length

	index = 0
	find = False
	while index <= main_length - pattern_length and find == False:
		main_pointer = index
		pattern_pointer = 0
		while pattern_pointer <= pattern_length:
			if main[main_pointer] == pattern[pattern_pointer]:
				main_pointer += 1
				pattern_pointer += 1
			else:
				break
		if pattern_pointer > pattern_length:
			find = True
		else:
			index += 1

	if find:
		print("Find target string")
	else:
		print("No target string")


def RK(main, pattern):
	def hash_function(string):
		sumer = 0
		for i in string:
			sumer += ord(i)
		return sumer

	main_length = len(main) - 1
	pattern_length = len(pattern) - 1
	if main_length < pattern_length:
		main,pattern = pattern,main
		main_length, pattern_length = pattern_length, main_length
	pattern_hash = hash_function(pattern)

	index = 0
	find = False
	while index <= main_length - pattern_length and find == False:
		main_hash = hash_function(main[index : index+pattern_length+1])
		if main_hash == pattern_hash:
			main_pointer = index
			pattern_pointer = 0
			while pattern_pointer <= pattern_length:
				if main[main_pointer] == pattern[pattern_pointer]:
					main_pointer += 1
					pattern_pointer += 1
				else:
					break
			if pattern_pointer > pattern_length:
				find = True
			else:
				index += 1
		else:
			index += 1

	if find:
		print("Find target string")
	else:
		print("No target string")


def BM(main, pattern):
	# Find the last element less than the target.
	def binary_search(data_list, target):
		num = len(data_list)
		low = 0
		high = num - 1
		find = False
		while low <= high:
			middle_num = low + (high-low) // 2
			if data_list[middle_num] >= target:
				high = middle_num - 1
			elif middle_num == num - 1 or data_list[middle_num+1] >= target:
				find = True
				break
			else:
				low = middle_num + 1

		if find:
			return data_list[middle_num]
		else:
			return -1

	def bad_character_rule(
			character_pos,
			main,
			pattern,
			main_pointer,
			pattern_pointer):
		bad_character = main[main_pointer]
		si = pattern_pointer
		xi = -1

		if character_pos.get(ord(bad_character), False):
			pos_list = character_pos[ord(bad_character)]
			xi = binary_search(pos_list, pattern_pointer)
		bad_character_move = si - xi

		return bad_character_move

	def good_suffix_rule(
			main,
			pattern,
			main_pointer,
			pattern_pointer,
			pattern_length,
			suffix,
			prefix):
		good_suffix = pattern[pattern_pointer+1 : ]
		len_good_suffix = len(good_suffix)

		if len_good_suffix == 0:
			return 0
		if suffix[len_good_suffix] != -1:
			return pattern_pointer - suffix[len_good_suffix] + 1
		else:
			k = pattern_pointer - 1
			while k >= 0:
				if prefix[k] == True:
					return pattern_length - k + 1
				k -= 1
			return pattern_length + 1

	main_length = len(main) - 1
	pattern_length = len(pattern) - 1
	if main_length < pattern_length:
		main, pattern = pattern, main
		main_length, pattern_length = pattern_length, main_length

	"""
		The location of each character in the pattern string is stored to
		  greatly improve the search efficiency of bad characters.
	"""
	character_pos = {}
	index = 0
	for i in pattern:
		character_ascll = ord(i)
		if not character_pos.get(character_ascll, False):
			character_pos[character_ascll] = [index]
		else:
			character_pos[character_ascll].append(index)
		index += 1

	"""
		Suffix array is used to store the starting subscript value of
		  the same substring in the pattern string as the suffix substring
		  of the length (i.e. subscript).
		Prefix array is used to record whether the suffix substring of
		  the length (i.e. subscript) pattern string can match the prefix substring
		  of the pattern string.
		Both the suffix and prefix arrays start at the position marked 1,
		  and the position marked 0 is not counted. The subscript means the number
		  of characters in the substring.
	"""
	suffix = [-1] * (pattern_length+1)
	prefix = [False] * (pattern_length+1)
	for i in range(pattern_length):
		j = i
		k = 0
		while j >= 0 and pattern[pattern_length-k] == pattern[j]:
			k += 1
			suffix[k] = j
			j -= 1
		if j < 0:
			prefix[k] = True

	index = 0
	find = False
	while index <= main_length - pattern_length and find == False:
		main_pointer = index + pattern_length
		pattern_pointer = pattern_length
		while pattern_pointer >= 0:
			if main[main_pointer] == pattern[pattern_pointer]:
				main_pointer -= 1
				pattern_pointer -= 1
			else:
				"""
					get the number of moving steps from the bad character principle
					  and the good suffix principle at the same time.
				"""
				bad_character_move = bad_character_rule(character_pos,
														main,
														pattern,
														main_pointer,
														pattern_pointer)
				good_suffix_move = good_suffix_rule(main,
													pattern,
													main_pointer,
													pattern_pointer,
													pattern_length,
													suffix,
													prefix)
				break

		if pattern_pointer < 0:
			find = True
			break
		else:
			"""
				Choose multiple moving steps among bad character principle
				  and good suffix principle.
			"""
			if bad_character_move > good_suffix_move:
				index += bad_character_move
			else:
				index += good_suffix_move

	if find:
		print("Find target string")
	else:
		print("No target string")


def KMP(main, pattern):
	main_length = len(main) - 1
	pattern_length = len(pattern) - 1
	if main_length < pattern_length:
		main, pattern = pattern, main
		main_length, pattern_length = pattern_length, main_length

	"""
		The next_list array is used to store the subscript of the longest
		  matching prefix substring end character of all length prefix substrings
		  in the pattern string.
		The array subscript represents the length of the prefix substring.
	"""
	next_list = [-1] * pattern_length
	k = -1
	for i in range(1, pattern_length):
		while k != -1 and pattern[k+1] != pattern[i]:
			k = next_list[k]
		if pattern[k+1] == pattern[i]:
			k += 1
		next_list[i] = k

	index = 0
	find = False
	while index <= main_length - pattern_length and find == False:
		main_pointer = index
		pattern_pointer = 0
		while pattern_pointer <= pattern_length:
			if main[main_pointer] == pattern[pattern_pointer]:
				main_pointer += 1
				pattern_pointer += 1
			else:
				# good prefix rule
				good_prefix = pattern[ : pattern_pointer]
				len_good_prefix = len(good_prefix) - 1
				if len_good_prefix == -1:
					index += 1
				else:
					index += pattern_pointer - next_list[len_good_prefix] - 1
				break

		if pattern_pointer > pattern_length:
			find = True
			break

	if find:
		print("Find target string")
	else:
		print("No target string")
