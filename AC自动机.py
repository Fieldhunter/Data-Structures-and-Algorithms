import functools


# AC自动机建立在Trie树之上
class AC_Node():
	"""
		Trie树中存储的字符串种类只包含26个英文小写字母
		length记录该字符在字符串中的下标
		end表示该字符是否为一个模式串的结尾
	"""
	def __init__(self, string, pointer=None):
		self.data = string
		self.length = 0
		self.next = [None] * 26
		self.end = False
		self.fail= pointer


class AC_automata():
	def __init__(self):
		self.__head = AC_Node(None)

	def add_data(self, string):
		pointer = self.__head

		for num, character in enumerate(string):
			character_ascll = ord(character) - 97
			if pointer.next[character_ascll] == None:
				pointer.next[character_ascll] = AC_Node(character, self.__head)

			pointer = pointer.next[character_ascll]
			pointer.length = num
		pointer.end = True

		self.__structure()

	# 构建自动机操作
	def __structure(self):
		queue = [self.__head]
		while len(queue) != 0:
			index = queue[0]
			del queue[0]

			for i in range(26):
				if index.next[i] == None:
					continue

				fail_pointer = index.fail
				pointer = index
				while fail_pointer != None:
					if fail_pointer.next[i] != None:
						fail_pointer = fail_pointer.next[i]
						pointer.next[i].fail = fail_pointer
						break
					else:
						fail_pointer = fail_pointer.fail

				queue.append(pointer.next[i])

	def find_data(self, main):
		len_main = len(main)
		fail_pointer = self.__head

		for i in range(len_main):
			i_ascll = ord(main[i]) - 97
			while fail_pointer != None:
				if fail_pointer.next[i_ascll] == None:
					fail_pointer = fail_pointer.fail
				else:
					fail_pointer = fail_pointer.next[i_ascll]
					break

			if fail_pointer == None:
				fail_pointer = self.__head
				continue

			index = fail_pointer
			while index != self.__head:
				if index.end == True:
					print("匹配到的字符串初始下标为{}，长度为{}".format(i-index.length,index.length+1))
				index = index.fail

	"""
		用于检查访问self.__head的code是否正确，装饰器函数
		简单加入code目的是防止AC自动机被恶意篡改，并留个接口给开发人员
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
