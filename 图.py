# 基于有向图
class Adjacency_matrix():
	# 初始化为一个10*10的矩阵,mapping用来记录节点与节点序数的对应关系
	def __init__(self):
		self.mapping = []
		self.size = 10
		self.data = []

		for _ in range(10):
			new_list = []
			for _ in range(10):
				new_list.append(0)
			self.data.append(new_list)

	def add_data(self, start, end):
		start, end = str(start), str(end)
		if start not in self.mapping:
			self.mapping.append(start)
			start_num = len(self.mapping) - 1
		else:
			start_num = self.mapping.index(start)
		if end not in self.mapping:
			self.mapping.append(end)
			end_num = len(self.mapping) - 1
		else:
			end_num = self.mapping.index(end)
		self.data[start_num][end_num] = 1

		# 如果节点个数接近矩阵的尺寸，则对矩阵进行扩容
		if self.size - len(self.mapping) < 2:
			for i in self.data:
				for _ in range(10):
					i.append(0)
			for _ in range(10):
				new_list = []
				for _ in range(10):
					new_list.append(0)
				self.data.append(new_list)
			self.size += 10


# 邻接表
class Adjacency_list():
	# mapping用来记录节点与节点序数的对应关系,data中用节点序数来表示指向关系
	def __init__(self):
		self.data = {}
		self.mapping = []

	def add_data(self, start, end):
		start, end = str(start), str(end)
		if start not in self.mapping:
			self.mapping.append(start)
			start_num = len(self.mapping) - 1
		else:
			start_num = self.mapping.index(start)
		if end not in self.mapping:
			self.mapping.append(end)
			end_num = len(self.mapping) - 1
		else:
			end_num = self.mapping.index(end)
		if not self.data.get(start_num, False):
			new_list = [end_num]
			self.data[start_num] = new_list
		else:
			if end_num in self.data[start_num]:
				print("data is in list")
			else:
				self.data[start_num].append(end_num)

	def BFS(self, start, end):
		start, end = str(start), str(end)
		if start not in self.mapping or end not in self.mapping:
			print("No data in need")
		else:
			"""
				queue为一个队列，用来存储当前遍历到的顶点
				visited数组用来记录已经被访问的顶点.用来避免顶点被重复访问
				prev数组用来记录搜素路径
			"""
			start_num, end_num = self.mapping.index(start), self.mapping.index(end)
			queue = [start_num]
			visited = [False] * len(self.mapping)
			prev = [-1] * len(self.mapping)
			find = False
			while len(queue) > 0 and find == False:
				focus = queue[0]
				del queue[0]
				visited[focus] = True
				if self.data.get(focus, False):
					for i in self.data[focus]:
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
		# 递归查找
		def recursion_found(pointer, end_num, visited, prev, find):
			if find == True:
				return visited, prev, find

			if self.data.get(pointer, False):
				for i in self.data[pointer]:
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
		if start not in self.mapping or end not in self.mapping:
			print("No data in need")
		else:
			# visited，prev数组作用与BFS相同
			start_num, end_num = self.mapping.index(start), self.mapping.index(end)
			visited = [False] * len(self.mapping)
			prev = [-1] * len(self.mapping)
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
