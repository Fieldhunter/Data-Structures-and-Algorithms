"""
	该散列表存储的是字符串格式数据，装载因子设置为0.2~0.8，利用链表法解决散列冲突
	散列函数为计算字符串上每个位置的Unicode码之和，之后求平均值并和散列表大小取余
"""
class Node():
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
		self.min_size = size
		self.size = size
		self.num = 0
		self.expansion = False
		self.expansion_pos = 0
		self.new_table = None
		self.stowage = self.num / self.size
		self.data = []
		for _ in range(size):
			self.data.append(None)

	def hash_function(self, data):
		num = 0
		sumer = 0
		for i in data:
			num += 1
			sumer += ord(i)
		sumer //= num
		sumer %= self.size

		return sumer

	def old_data_move(self):
		# 将老数据加入到新散列表,一次性最多搬3个
		for _ in range(3):
			while self.expansion_pos != len(self.data) and\
				  self.data[self.expansion_pos] == None:
				self.expansion_pos += 1

			# 判断是否原散列表数据已经搬移完，如果已经搬移完了，就把新的散列表更新到原散列表	
			if self.expansion_pos == len(self.data):
				self.expansion = False
				self.size = self.new_table.size
				self.num = self.new_table.num
				self.stowage = self.new_table.stowage
				self.data = self.new_table.data
				self.new_table = None
				self.expansion_pos = 0
				break
			else:
				# 对原散列表链表处理
				old_data = self.data[self.expansion_pos].head
				self.data[self.expansion_pos].head = \
						self.data[self.expansion_pos].head.next
				self.data[self.expansion_pos].num -= 1
				if self.data[self.expansion_pos].head == None:
					self.data[self.expansion_pos] = None

				old_hash_value = self.new_table.hash_function(old_data.data)
				if self.new_table.data[old_hash_value] == None:
					link_list = Linked_list()
					self.new_table.data[old_hash_value] = link_list
				else:
					link_list = self.new_table.data[old_hash_value]

				old_data.next = link_list.head
				link_list.head = old_data
				link_list.num += 1
				self.num -= 1
				self.new_table.num += 1
				self.new_table.stowage = self.new_table.num / self.new_table.size

	def add_data(self, data):
		if type(data) != type("1"):
			data = str(data)
		new_node = Node(data)

		if self.expansion == False:
			hash_value = self.hash_function(data)
			if self.data[hash_value] == None:
				link_list = Linked_list()
				self.data[hash_value] = link_list
			else:
				link_list = self.data[hash_value]

			new_node.next = link_list.head
			link_list.head = new_node
			link_list.num += 1
			self.num += 1
			self.stowage = self.num / self.size

			# 动态扩容
			if self.stowage > 0.8:
				self.expansion = True
				new_hash_table = Hash_table(self.size*2)
				self.new_table = new_hash_table
				self.old_data_move()
		# 扩容中
		else:
			# 先将新数据加入
			hash_value = self.new_table.hash_function(data)
			if self.new_table.data[hash_value] == None:
				link_list = Linked_list()
				self.new_table.data[hash_value] = link_list
			else:
				link_list = self.new_table.data[hash_value]

			new_node.next = link_list.head
			link_list.head = new_node
			link_list.num += 1
			self.new_table.num += 1
			self.new_table.stowage = self.new_table.num / self.new_table.size
			
			self.old_data_move()

	def del_data(self, data):
		if type(data) != type("1"):
			data = str(data)
		hash_value = self.hash_function(data)
		find = False

		# 先在原散列表中找
		if self.data[hash_value] == None:
			pass
		else:
			pointer = self.data[hash_value].head
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
				self.data[hash_value].head = pointer.next

			self.data[hash_value].num -= 1
			if self.data[hash_value].num == 0:
				self.data[hash_value] = None
			self.num -= 1
			self.stowage = self.num / self.size

		# 判断是否正在扩容
		elif self.expansion == True:
			hash_value = self.new_table.hash_function(data)
			if self.new_table.data[hash_value] == None:
				pass
			else:
				pointer = self.new_table.data[hash_value].head
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
					self.new_table.data[hash_value].head = pointer.next

				self.new_table.data[hash_value].num -= 1
				if self.new_table.data[hash_value].num == 0:
					self.new_table.data[hash_value] = None
				self.new_table.num -= 1
				self.new_table.stowage = self.new_table.num / self.new_table.size
			else:
				print("No data in two Hash_table")
		else:
			print("No data in Hash_table")

		# 如果删除成功并处于扩容状态，那么进行数据搬移操作
		if find and self.expansion == True:
			self.old_data_move()

		# 动态缩容
		if self.stowage < 0.2 and \
		   self.size > self.min_size and self.expansion == False:

			new_table = Hash_table(self.size//2)
			while len(self.data) > 0:
				if self.data[0] == None or self.data[0].head == None:
					del self.data[0]
					continue
				else:
					pointer = self.data[0].head
					while pointer != None:
						new_table.add_data(pointer.data)
						pointer = pointer.next
						self.data[0].head = pointer

			self.data = new_table.data
			self.size = new_table.size
			self.stowage = self.num / self.size


	def find_data(self, data):
		if type(data) != type("1"):
			data = str(data)
		hash_value = self.hash_function(data)
		find = False

		if self.data[hash_value] == None:
			pass
		else:
			pointer = self.data[hash_value].head
			while pointer != None:
				if pointer.data == data:
					find = True
					break
				else:
					prev_pointer = pointer
					pointer = pointer.next

		if find:
			print("Find data in Hash_table")
		elif self.expansion == True:
			hash_value = self.new_table.hash_function(data)
			if self.new_table.data[hash_value] == None:
				pass
			else:
				pointer = self.new_table.data[hash_value].head
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
