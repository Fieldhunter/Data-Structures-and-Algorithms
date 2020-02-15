import functools


class A_Node():
	# value用来存储该节点与指向节点之间的权值,x，y属性存储该节点的x，y值
	def __init__(self, element, x_way, y_way):	
		self.data = element
		self.value = []
		self.x = x_way
		self.y = y_way


# 实现一个小顶堆,小顶堆用于后续的A*算法的优先级队列
class Heap():
	def __init__(self):
		self.data = [None]

	"""
		小顶堆存储的是一个元组，元组有两个值，第一个是节点在邻接表中对应的下标
		第二个是该节点在A*算法中judge数组中的值
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
		__mapping用来记录节点的值与节点序数的对应关系
		__data中用节点序数来表示指向关系
		__node_mapping用来存储节点与节点序数的对应关系
	"""
	def __init__(self):
		self.__data = {}
		self.__node_mapping = []
		self.__mapping = []

	def add_data(self, start, start_x, start_y, end, end_x, end_y, weight):
		start, end = str(start), str(end)
		if start not in self.__mapping:
			new_node = A_Node(start, start_x, start_y)
			self.__node_mapping.append(new_node)
			self.__mapping.append(start)
			start_num = len(self.__mapping) - 1
		else:
			# 如果起始节点已经存在，则不更新起始节点的坐标值，结束节点同理
			start_num = self.__mapping.index(start)

		if end not in self.__mapping:
			new_node = A_Node(end, end_x, end_y)
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

	# A#算法
	def a(self, start, end):
		# 计算曼哈顿距离
		def manhattan(start_num, end_num):
			start_x, start_y = \
				self.__node_mapping[start_num].x, self.__node_mapping[start_num].y
			end_x , end_y = self.__node_mapping[end_num].x, self.__node_mapping[end_num].y
			manhattan_dist = abs(start_x-end_x) + abs(start_y-end_y)

			return manhattan_dist

		start,end = str(start), str(end)
		if start not in self.__mapping or end not in self.__mapping:
			print("No target data in map")
		else:
			"""
				初始化部分:
					vertexes数组用来存储某个下标节点与起始节点的距离，记作g(i)，None表示无穷大
					judge数组用来存储某个下标节点与结束节点的曼哈顿距离（记作h(i)）
						与对应下标的vertexes数组中的值之和，记作f(i)，None表示无穷大
					predecessor数组用来存储每个节点的前驱节点，用于输出路径
					inqueue数组是为了避免将一个顶点多次添加到优先级队列中
					level_queue为优先级队列
			"""
			start_num, end_num = self.__mapping.index(start), self.__mapping.index(end)
			vertexes = [None] * len(self.__mapping)
			judge = [None] * len(self.__mapping)
			predecessor = [-1] * len(self.__mapping)
			inqueue = [False] * len(self.__mapping)
			level_queue = Heap()
			find = False

			# 对起始节点先进行处理，放入优先级队列中
			vertexes[start_num] = 0
			judge[start_num] = manhattan(start_num, end_num)
			level_queue.add_data((start_num, judge[start_num]))
			inqueue[start_num] = True

			while len(level_queue.data) > 1 and find == False:
				# 取出一个judge值最短的节点
				minvertex = level_queue.get_top_element()

				if self.__data.get(minvertex,False):
					# 遍历minvertex的出度节点
					for num, i in enumerate(self.__data.get(minvertex)):
						"""
							judge数组记录的是f(i)，而f(i)=g(i)+h(i)，
							h(i)即曼哈顿距离，一个节点的曼哈顿距离是不变的
							所以A*算法中f(i)的比较也就是g(i)的比较，此处判断就是这个道理
							如果minVertex的g(i)值加上两节点之间的权重小于该出度节点的g(i)值
							或者出度节点的g(i)值为None，则对出度节点的g(i)值进行更新
						"""
						if vertexes[i] == None or \
							(vertexes[minvertex] + self.__node_mapping[minvertex].value[num])\
								< vertexes[i]:

							# 同时更新judge数组，即f(i)值,以及前驱节点
							vertexes[i] = \
								vertexes[minvertex] + self.__node_mapping[minvertex].value[num]
							judge[i] = vertexes[i] + manhattan(i, end_num)
							predecessor[i] = minvertex

							# 判断该出度节点是否之前已经加入到优先级队列中，如果没有，则加入
							if inqueue[i] == False:
								level_queue.add_data((i, judge[i]))
								inqueue[i] = True

							# 如果遍历到结束节点，则退出循环
							if i == end_num:
								find = True
								break

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
