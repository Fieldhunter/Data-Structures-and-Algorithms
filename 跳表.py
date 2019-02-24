class Node():
	def __init__(self,data):					#next列表表示该节点指向的节点，不同位置的节点表示索引中不同层数指向的位置
		self.data=data							#0号位是链表本身，1号位是第一层索引，以此类推，后面跳表实现阶段会初始化和更新
		self.next=[]

class Skip_list():
	def __init__(self):
		self.head=None
		self.add_num=0
		self.del_num=0
		self.num=0

	def index(self):
		num=self.num
		max_level=0
		while num>3:					#计算索引的层数
			max_level+=1
			num//=3

		pointer=self.head					#为每个节点的next列表初始化
		while pointer:
			if len(pointer.next)-1<max_level:				#索引层数增加
				for _ in range(max_level-(len(pointer.next)-1)):
					pointer.next.append(None)
			elif len(pointer.next)-1>max_level:				#索引层数减少
				del pointer.next[-(len(pointer.next)-1-max_level):]
			pointer=pointer.next[0]

		for i in range(max_level): 					#更新构建索引的节点的next列表
			pointer=self.head
			while pointer:
				try:
					next_pointer=pointer.next[i].next[i].next[i]
					pointer.next[i+1]=next_pointer
					pointer=next_pointer
				except:					#处理这一层索引最后一个节点
					pointer.next[i+1]=None
					break

	def add_data(self,element):					#加入数据，使链表保持由小到大的顺序
		new_data=Node(element)
		self.num+=1
		self.add_num+=1
		if self.head==None or new_data.data<=self.head.data:
			new_data.next.append(self.head)
			self.head=new_data
		else:
			pointer=self.head
			for i in range(len(self.head.next),0,-1):
				while pointer.next[i-1]!=None:
					if new_data.data<=pointer.next[i-1].data:
						break
					else:
						pointer=pointer.next[i-1]
			new_data.next.append(pointer.next[0])
			pointer.next[0]=new_data

		if self.add_num==3:			#每加入三个数据更新一遍索引
			self.index()
			self.add_num=0

	def del_data(self,num):
		if self.head==None:
			print("No data in Skip_list")
		elif self.head.data==num:
			self.head=self.head.next[0]
			self.num-=1
			self.index()
		else:
			prev_pointer=self.head
			find=False
			for i in range(len(self.head.next),0,-1):
				if not find:
					pointer=prev_pointer.next[i-1]
				while pointer!=None:
					if pointer.data==num:
						while prev_pointer.next[i-1]!=pointer:		#更新前指针，保证两指针的前后关系	
							prev_pointer=prev_pointer.next[i-1]
						prev_pointer.next[i-1]=pointer.next[i-1]
						find=True
						break
					elif pointer.data<num:
						prev_pointer=prev_pointer.next[i-1]
						pointer=pointer.next[i-1]
					else:
						break
			if find:
				self.num-=1
				self.del_num+=1
			else:
				print("No data in Skip_list")
			if self.del_num==3:					#每删除三个数据更新一遍索引，删除头结点不算
				self.index()
				self.del_num=0

	def find_data(self,num):
		if self.head==None:
			print("No data in Skip_list")
		else:
			find=False
			pointer=self.head
			for i in range(len(self.head.next),0,-1):
				if find:
					break
				while pointer.next[i-1]!=None:
					if pointer.data==num:
						find=True
						break
					elif pointer.next[i-1].data<=num:
						pointer=pointer.next[i-1]
					else:
						break
			if find:
				print("Find your data")
			else:
				print("No this data in Skip_list")