class Sequence_stack():                    #顺序栈
	def __init__(self):
		self.data_list=[]
		self.num=0

	def add_data(self,element):
		self.data_list.append(element)
		self.num+=1

	def delete_data(self):
		global last_data
		if self.data_list!=[]:
			last_data=self.data_list[-1]
			del self.data_list[-1]
			self.num-=1
		else:
			print("No data in stack")



class Node():                              #链式栈
	def __init__(self,num):
		self.data=num
		self.next=None

class Linked_stack():
	def __init__(self):
		self.head=None
		self.num=0
	
	def add_data(self,element):
		new_data=Node(element)
		new_data.next=self.head
		self.head=new_data
		self.num+=1

	def del_data(self):
		global last_data
		if self.head!=None:
			last_data=self.head.data
			self.head=self.head.next
			self.num-=1
		else:
			print("No data in stack")