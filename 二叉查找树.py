class Node():							#该二叉搜索树中，左子树中的每个节点的值，都要小于等于这个节点的值
	def __init__(self,num):				#而右子树节点的值都大于这个节点的值
		self.data=num
		self.left=None
		self.right=None

class Binary_search_tree():
	def __init__(self):
		self.head=None
		self.left_num=0			#这两个值用来记录根节点左右两树的个数情况
		self.right_num=0		#适当进行左右旋(借鉴红黑树)，以尽量提高各操作效率

	def left_rotate(self):
		while self.left_num<self.right_num:
			focus_node=self.head
			right_node=self.head.right
			right_node_son=right_node.left

			focus_node.right=right_node_son
			right_node.left=focus_node
			self.head=right_node
			if right_node_son==None:
				self.left_num+=1
				self.right_num-=1
			else:
				self.left_num+=2
				self.right_num-=2

	def right_rotate(self):
		while self.right_num<self.left_num:
			focus_node=self.head
			left_node=self.head.left
			left_node_son=left_node.right

			focus_node.left=left_node_son
			left_node.right=focus_node
			self.head=left_node
			if left_node_son==None:
				self.left_num-=1
				self.right_num+=1
			else:
				self.left_num-=2
				self.right_num+=2

	def add_data(self,element):
		new_node=Node(element)
		if self.head==None:
			self.head=new_node
		else:
			pointer=self.head
			if element>self.head.data:
				self.right_num+=1
			else:
				self.left_num+=1
			while pointer!=None:
				prev_pointer=pointer
				if element>pointer.data:
					pointer=pointer.right
					pos="right"
				else:
					pointer=pointer.left
					pos="left"
			if pos=="right":
				prev_pointer.right=new_node
			else:
				prev_pointer.left=new_node

		if self.left_num-self.right_num==5:			#两子树个数相差5个时候，进行左右旋
			self.right_rotate()
		elif self.right_num-self.left_num==5:
			self.left_rotate()

	def del_data(self,element):
		prev_pointer=None
		pos=None
		pointer=self.head
		find=False
		if pointer!=None:				#方便减少根节点左右子树节点个数
			if pointer.data<element:
				direction="right"
			else:
				direction="left"
		while pointer!=None and find==False:
			if pointer.data==element:
				find=True
			else:
				prev_pointer=pointer
				if pointer.data<element:
					pointer=pointer.right
					pos="right"
				else:
					pointer=pointer.left
					pos="left"
		
		if find:
			if pointer!=self.head:
				if direction=="right":
					self.right_num-=1
				else:
					self.left_num-=1
			elif pointer.right!=None:
				self.right_num-=1
			elif pointer.left!=None:
				self.left_num-=1
			self.del_step(prev_pointer,pointer,pos)		#因为删除第二步中有重复使用第二步的操作，所以将第二步单独拎出来
			print("Successful to del data")
		else:
			print("No data in need")

		if self.left_num-self.right_num==5:			#两子树个数相差5个时候，进行左右旋
			self.right_rotate()
		elif self.right_num-self.left_num==5:
			self.left_rotate()

	def del_step(self,prev_pointer,pointer,pos):
		if pointer.left==None and pointer.right==None:	#要删除的节点没有子节点的情况
			if pointer==self.head:
				self.head==None
			else:
				if pos=="right":
					prev_pointer.right=None
				else:
					prev_pointer.left=None
		elif pointer.left!=None and pointer.right!=None:	#要删除的节点有两个子节点的情况
			min_node_prev=pointer
			min_node=pointer.right
			new_pointer=min_node.left
			new_pos="right"
			while new_pointer!=None:
				new_pos="left"
				min_node_prev=min_node
				min_node=new_pointer
				new_pointer=new_pointer.left
			new_node=Node(min_node.data)
			new_node.left=pointer.left
			new_node.right=pointer.right
			if self.head==pointer:
				self.head=new_node
			else:
				if pos=="right":
					prev_pointer.right=new_node
				else:
					prev_pointer.left=new_node
			if min_node_prev==pointer:
				min_node_prev=new_node
			self.del_step(min_node_prev,min_node,new_pos)
		else:											#要删除的节点只有一个子节点的情况
			if pointer==self.head:
				if self.head.left!=None:
					self.head=self.head.left
				else:
					self.head=self.head.right
			else:
				if pos=="right":
					if pointer.right!=None:
						prev_pointer.right=pointer.right
					else:
						prev_pointer.right=pointer.left
				else:
					if pointer.right!=None:
						prev_pointer.left=pointer.right
					else:
						prev_pointer.left=pointer.left

	def find_data(self,element):
		pointer=self.head
		find=False
		while pointer!=None and find==False:
			if pointer.data==element:
				find=True
			elif pointer.data<element:
				pointer=pointer.right
			else:
				pointer=pointer.left
		if find:
			print("find data")
		else:
			print("No data in need")

	def inorder_traversal(self,pointer=True):			#中序遍历
		if pointer==True:
			pointer=self.head
		if pointer!=None:
			self.inorder_traversal(pointer.left)
			print(pointer.data,end=" ")
			self.inorder_traversal(pointer.right)