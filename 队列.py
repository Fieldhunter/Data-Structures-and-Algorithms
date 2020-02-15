import functools


"""
	用于检查访问队列基本信息的code是否正确，装饰器函数
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


# 顺序队列
class Sequential_queue():
	def __init__(self):
		self.__data = []
		self.__num = 0

	def add_data(self, element):
		self.__data.append(element)
		self.__num += 1

	def pop_data(self):
		if self.__data != []:
			last_data = self.__data[0]
			del self.__data[0]
			self.__num -= 1

			return last_data
		else:
			print("No data in queue")
			return None

	@check_code
	def return_basic_information(self, code):
		return self.__data, self.__num


#链式队列
class Link_Node():
	def __init__(self, num):
		self.data = num
		self.prev = None
		self.next = None


class Linked_queue():
	def __init__(self):
		self.__head = None
		self.__tail = None
		self.__num = 0

	def add_data(self, element):
		new_data = Link_Node(element)
		self.__num += 1
		if self.__tail == None:
			self.__head = self.__tail = new_data
		else:
			self.__head.prev = new_data
			new_data.next = self.__head
			self.__head = new_data

	def pop_data(self):
		if self.__tail == None:
			print("No data in queue")
			return None
		else:
			last_data = self.__tail.data
			self.__tail = self.__tail.prev
			self.__num -= 1
			if self.__tail == None:
				self.__head = None

			return last_data

	@check_code
	def return_basic_information(self, code):
		return self.__head, self.__tail, self.__num
