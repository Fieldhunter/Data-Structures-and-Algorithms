import functools


"""
	该二叉搜索树中，左子树中的每个节点的值，都要小于等于这个节点的值
	而右子树节点的值都大于这个节点的值
"""
class tree_Node():
	def __init__(self, num):
		self.data = num
		self.left = None
		self.right = None


class Binary_search_tree():
	"""
		__left_num和__right_num用来记录根节点左右两树节点个数情况
		用于适当进行左右旋(借鉴红黑树)，以尽量提高各操作效率
	"""
	def __init__(self):
		self.__head = None
		self.__left_num = 0
		self.__right_num = 0

	# 左旋
	def __left_rotate(self):
		while self.__left_num < self.__right_num:
			focus_node = self.__head
			right_node = self.__head.right
			right_node_son = right_node.left

			focus_node.right = right_node_son
			right_node.left = focus_node
			self.__head = right_node

			if right_node_son == None:
				self.__left_num += 1
				self.__right_num -= 1
			else:
				self.__left_num += 2
				self.__right_num -= 2

	# 右旋
	def __right_rotate(self):
		while self.__right_num < self.__left_num:
			focus_node = self.__head
			left_node = self.__head.left
			left_node_son = left_node.right

			focus_node.left = left_node_son
			left_node.right = focus_node
			self.__head = left_node

			if left_node_son == None:
				self.__left_num -= 1
				self.__right_num += 1
			else:
				self.__left_num -= 2
				self.__right_num += 2

	def add_data(self, element):
		new_node = tree_Node(element)
		if self.__head == None:
			self.__head = new_node
		else:
			pointer = self.__head
			if element > self.__head.data:
				self.__right_num += 1
			else:
				self.__left_num += 1

			while pointer != None:
				prev_pointer = pointer
				if element > pointer.data:
					pointer = pointer.right
					pos = "right"
				else:
					pointer = pointer.left
					pos = "left"

			if pos == "right":
				prev_pointer.right = new_node
			else:
				prev_pointer.left = new_node

		# 两子树个数相差5个时候，进行左右旋
		if self.__left_num - self.__right_num == 5:
			self.__right_rotate()
		elif self.__right_num - self.__left_num == 5:
			self.__left_rotate()

	def del_data(self, element):
		prev_pointer = None
		pos = None
		pointer = self.__head
		find = False

		# 方便减少根节点左右子树节点个数
		if pointer != None:
			if pointer.data < element:
				direction = "right"
			else:
				direction = "left"

		while pointer != None and find == False:
			if pointer.data == element:
				find = True
			else:
				prev_pointer = pointer
				if pointer.data < element:
					pointer = pointer.right
					pos = "right"
				else:
					pointer = pointer.left
					pos = "left"
		
		if find:
			if pointer != self.__head:
				if direction == "right":
					self.__right_num -= 1
				else:
					self.__left_num -= 1
			elif pointer.right != None:
				self.__right_num -= 1
			elif pointer.left != None:
				self.__left_num -= 1

			# 因为删除第二步中有重复使用第二步的操作，所以将第二步单独拎出来
			self.__del_step(prev_pointer, pointer, pos)

			print("Successful to del data")
		else:
			print("No data in need")

		# 两子树个数相差5个时候，进行左右旋
		if self.__left_num - self.__right_num == 5:
			self.__right_rotate()
		elif self.__right_num - self.__left_num == 5:
			self.__left_rotate()

	def __del_step(self, prev_pointer, pointer, pos):
		# 要删除的节点没有子节点的情况
		if pointer.left == None and pointer.right == None:
			if pointer == self.__head:
				self.__head == None
			else:
				if pos == "right":
					prev_pointer.right = None
				else:
					prev_pointer.left = None

		# 要删除的节点有两个子节点的情况
		elif pointer.left != None and pointer.right != None:
			min_node_prev = pointer
			min_node = pointer.right
			new_pointer = min_node.left
			new_pos = "right"

			while new_pointer != None:
				new_pos = "left"
				min_node_prev = min_node
				min_node = new_pointer
				new_pointer = new_pointer.left
			new_node = tree_Node(min_node.data)
			new_node.left = pointer.left
			new_node.right = pointer.right

			if self.__head == pointer:
				self.__head = new_node
			else:
				if pos == "right":
					prev_pointer.right = new_node
				else:
					prev_pointer.left = new_node

			if min_node_prev == pointer:
				min_node_prev = new_node
			self.__del_step(min_node_prev, min_node, new_pos)

		# 要删除的节点只有一个子节点的情况
		else:
			if pointer == self.__head:
				if self.__head.left != None:
					self.__head = self.__head.left
				else:
					self.__head = self.__head.right
			else:
				if pos == "right":
					if pointer.right != None:
						prev_pointer.right = pointer.right
					else:
						prev_pointer.right = pointer.left
				else:
					if pointer.right != None:
						prev_pointer.left = pointer.right
					else:
						prev_pointer.left = pointer.left

	def find_data(self, element):
		pointer = self.__head
		find = False

		while pointer != None and find == False:
			if pointer.data == element:
				find = True
			elif pointer.data < element:
				pointer = pointer.right
			else:
				pointer = pointer.left

		if find:
			print("find data")
		else:
			print("No data in need")

	# 中序遍历
	def inorder_traversal(self, pointer=self.__head):
		if pointer != None:
			self.inorder_traversal(pointer.left)
			print(pointer.data, end=" ")
			self.inorder_traversal(pointer.right)
		elif pointer == self.__head:
			print(None)

	"""
		用于检查访问类基本信息的code是否正确，装饰器函数
		简单加入code目的是防止二叉查找树被恶意篡改，并留个接口给开发人员
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
	def return_basic_information(self, code):
		return self.__head, self.__left_num, self.__right_num
