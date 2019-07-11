class Node():
	# 存储的数据为数字
	def __init__(self, data):
		self.data = data
		self.next = None


class Linkedlist():
	def __init__(self):
		self.head = None
		self.num = 0

	# num是要加入的数字,pos_num代表在哪个数据后面加入,不填默认在头结点
	def add_data(self, num, pos_num=None):		
		new_node = Node(num)
		if self.head == None or pos_num == None:
			new_node.next = self.head
			self.head = new_node
			self.num += 1
		else:
			data_1 = self.head
			finder = False
			while data_1.data != pos_num and data_1 != None:
				data_1 = data_1.next
			if data_1.data == pos_num:
				finder = True
			
			if finder == False:
				print("No data in need")
			else:
				new_node.next = data_1.next
				data_1.next = new_node
				self.num += 1

	def del_data(self, num):
		data_1 = None
		data_2 = self.head
		finder = False

		while not data_2 == None:
			if data_2.data == num:
				finder = True
				if data_1 == None:
					if data_2.next == None:
						self.head = None
					else:
						self.head = data_2.next
				else:
					data_1.next = data_2.next
				self.num -= 1
				data_2.next = data_2.data = None
				break
			else:
				data_1 = data_2
				data_2 = data_2.next

		if finder == True:
			print("delete OK!")
		else:
			print("No data")

	def find_data(self, num):
		data_list = self.head
		pos = 0
		while not data_list == None:
			pos += 1
			if data_list.data == num:
				break
			else:
				data_list = data_list.next

		print(pos)

	def print_all_data(self):
		data_list = self.head
		while data_list != None:
			print(data_list.data, end=" ")
			data_list = data_list.next

	# 单链表反转
	def reversal(self):
		try:
			data_1 = None
			data_2 = self.head
			data_3 = self.head.next

			while not data_3 == None:
				data_2.next = data_1
				data_1 = data_2
				data_2 = data_3
				data_3 = data_3.next
			data_2.next = data_1 
			self.head = data_2
		except:
			pass

	def find_middle_data(self):
		middle_pos = self.num // 2
		data_list = self.head
		pos = 1

		while pos < middle_pos:
			pos += 1
			data_list = data_list.next
		if middle_pos % 2 != 0 and self.num != 1:
			data_list = data_list.next

		try:
			print(data_list.data)
		except:
			print("No data in linkedlist")

	def check_ring(self):
		result = False
		fast_point = self.head
		slow_point = self.head

		while fast_point != None and slow_point != None:
			if fast_point.next == slow_point:
				result = True
				break
			else:
				if fast_point.next == None:
					break
				else:
					fast_point = fast_point.next.next
					slow_point = slow_point.next

		if result == True:
			print("has circle")
		else:
			print("No circle")


# 两个链表合并
def merge(list1, list2, list3):
	data1 = list1.head
	data2 = list2.head

	while not data1 == None and not data2 == None:
		if data1.data >= data2.data:
			num = data1
			data1 = data1.next
			list3.add_data(num)
		else:
			num = data2
			data2 = data2.next
			list3.add_data(num)

	if data1 == None:
		while not data2 == None:
			num = data2
			data2 = data2.next
			list3.add_data(num)
	else:
		while not data1 == None:
			num = data1
			data1 = data1.next
			list3.add_data(num)
