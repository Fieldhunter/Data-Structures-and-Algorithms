import functools


class Node():
	def __init__(self,element):
		self.data = element
		self.in_degree = 0
		self.out_degree = 0


class Adjacency_list():
	"""
		Self.__node_mapping is used to record the correspondence between
		  node and node ordinal number.
		Self.__mapping is used to record the correspondence between node data
		  and node ordinal number.
		In self.__data, using node ordinal number express pointing relationship.
	"""
	def __init__(self):
		self.__data = {}
		self.__node_mapping = []
		self.__mapping = []

	def add_data(self, start, end):
		start, end = str(start), str(end)
		if start not in self.__mapping:
			new_node = Node(start)
			self.__node_mapping.append(new_node)
			self.__mapping.append(start)
			start_num = len(self.__mapping) - 1
		else:
			start_num = self.__mapping.index(start)
		if end not in self.__mapping:
			new_node = Node(end)
			self.__node_mapping.append(new_node)
			self.__mapping.append(end)
			end_num = len(self.__mapping) - 1
		else:
			end_num = self.__mapping.index(end)

		if not self.__data.get(start_num, False):
			new_list = [end_num]
			self.__data[start_num] = new_list
			self.__node_mapping[start_num].out_degree += 1
			self.__node_mapping[end_num].in_degree += 1
		else:
			if end_num in self.__data[start_num]:
				print("data is in list")
			else:
				self.__data[start_num].append(end_num)
				self.__node_mapping[start_num].out_degree += 1
				self.__node_mapping[end_num].in_degree += 1

	def kahn(self):
		"""
			The in_list array records the input degree's numbers of each node.
			The queue array is a queue that stores the node subscripts to be processed.
			The result array is used to store the result order.
		"""
		in_list = []
		for i in self.__node_mapping:
			in_list.append(i.in_degree)
		quene = []
		result = []

		try:
			# find the starting node subscript with 0 in_degree
			pointer = in_list.index(0)
			quene.append(pointer)
			in_list[pointer] = None
		except:
			pass

		while len(quene) != 0:
			pointer = quene[0]
			del quene[0]
			result.append(self.__mapping[pointer])
			if self.__data.get(pointer, False):
				for i in self.__data.get(pointer):
					in_list[i] -= 1

					# set None to the node which has 0 in_degree
					if in_list[i] == 0:
						quene.append(i)
						in_list[i] = None

		"""
			In the end, if not all of them are None in in_list,
			  it means there are ring in the diagram.
		"""
		if in_list.count(None) == len(in_list):
			print(result)
		else:
			print("A ring in map")

	def DFS(self):
		def loop_output(num, result, count):
			count+=1

			"""
				If the function executes' numbers more than the total
				  numbers of nodes, there must be a ring.
			"""
			if count > len(self.__mapping):
				return False

			if inverse_adjacency_list.get(num, False):
				for j in inverse_adjacency_list.get(num):
					result = loop_output(j, result, count)

			if result != False:
				# if this node has not output, then output
				if check_list[num] != True:
					check_list[num] = True
					result.append(self.__mapping[num])

			return result

		"""
			The check_list array is used to determine whether the subscript node
			  has been output.
			The out_list array records the number of out_degree of each node.
			The result array is used to store the result order.
			The count is used to record the execution times of the loop output function.
		"""
		check_list = [False] * len(self.__mapping)
		out_list = []
		result = []
		count = 0
		for i in self.__node_mapping:
			out_list.append(i.out_degree)

		# building a reverse adjacency list
		inverse_adjacency_list = {}
		for i in self.__data:
			if self.__data.get(i, False):
				for j in self.__data.get(i):
					if inverse_adjacency_list.get(j, False):
						inverse_adjacency_list[j].append(i)
					else:
						new_list = [i]
						inverse_adjacency_list[j] = new_list

		try:
			"""
				Find the node with the initial out_degree's value of 0,
				  that is, the end of the original sequence.
			"""
			pointer = out_list.index(0)
			result = loop_output(pointer, result, count)
			if result == False:
				print("A ring in map")
			else:
				print(result)
		except:
			print("A ring in map")

	"""
		Check if the code used to access the class information,Decorator function.
		The purpose of simply adding code is to prevent Adjacency list from 
		  being tampered with maliciously and to provide the API for developers.
	"""
	def __check_code(func):
		@functools.wraps(func)
		def check(self, code):
			if code != 'adsf;{h3096j34ka`fd>&/edgb^45:6':
				raise Exception('code is wrong!')
			result = func(self, code)
			return result

		return check

	@__check_code
	def return_data(self, code):
		return self.__data

	@__check_code
	def return_mapping(self, code):
		return self.__mapping, self.__node_mapping
