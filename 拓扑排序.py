import functools


class Node():
	# in_degree表示入度数，out_degree表示出度数
	def __init__(self,element):
		self.data = element
		self.in_degree = 0
		self.out_degree = 0


# 邻接表
class Adjacency_list():
	"""
		__node_mapping用来记录节点与节点序数的对应关系
		__mapping用来记录节点数据与节点序数的对应关系
		__data中用节点序数来表示指向关系
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
		# in_list记录每个节点的入度数,queue是一个队列，用来存储待处理的节点下标,result用来存储结果顺序
		in_list = []
		for i in self.__node_mapping:
			in_list.append(i.in_degree)
		quene = []
		result = []

		try:
			# 找到入度为0的初始节点下标
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

					# 入度为0的节点设置为None
					if in_list[i] == 0:
						quene.append(i)
						in_list[i] = None

		# 如果最终in_list里不全是None，说明有环
		if in_list.count(None) == len(in_list):
			print(result)
		else:
			print("A ring in map")

	def DFS(self):
		# 循环输出
		def loop_output(num, result, count):
			count+=1

			# 如果函数执行次数超过了总的节点数，说明肯定存在环
			if count > len(self.__mapping):
				return False

			if inverse_adjacency_list.get(num, False):
				for j in inverse_adjacency_list.get(num):
					result = loop_output(j, result, count)

			if result != False:
				# 该节点如果没有输出过，则输出
				if check_list[num] != True:
					check_list[num] = True
					result.append(self.__mapping[num])

			return result

		"""
			check_list数组用来判断该下标的节点有没有输出过
			out_list记录每个节点的出度数
			result用来存储结果顺序
			count用来记录循环输出函数的执行次数
		"""
		check_list = [False] * len(self.__mapping)
		out_list = []
		result = []
		count = 0
		for i in self.__node_mapping:
			out_list.append(i.out_degree)

		# 构建逆邻接表
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
			# 找到出度数初始值为0的节点，即原顺序的末尾
			pointer = out_list.index(0)
			result = loop_output(pointer, result, count)
			if result == False:
				print("A ring in map")
			else:
				print(result)
		except:
			print("A ring in map")

	"""
		用于检查访问类基本信息的code是否正确，装饰器函数
		简单加入code目的是防止邻接表被恶意篡改，并留个接口给开发人员
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
