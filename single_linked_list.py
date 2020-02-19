import functools


class Link_Node():
	# Stored data is digital
	def __init__(self, data):
		self.data = data
		self.next = None


class Linkedlist():
	def __init__(self):
		self.__head = None
		self.__num = 0

	"""
		num is the number to be added.
		pos_num is which the data is added after.(position ordinal)
		  It is filled in the header node by default.
	"""
	def add_data(self, num, pos_num=None):
		new_node = Link_Node(num)
		if self.__head == None or pos_num == None:
			new_node.next = self.__head
			self.__head = new_node
			self.__num += 1
		else:
			data_1 = self.__head
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
				self.__num += 1

	def del_data(self, num):
		data_1 = None
		data_2 = self.__head
		finder = False

		while not data_2 == None:
			if data_2.data == num:
				finder = True
				if data_1 == None:
					if data_2.next == None:
						self.__head = None
					else:
						self.__head = data_2.next
				else:
					data_1.next = data_2.next
				self.__num -= 1
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
		data_list = self.__head
		pos = 0
		while not data_list == None:
			pos += 1
			if data_list.data == num:
				break
			else:
				data_list = data_list.next

		print(pos)

	def print_all_data(self):
		data_list = self.__head
		while data_list != None:
			print(data_list.data, end=" ")
			data_list = data_list.next

	# single linked list inversion
	def reversal(self):
		try:
			data_1 = None
			data_2 = self.__head
			data_3 = self.__head.next

			while not data_3 == None:
				data_2.next = data_1
				data_1 = data_2
				data_2 = data_3
				data_3 = data_3.next
			data_2.next = data_1 
			self.__head = data_2
		except:
			pass

	def find_middle_data(self):
		middle_pos = self.__num // 2
		data_list = self.__head
		pos = 1

		while pos < middle_pos:
			pos += 1
			data_list = data_list.next
		if middle_pos % 2 != 0 and self.__num != 1:
			data_list = data_list.next

		try:
			print(data_list.data)
		except:
			print("No data in linkedlist")

	def check_ring(self):
		result = False
		fast_point = self.__head
		slow_point = self.__head

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
			print("Find circle")
		else:
			print("No circle")

	"""
		Check if the code used to access the linked list's head,Decorator function.
		The purpose of simply adding code is to prevent linked list from 
		  being tampered with maliciously and to provide the API for developers.
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

	def return_num(self):
		return self.__num


# merge two linked lists
def merge(list1, list2):
	data1 = list1.return_head('adsf;{h3096j34ka`fd>&/edgb^45:6')
	data2 = list2.return_head('adsf;{h3096j34ka`fd>&/edgb^45:6')
	new_link_list = Linkedlist()

	while not data1 == None and not data2 == None:
		if data1.data >= data2.data:
			num = data1.data
			data1 = data1.next
			new_link_list.add_data(num)
		else:
			num = data2.data
			data2 = data2.next
			new_link_list.add_data(num)

	if data1 == None:
		while not data2 == None:
			num = data2.data
			data2 = data2.next
			new_link_list.add_data(num)
	else:
		while not data1 == None:
			num = data1.data
			data1 = data1.next
			new_link_list.add_data(num)

	return new_link_list
