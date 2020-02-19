"""
	The data of the bloon filter is stored in an array(self.__data) to
	  store multiple expanded binary tables.
	Self.__size express the size of the current binary table.
	Self.__num express the number of changed binaries in the current table.
	  (No matter whether there are duplicates or not, self.__num add 3
	  for every data you add, so as to minimize conflicts.)
	Self.__stowage is the loading factor, with a maximum of 0.8.
	  If it is greater than 0.8, a new table of double size will be
	  added to the self.__data.
"""
class Bloom_Filter():
	def __init__(self, number):
		self.__data = [bytearray(number)]
		self.__size = number
		self.__num = 0
		self.__stowage = self.__num / self.__size

	# using ASCII method
	def __hash_function_1(self, data, size):
		if type(data) != type("1"):
			data = str(data)

		num = 0
		sumer = 0
		for i in data:
			num += 1
			sumer += ord(i)
		sumer //= num
		sumer %= size

		return sumer

	"""
		Divide the ascll value on each bit by its own number of digits,
		  accumulate, and then calculate the remainder with the table size.
	"""
	def __hash_function_2(self, data, size):
		if type(data) != type("1"):
			data = str(data)

		num = 0
		sumer = 0
		for i in data:
			num += 1
			sumer += ord(i) // num
		sumer %= size

		return sumer

	# Square and then Mod
	def __hash_function_3(self, data, size):
		if type(data) != type(1):
			num = 0
			sumer = 0
			for i in data:
				num += 1
				sumer += ord(i)
			data = sumer

		sumer = pow(data, 2)
		sumer %= size
		return sumer

	def add_data(self, data):
		self.__num += 3
		byte_list = self.__data[-1]

		hash_value_1 = self.__hash_function_1(data, self.__size)
		hash_value_2 = self.__hash_function_2(data, self.__size)
		hash_value_3 = self.__hash_function_3(data, self.__size)
		byte_list[hash_value_1] = 1
		byte_list[hash_value_2] = 1
		byte_list[hash_value_3] = 1

		self.__stowage = self.__num / self.__size

		# Determine whether to increase a table twice the size
		if self.__stowage > 0.8:
			self.__data.append(bytearray(self.__size*2))

			# Update num, size, stowage to the value of the new table
			self.__num = 0
			self.__size *= 2
			self.__stowage = 0

	def find_data(self, data):
		find = False
		for num, byte_list in enumerate(self.__data):
			hash_value_1 = self.__hash_function_1(data, len(byte_list))
			hash_value_2 = self.__hash_function_2(data, len(byte_list))
			hash_value_3 = self.__hash_function_3(data, len(byte_list))

			if byte_list[hash_value_1] == 1 and byte_list[hash_value_2] == 1 \
				and byte_list[hash_value_3] == 1:

				find = True
				break

		if find:
			print("Find data in list_{}".format(num+1))
		else:
			print("No target data")

	def return_basic_information(self):
		return len(self.__data), self.__size, self.__num, self.__stowage
