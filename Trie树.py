import functools


class Trie_Node():
	# Trie树中存储的字符串种类只包含26个英文小写字母
	def __init__(self, string):
		self.data = string
		self.next = [None] * 26
		self.end = False

class Trie():
	def __init__(self):
		self.__head = Trie_Node(None)

	def add_data(self, string):
		pointer = self.__head

		for character in string:
			character_ascll = ord(character) - 97
			if pointer.next[character_ascll] == None:
				new_node = Trie_Node(character)
				pointer.next[character_ascll] = new_node
			pointer = pointer.next[character_ascll]

		pointer.end = True

	def find_data(self, string):
		pointer = self.__head
		find = False

		for character in string:
			character_ascll = ord(character) - 97
			if pointer.next[character_ascll] == None:
				break
			pointer = pointer.next[character_ascll]
			if character == string[-1]:
				if pointer.end == True:
					find = True

		if find:
			print("Find target data")
		else:
			print("No target data")

	"""
		用于检查访问self.__head的code是否正确，装饰器函数
		简单加入code目的是防止Trie树被恶意篡改，并留个接口给开发人员
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
