import functools


"""
	用于检查访问队列信息的code是否正确，装饰器函数
	简单加入code目的是防止队列被恶意篡改，并留个接口给开发人员
"""
def check_code(func):
	@functools.wraps(func)
	def check(self, code):
		if code != 'adsf;{h3096j34ka`fd>&/edgb^45:6':
			raise Exception('code is wrong!')
		result = func(self, code)
		return result

	return check


# 顺序栈
class Sequence_stack():
	def __init__(self):
		self.__data_list = []
		self.__num = 0

	def add_data(self, element):
		self.__data_list.append(element)
		self.__num += 1

	def pop_data(self):
		if self.__data_list != []:
			last_data = self.__data_list[-1]
			del self.__data_list[-1]
			self.__num -= 1

			return last_data
		else:
			print("No data in stack")
			return None

	@check_code
	def return_basic_information(self, code):
		return self.__data_list, self.__num


# 链式栈
class link_Node():
	def __init__(self, num):
		self.data = num
		self.next = None


class Linked_stack():
	def __init__(self):
		self.__head = None
		self.__num = 0
	
	def add_data(self, element):
		new_data = link_Node(element)
		new_data.next = self.__head
		self.__head = new_data
		self.__num += 1

	def pop_data(self):
		if self.__head != None:
			last_data = self.__head.data
			self.__head = self.__head.next
			self.__num -= 1

			return last_data
		else:
			print("No data in stack")
			return None

	@check_code
	def return_basic_information(self, code):
		return self.__head, self.__num
