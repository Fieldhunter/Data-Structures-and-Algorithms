import functools


class link_Node():
	"""
		next列表表示该节点指向的节点，不同位置的节点表示索引中不同层数指向的位置
		0号位是链表本身，1号位是第一层索引，以此类推，后面跳表实现阶段会初始化和更新
	"""
	def __init__(self, data):
		self.data = data
		self.next = []


class Skip_list():
	def __init__(self):
		self.__head = None
		self.__add_num = 0
		self.__del_num = 0
		self.__num = 0

	def __index(self):
		# 计算索引的层数
		num = self.__num
		max_level = 0
		while num > 3:
			max_level += 1
			num //= 3

		# 为每个节点的next列表初始化
		pointer = self.__head
		while pointer:

			# 索引层数增加
			if len(pointer.next) - 1 < max_level:
				for _ in range(max_level - (len(pointer.next)-1)):
					pointer.next.append(None)

			# 索引层数减少
			elif len(pointer.next) - 1 > max_level:	
				del pointer.next[-(len(pointer.next)-1-max_level) : ]
			pointer = pointer.next[0]

		# 更新构建索引的节点的next列表
		for i in range(max_level):
			pointer = self.__head
			while pointer:
				try:
					next_pointer = pointer.next[i].next[i].next[i]
					pointer.next[i+1] = next_pointer
					pointer = next_pointer
				except:
					# 处理这一层索引最后一个节点
					pointer.next[i+1] = None
					break

	# 加入数据，使链表保持由小到大的顺序
	def add_data(self, element):
		new_data = link_Node(element)
		self.__num += 1
		self.__add_num += 1

		if self.__head == None or new_data.data <= self.__head.data:
			new_data.next.append(self.__head)
			self.__head = new_data
		else:
			pointer = self.__head
			for i in range(len(self.__head.next), 0, -1):
				while pointer.next[i-1] != None:
					if new_data.data <= pointer.next[i-1].data:
						break
					else:
						pointer = pointer.next[i-1]

			new_data.next.append(pointer.next[0])
			pointer.next[0] = new_data

		# 每加入三个数据更新一遍索引
		if self.__add_num == 3:
			self.__index()
			self.__add_num = 0

	def del_data(self, num):
		if self.__head == None:
			print("No data in Skip_list")
		elif self.__head.data == num:
			self.__head = self.__head.next[0]
			self.__num -= 1
			self.__index()
		else:
			prev_pointer = self.__head
			find = False

			for i in range(len(self.__head.next), 0, -1):
				if not find:
					pointer = prev_pointer.next[i-1]

				while pointer != None:
					if pointer.data == num:
						# 更新前指针，保证两指针的前后关系
						while prev_pointer.next[i-1] != pointer:	
							prev_pointer = prev_pointer.next[i-1]

						prev_pointer.next[i-1] = pointer.next[i-1]
						find = True
						break
					elif pointer.data < num:
						prev_pointer = prev_pointer.next[i-1]
						pointer = pointer.next[i-1]
					else:
						break

			if find:
				self.__num -= 1
				self.__del_num += 1
			else:
				print("No data in Skip_list")

			# 每删除三个数据更新一遍索引，删除头结点不算
			if self.__del_num == 3:
				self.__index()
				self.__del_num = 0

	def find_data(self, num):
		if self.__head == None:
			print("No data in Skip_list")
		else:
			find = False
			pointer = self.__head
			for i in range(len(self.__head.next), 0, -1):
				if find:
					break
				while pointer.next[i-1] != None:
					if pointer.data == num:
						find = True
						break
					elif pointer.next[i-1].data <= num:
						pointer = pointer.next[i-1]
					else:
						break

			if find:
				print("Find your data")
			else:
				print("No this data in Skip_list")

	"""
		用于检查访问类基本信息的code是否正确，装饰器函数
		简单加入code目的是防止跳表被恶意篡改，并留个接口给开发人员
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
	def return_head(self, code):
		return self.__head

	@__check_code
	def return_num(self, code):
		return self.__num, self.__add_num, self.__del_num
