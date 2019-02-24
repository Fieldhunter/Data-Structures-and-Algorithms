class Sequential_queue(): 					#顺序队列
	def __init__(self):
		self.data=[]
		self.num=0

	def add_data(self,element):
		self.data.append(element)
		self.num+=1

	def del_data(self):
		global last_data
		if self.data!=[]:
			last_data=self.data[0]
			del self.data[0]
			self.num-=1
		else:
			print("No data in queue")



class Node(): 					#链式队列
	def __init__(self,num):
		self.data=num
		self.prev=None
		self.next=None

class Linked_queue():
	def __init__(self):
		self.head=None
		self.tail=None
		self.num=0

	def add_data(self,element):
		new_data=Node(element)
		self.num+=1
		if self.tail==None:
			self.head=self.tail=new_data
		else:
			self.head.prev=new_data
			new_data.next=self.head
			self.head=new_data

	def del_data(self):
		global last_data
		if self.tail==None:
			print("No data in queue")
		else:
			last_data=self.tail.data
			self.tail=self.tail.prev
			if self.tail==None:
				self.head=None