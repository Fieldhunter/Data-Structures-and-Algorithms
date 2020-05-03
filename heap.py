"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
# implement a large top heap
class Heap():
	def __init__(self):
		self.__data = [None]

	def add_data(self, element):
		self.__data.append(element)
		index = len(self.__data) - 1
		while index > 1:
			if self.__data[index] > self.__data[index//2]:
				self.__data[index], self.__data[index//2] = \
					self.__data[index//2], self.__data[index]
				index //= 2
			else:
				break

	def del_top_element(self):
		num = len(self.__data) - 1
		if num == 0:
			print("No data in Heap")
		else:
			self.__data[num], self.__data[1] = self.__data[1], self.__data[num]
			del self.__data[-1]
			num -= 1
			heap_up_down(self.__data,num)

	def return_top_data(self):
		return self.__data[1]


# heap up from top to bottom
def heap_up_down(data, num, index=1):
	while (2*index) <= num:

		# both child nodes exist
		if (2*index+1) <= num:
			if data[2*index] > data[index]:
				if data[2*index+1] > data[index]:
					if data[2*index] > data[2*index+1]:
						data[index], data[2*index] = data[2*index], data[index]
						index *= 2
					else:
						data[index], data[2*index+1] = data[2*index+1], data[index]
						index = 2 * index + 1
				else:
					data[index], data[2*index] = data[2*index], data[index]
					index *= 2
			elif data[2*index+1] > data[index]:
				data[index], data[2*index+1] = data[2*index+1], data[index]
				index = 2 * index + 1
			else:
				break

		# only left child node exist
		else:
			if data[2*index] > data[index]:
				data[index], data[2*index] = data[2*index], data[index]
				index *= 2
			else:
				break


def heap_sort(data):
	data.insert(0, None)
	num = len(data) - 1
	pointer = num // 2

	# build heap
	while pointer >= 1:
		heap_up_down(data, num, pointer)
		pointer -= 1

	# sort
	index = num
	for _ in range(num-1):
		data[1], data[index] = data[index], data[1]
		index -= 1
		heap_up_down(data, index)

	del data[0]
