import functools


"""
	该散列表存储的是字符串格式数据，装载因子设置为0.2~0.8，利用链表法解决散列冲突
	散列函数为计算字符串上每个位置的Unicode码之和，之后求平均值并和散列表大小取余
"""
class link_Node():
	def __init__(self, num):
		self.data = num
		self.next = None


class Linked_list():
	def __init__(self):
		self.head = None
		self.num = 0


class Hash_table():
	"""
		size是散列表的大小，默认为10，num是已有的数据个数
		min_size不扩容时不更新，用于动态缩容时散列表最小大小
		stowage是装载因子,expansion代表散列表是否正在扩容,new_table存储新散列表
		扩容策略为当要扩容时，单单申请，不转移数据，当要增加一个数据时，
		将新数据和原散列表中的几个数据加入到新散列表
		expansion_pos代表扩容时原散列表遍历到的位置，目的是方便删除和查找操作
	"""
	def __init__(self, size=10):
		self.__min_size = size
		self.__size = size
		self.__num = 0
		self.__expansion = False
		self.__expansion_pos = 0
		self.__new_table = None
		self.__stowage = self.__num / self.__size
		self.__data = []
		for _ in range(size):
			self.__data.append(None)

	# 用于检查输入数据是否合法，装饰器函数
	def __check_data_format(func):
		@functools.wraps(func)
		def check(self, data):
			if type(data) != type("1"):
				data = str(data)
			func(self, data)

		return check

	"""
		用于检查访问self.__data或self.__new_table的code是否正确，装饰器函数
		简单加入code目的是防止hash table被恶意篡改，并留个接口给开发人员
	"""
	def __check_code(func):
		@functools.wraps(func)
		def check(self, code):
			if code != 'adsf;{h3096j34ka`fd>&/edgb^45:6':
				raise Exception('code is wrong!')
			result = func(self, code)
			return result

		return check

	def __hash_function(self, data):
		num = 0
		sumer = 0
		for i in data:
			num += 1
			sumer += ord(i)
		sumer //= num
		sumer %= self.__size

		return sumer

	def __old_data_move(self):
		# 将老数据加入到新散列表,一次性最多搬3个
		for _ in range(3):
			while self.__expansion_pos != len(self.__data) and\
				  self.__data[self.__expansion_pos] == None:
				self.__expansion_pos += 1

			# 判断是否原散列表数据已经搬移完，如果已经搬移完了，就把新的散列表更新到原散列表	
			if self.__expansion_pos == len(self.__data):
				self.__expansion = False
				self.__size = self.__new_table.__size
				self.__num = self.__new_table.__num
				self.__stowage = self.__new_table.__stowage
				self.__data = self.__new_table.__data
				self.__new_table = None
				self.__expansion_pos = 0
				break
			else:
				# 对原散列表链表处理
				old_data = self.__data[self.__expansion_pos].head
				self.__data[self.__expansion_pos].head = \
						self.__data[self.__expansion_pos].head.next
				self.__data[self.__expansion_pos].num -= 1
				if self.__data[self.__expansion_pos].head == None:
					self.__data[self.__expansion_pos] = None

				old_hash_value = self.__new_table.__hash_function(old_data.data)
				if self.__new_table.__data[old_hash_value] == None:
					link_list = Linked_list()
					self.__new_table.__data[old_hash_value] = link_list
				else:
					link_list = self.__new_table.__data[old_hash_value]

				old_data.next = link_list.head
				link_list.head = old_data
				link_list.num += 1
				self.__num -= 1
				self.__new_table.__num += 1
				self.__new_table.__stowage = self.__new_table.__num / self.__new_table.__size

	@__check_data_format
	def add_data(self, data):
		new_node = link_Node(data)

		if self.__expansion == False:
			hash_value = self.__hash_function(data)
			if self.__data[hash_value] == None:
				link_list = Linked_list()
				self.__data[hash_value] = link_list
			else:
				link_list = self.__data[hash_value]

			new_node.next = link_list.head
			link_list.head = new_node
			link_list.num += 1
			self.__num += 1
			self.__stowage = self.__num / self.__size

			# 动态扩容
			if self.__stowage > 0.8:
				self.__expansion = True
				new_hash_table = Hash_table(self.__size*2)
				self.__new_table = new_hash_table
				self.__old_data_move()
		# 扩容中
		else:
			# 先将新数据加入
			hash_value = self.__new_table.__hash_function(data)
			if self.__new_table.__data[hash_value] == None:
				link_list = Linked_list()
				self.__new_table.__data[hash_value] = link_list
			else:
				link_list = self.__new_table.__data[hash_value]

			new_node.next = link_list.head
			link_list.head = new_node
			link_list.num += 1
			self.__new_table.__num += 1
			self.__new_table.__stowage = self.__new_table.__num / self.__new_table.__size
			
			self.__old_data_move()

	@__check_data_format
	def del_data(self, data):
		hash_value = self.__hash_function(data)
		find = False

		# 先在原散列表中找
		if self.__data[hash_value] == None:
			pass
		else:
			pointer = self.__data[hash_value].head
			while pointer != None:
				if pointer.data == data:
					find = True
					break
				else:
					prev_pointer = pointer
					pointer = pointer.next

		if find:
			print("Successful del data")
			try:
				prev_pointer.next = pointer.next
			except:
				self.__data[hash_value].head = pointer.next

			self.__data[hash_value].num -= 1
			if self.__data[hash_value].num == 0:
				self.__data[hash_value] = None
			self.__num -= 1
			self.__stowage = self.__num / self.__size

		# 判断是否正在扩容
		elif self.__expansion == True:
			hash_value = self.__new_table.__hash_function(data)
			if self.__new_table.__data[hash_value] == None:
				pass
			else:
				pointer = self.__new_table.__data[hash_value].head
				while pointer != None:
					if pointer.data == data:
						find = True
						break
					else:
						prev_pointer = pointer
						pointer = pointer.next

			if find:
				print("Successful del data in new_Hash_table")
				try:
					prev_pointer.next = pointer.next
				except:
					self.__new_table.__data[hash_value].head = pointer.next

				self.__new_table.__data[hash_value].num -= 1
				if self.__new_table.__data[hash_value].num == 0:
					self.__new_table.__data[hash_value] = None
				self.__new_table.__num -= 1
				self.__new_table.__stowage = self.__new_table.__num / self.__new_table.__size
			else:
				print("No data in two Hash_table")
		else:
			print("No data in Hash_table")

		# 如果删除成功并处于扩容状态，那么进行数据搬移操作
		if find and self.__expansion == True:
			self.__old_data_move()

		# 动态缩容
		if self.__stowage < 0.2 and \
		   self.__size > self.__min_size and self.__expansion == False:

			new_table = Hash_table(self.__size//2)
			while len(self.__data) > 0:
				if self.__data[0] == None or self.__data[0].head == None:
					del self.__data[0]
					continue
				else:
					pointer = self.__data[0].head
					while pointer != None:
						new_table.add_data(pointer.data)
						pointer = pointer.next
						self.__data[0].head = pointer

			self.__data = new_table.__data
			self.__size = new_table.__size
			self.__stowage = self.__num / self.__size

	@__check_data_format
	def find_data(self, data):
		hash_value = self.__hash_function(data)
		find = False

		if self.__data[hash_value] == None:
			pass
		else:
			pointer = self.__data[hash_value].head
			while pointer != None:
				if pointer.data == data:
					find = True
					break
				else:
					prev_pointer = pointer
					pointer = pointer.next

		if find:
			print("Find data in Hash_table")
		elif self.__expansion == True:
			hash_value = self.__new_table.__hash_function(data)
			if self.__new_table.__data[hash_value] == None:
				pass
			else:
				pointer = self.__new_table.__data[hash_value].head
				while pointer != None:
					if pointer.data == data:
						find = True
						break
					else:
						prev_pointer = pointer
						pointer = pointer.next

			if find:
				print("Find data in new_Hash_table")
			else:
				print("No data in need")
		else:
			print("No data in need")

	def return_basic_information(self):
		return self.__min_size, self.__size, self.__num, \
			self.__expansion, self.__expansion_pos, self.__stowage

	@__check_code
	def return_hash_data(self, code):
		return self.__data

	@__check_code
	def return_hash_expansion_table(self, code):
		return self.__new_table
