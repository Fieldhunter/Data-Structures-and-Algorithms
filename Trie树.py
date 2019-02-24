class Node():
	def __init__(self,string):			#Trie树中存储的字符串种类只包含26个英文小写字母
		self.data=string
		self.next=[None]*26
		self.end=False

class Trie():
	def __init__(self):
		self.head=Node(None)

	def add_data(self,string):
		pointer=self.head
		for character in string:
			character_ascll=ord(character)-97
			if pointer.next[character_ascll]==None:
				new_node=Node(character)
				pointer.next[character_ascll]=new_node
			pointer=pointer.next[character_ascll]
		pointer.end=True

	def find_data(self,string):
		pointer=self.head
		find=False
		for character in string:
			character_ascll=ord(character)-97
			if pointer.next[character_ascll]==None:
				break
			pointer=pointer.next[character_ascll]
			if character==string[-1]:
				if pointer.end==True:
					find=True
		if find:
			print("Find target data")
		else:
			print("No target data")