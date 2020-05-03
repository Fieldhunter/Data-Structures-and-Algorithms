"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
import functools


"""
	preprocessing operation for adding data in two graph
	  representation methods, decorator function
"""
def start_end_process(func):
	@functools.wraps(func)
	def process(self, start, end):
		start, end = str(start), str(end)
		if start not in self.__mapping:
			self.__mapping.append(start)
			start_num = len(self.__mapping) - 1
		else:
			start_num = self.__mapping.index(start)
		if end not in self.__mapping:
			self.__mapping.append(end)
			end_num = len(self.__mapping) - 1
		else:
			end_num = self.__mapping.index(end)

		func(self, start_num, end_num)
	return process


"""
	Check if the code used to access the graph information,Decorator function.
	The purpose of simply adding code is to prevent graph from 
	  being tampered with maliciously and to provide the API for developers.
"""
def check_code(func):
	@functools.wraps(func)
	def check(self, code):
		if code != 'adsf;{h3096j34ka`fd>&/edgb^45:6':
			raise Exception('code is wrong!')
		result = func(self, code)
		return result

	return check


# based on directed graph
class Adjacency_matrix():
	"""
		Initialize to a matrix of 10 * 10
		Self.__mapping is used to record the correspondence
		  between nodes and their ordinal numbers.
	"""
	def __init__(self):
		self.__mapping = []
		self.__size = 10
		self.__data = []

		for _ in range(10):
			new_list = []
			for _ in range(10):
				new_list.append(0)
			self.__data.append(new_list)

	@start_end_process
	def add_data(self, start_num, end_num):
		self.__data[start_num][end_num] = 1

		"""
			If the number of nodes is close to the size of the matrix,
			  the matrix is expanded.
		"""
		if self.__size - len(self.__mapping) < 2:
			for i in self.__data:
				for _ in range(10):
					i.append(0)
			for _ in range(10):
				new_list = []
				for _ in range(10):
					new_list.append(0)
				self.__data.append(new_list)
			self.__size += 10

	@check_code
	def return_basic_information(self, code):
		return self.__data, self.__mapping, self.__size


class Adjacency_list():
	"""
		Self.__mapping is used to record the correspondence between
		  nodes and their ordinal numbers.
		In self.__data, using node ordinal express pointing relation.
	"""
	def __init__(self):
		self.__data = {}
		self.__mapping = []

	@start_end_process
	def add_data(self, start_num, end_num):
		if not self.__data.get(start_num, False):
			new_list = [end_num]
			self.__data[start_num] = new_list
		else:
			if end_num in self.__data[start_num]:
				print("data is in list")
			else:
				self.__data[start_num].append(end_num)

	def BFS(self, start, end):
		start, end = str(start), str(end)
		if start not in self.__mapping or end not in self.__mapping:
			print("No data in need")
		else:
			"""
				The queue array is a queue to store the currently traversed vertices.
				The visited array is used to record the visited vertices. It is used to
				  avoid repeated access of vertices.
				The prev array is used to record search path.
			"""
			start_num, end_num = self.__mapping.index(start), self.__mapping.index(end)
			queue = [start_num]
			visited = [False] * len(self.__mapping)
			prev = [-1] * len(self.__mapping)
			find = False
			while len(queue) > 0 and find == False:
				focus = queue[0]
				del queue[0]
				visited[focus] = True
				if self.__data.get(focus, False):
					for i in self.__data[focus]:
						if visited[i] != True:
							queue.append(i)
							prev[i] = focus
							if i == end_num:
								find = True
								break

			if find:
				pointer = end_num
				prev_way = []
				while pointer != -1:
					prev_way.insert(0, pointer)
					pointer = prev[pointer]
				print(prev_way)
			else:
				print("No way from start to end")

	def DFS(self, start, end):
		def recursion_found(pointer, end_num, visited, prev, find):
			if find == True:
				return visited, prev, find

			if self.__data.get(pointer, False):
				for i in self.__data[pointer]:
					if find:
						break
					if visited[i] != True:
						visited[i] = True
						prev[i] = pointer
						if i == end_num:
							find = True
							break
						visited, prev, find = recursion_found(i, end_num, visited, prev, find)

			return visited, prev, find

		start, end = str(start), str(end)
		if start not in self.__mapping or end not in self.__mapping:
			print("No data in need")
		else:
			# visited, prev array has the same function as BFS
			start_num, end_num = self.__mapping.index(start), self.__mapping.index(end)
			visited = [False] * len(self.__mapping)
			prev = [-1] * len(self.__mapping)
			find = False
			pointer = start_num
			visited[start_num] = True
			visited, prev, find = recursion_found(pointer, end_num, visited, prev, find)

			if find:
				index = end_num
				prev_way = []
				while index != -1:
					prev_way.insert(0, index)
					index = prev[index]
				print(prev_way)
			else:
				print("No way from start to end")

	@check_code
	def return_basic_information(self, code):
		return self.__data, self.__mapping
