import functools


class Dijkstra_Node():
	# value用来存储该节点与指向节点之间的权值
	def __init__(self, element):
		self.data = element
		self.value = []


# 实现一个小顶堆,用于后续的dijkstra的优先级队列
class Heap():
	def __init__(self):
		self.data = [None]

	"""
		小顶堆存储的是一个元组，元组有两个值，第一个是节点在邻接表中对应的下标
		第二个是该节点在dijkstra算法中与起始节点的距离，即后面vertexes数组中该节点下标的值
		小顶堆以第二个值进行堆化
	"""
	def add_data(self, element):
		self.data.append(element)
		index = len(self.data) - 1
		while index > 1:
			if self.data[index][1] < self.data[index//2][1]:
				self.data[index], self.data[index//2] = \
					self.data[index//2], self.data[index]
				index //= 2
			else:
				break

	def get_top_element(self):
		num = len(self.data) - 1
		self.data[num], self.data[1] = self.data[1], self.data[num]

		# 取得堆顶元素时，只返回节点在邻接表中对应的下标
		top_element = self.data[-1][0]
		del self.data[-1]
		num -= 1
		self.__heap_up_down(self.data, num)

		return top_element

	# 从上往下进行堆化
	def __heap_up_down(self, data, num, index=1):
		while (2*index) <= num:

			# 两个子节点都存在
			if (2*index+1) <= num:
				if data[2*index][1] <= data[index][1]:
					if data[2*index+1][1] < data[index][1]:
						if data[2*index][1] < data[2*index+1][1]:
							data[index], data[2*index] = data[2*index], data[index]
							index *= 2
						else:
							data[index], data[2*index+1] = data[2*index+1], data[index]
							index = 2 * index + 1
					else:
						data[index], data[2*index] = data[2*index], data[index]
						index *= 2
				elif data[2*index+1][1] < data[index][1]:
					data[index], data[2*index+1] = data[2*index+1], data[index]
					index = 2 * index + 1
				else:
					break

			# 只存在左节点
			else:
				if data[2*index][1] <= data[index][1]:
					data[index], data[2*index] = data[2*index], data[index]
					index *= 2
				else:
					break


# 邻接表
class Adjacency_list():
	"""
		__mapping用来记录及节点的值与节点序数的对应关系
		__data中用节点序数来表示指向关系
		__node_mapping用来存储节点与节点序数的对应关系
	"""
	def __init__(self):
		self.__data = {}
		self.__node_mapping = []
		self.__mapping = []

	def add_data(self, start, end, weight):
		start, end = str(start), str(end)
		if start not in self.__mapping:
			new_node = Dijkstra_Node(start)
			self.__node_mapping.append(new_node)
			self.__mapping.append(start)
			start_num = len(self.__mapping) - 1
		else:
			start_num = self.__mapping.index(start)
		if end not in self.__mapping:
			new_node = Dijkstra_Node(end)
			self.__node_mapping.append(new_node)
			self.__mapping.append(end)
			end_num = len(self.__mapping) - 1
		else:
			end_num = self.__mapping.index(end)

		if not self.__data.get(start_num, False):
			new_list = [end_num]
			self.__data[start_num] = new_list
			self.__node_mapping[start_num].value.append(weight)
		else:
			# 如果起始节点与结束节点已经有对应关系了，那么就更新他们两个的之间的权值
			if end_num in self.__data[start_num]:
				pointer = self.__data[start_num].index(end_num)
				self.__node_mapping[start_num].value[pointer] = weight
			else:
				self.__data[start_num].append(end_num)
				self.__node_mapping[start_num].value.append(weight)

	# Dijkstra算法
	def dijkstra(self, start, end):
		start,end = str(start),str(end)

		if start not in self.__mapping or end not in self.__mapping:
			print("No target data in map")
		else:
			"""
				初始化部分:
					vertexes数组用来存储某个下标节点与起始节点的距离，记作dist，None表示无穷大
					predecessor数组用来存储每个节点的前驱节点，用于输出路径
					inqueue数组是为了避免将一个顶点多次添加到优先级队列中
					level_queue为优先级队列
			"""
			start_num, end_num = self.__mapping.index(start), self.__mapping.index(end)
			vertexes = [None] * len(self.__mapping)
			predecessor = [-1] * len(self.__mapping)
			inqueue = [False] * len(self.__mapping)
			level_queue = Heap()
			find = False

			# 对起始节点先进行处理，放入优先级队列中
			vertexes[start_num] = 0
			level_queue.add_data((start_num, vertexes[start_num]))
			inqueue[start_num] = True

			while len(level_queue.data) > 1:
				# 取出一个与起始节点距离最短的节点
				minvertex = level_queue.get_top_element()

				# 如果结束节点出队列，说明找到了最短路径，则退出循环
				if minvertex == end_num:
					find = True
					break

				if self.__data.get(minvertex, False):
					# 遍历minvertex的出度节点
					for num, i in enumerate(self.__data.get(minvertex)):
						if vertexes[i] == None or vertexes[minvertex] + \
							self.__node_mapping[minvertex].value[num] < vertexes[i]:

							"""
								如果minVertex的dist值加上两节点之间的权重小于该出度节点的dist值
								或者出度节点的dist值为None，则对出度节点的dist值进行更新
								同时前驱节点进行更新
							"""
							vertexes[i] = vertexes[minvertex] + \
								self.__node_mapping[minvertex].value[num]
							predecessor[i] = minvertex

							# 判断该出度节点是否之前已经加入到优先级队列中，如果没有，则加入
							if inqueue[i] == False:
								level_queue.add_data((i, vertexes[i]))
								inqueue[i] = True

			# 找到路径，则遍历predecess数组输出
			if find:
				pointer = predecessor[end_num]
				result = [self.__mapping[end_num]]

				while pointer != -1:
					result.insert(0, self.__mapping[pointer])
					pointer = predecessor[pointer]

				print(result)
			else:
				print("No way from start to end")

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
