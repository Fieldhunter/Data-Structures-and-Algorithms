# 实现一个大顶堆
class Heap():
	def __init__(self):
		self.data = [None]

	def add_data(self, element):
		self.data.append(element)
		index = len(self.data) - 1
		while index > 1:
			if self.data[index] > self.data[index//2]:
				self.data[index], self.data[index//2] = \
					self.data[index//2], self.data[index]
				index //= 2
			else:
				break

	def del_top_element(self):
		num = len(self.data) - 1
		if num == 0:
			print("No data in Heap")
		else:
			self.data[num], self.data[1] = self.data[1], self.data[num]
			del self.data[-1]
			num -= 1
			heap_up_down(self.data,num)


# 从上往下进行堆化
def heap_up_down(data, num, index=1):
	while (2*index) <= num:

		# 两个子节点都存在
		if (2*index+1) <= num:
			if data[2*index] > data[index]:
				if data[2*index+1] > data[index]:
					if data[2*index] > data[2*index+1]:
						data[index], data[2*index] = data[2*index], data[index]
						index *= 2
					else:
						data[index], data[2*index+1] = data[2*index+1], data[index]
						index = 2 * index + 1
				else:
					data[index], data[2*index] = data[2*index], data[index]
					index *= 2
			elif data[2*index+1] > data[index]:
				data[index], data[2*index+1] = data[2*index+1], data[index]
				index = 2 * index + 1
			else:
				break

		# 只存在左节点
		else:
			if data[2*index] > data[index]:
				data[index], data[2*index] = data[2*index], data[index]
				index *= 2
			else:
				break


# 堆排序
def heap_sort(data):
	data.insert(0, None)
	num = len(data) - 1
	pointer = num // 2

	# 建堆
	while pointer >= 1:
		heap_up_down(data, num, pointer)
		pointer -= 1

	# 排序
	index = num
	for _ in range(num-1):
		data[1], data[index] = data[index], data[1]
		index -= 1
		heap_up_down(data, index)

	del data[0]
