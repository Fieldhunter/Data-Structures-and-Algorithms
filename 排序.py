import random


# 冒泡排序
def bubble_sort(data_list):
	num = len(data_list)
	for i in range(num-1):
		find = False
		for j in range(num-i-1):
			if data_list[j] > data_list[j+1]:
				find = True
				data_list[j], data_list[j+1] = data_list[j+1], data_list[j]
		if find == False:
			break

	print(data_list)


# 插入排序
def insertion_sort(data_list):
	num = len(data_list)
	for i in range(num):
		m = i
		while m > 0:
			if data_list[m] < data_list[m-1]:
				data_list[m], data_list[m-1] = data_list[m-1], data_list[m]
			else:
				break
			m -= 1

	print(data_list)


# 选择排序
def selection_sort(data_list):
	num = len(data_list)
	for i in range(num):
		min_pos = i
		for j in range(i+1, num):
			if data_list[j] < data_list[min_pos]:
				min_pos = j
		data_list[i], data_list[min_pos] = data_list[min_pos], data_list[i]

	print(data_list)


# 归并排序
def merge_sort(data_list):
	num = len(data_list)
	if num == 1:
		return data_list
	else:
		middle_num = num // 2
		merge_list_1 = merge_sort(data_list[ : middle_num])
		merge_list_2 = merge_sort(data_list[middle_num : ])
		last_list = []
		m = n = 0

		while m <= len(merge_list_1) - 1 and n <= len(merge_list_2) - 1:
			if merge_list_1[m] <= merge_list_2[n]:
				last_list.append(merge_list_1[m])
				m += 1
			else:
				last_list.append(merge_list_2[n])
				n += 1

		if m > len(merge_list_1) - 1:
			while n <= len(merge_list_2) - 1:
				last_list.append(merge_list_2[n])
				n += 1
		else:
			while m <= len(merge_list_1) - 1:
				last_list.append(merge_list_1[m])
				m += 1

		return last_list


# 快速排序
def quick_sort(data_list):
	num = len(data_list)
	if num <= 1:
		return data_list
	else:
		pivot = random.randint(0, num-1)
		data_list[pivot], data_list[num-1] = data_list[num-1], data_list[pivot]
		pivot = num - 1
		i = j = 0

		while j != pivot:
			if data_list[j] <= data_list[pivot]:
				data_list[i], data_list[j] = data_list[j], data_list[i]
				i += 1
			j += 1

		data_list[i], data_list[pivot] = data_list[pivot], data_list[i]
		data_list[ : i] = quick_sort(data_list[ : i])
		data_list[i+1 : ] = quick_sort(data_list[i+1 : ])

		return data_list


# 桶排序,此例为对0-1000范围的数进行排序
def bucket_sort(data_list):
	list_1 = []
	list_2 = []
	list_3 = []

	for i in data_list:
		if i >= 0 and i <= 333:
			list_1.append(i)
		elif i <= 666:
			list_2.append(i)
		else:
			list_3.append(i)

	list_1 = quick_sort(list_1)
	list_2 = quick_sort(list_2)
	list_3 = quick_sort(list_3)
	data_list[ : ]= list_1 + list_2 + list_3

	return data_list


# 计数排序
def count_sort(data_list):
	num = len(data_list)
	max_num = max(data_list)
	list_1 = []
	last_list = []

	for i in range(max_num+1):
		list_1.append(0)
	for i in range(num):
		last_list.append(0)

	for i in data_list:
		list_1[i] += 1
	for i in range(1,max_num+1):
		list_1[i] += list_1[i-1]
	for i in data_list:
		last_list[list_1[i]-1] = i
		list_1[i] -= 1

	return last_list


#基数排序，此例为排序电话号码
def radix_sort(data_list, pos=0):
	if len(data_list) == 1:
		return data_list
	else:
		now_pos = pos
		num = len(data_list)
		len_num = len(str(max(data_list)))
		list_1 = []
		list_2 = []
		list_3 = []
		list_4 = []

		for i in range(num):
			list_1.append(int(str(data_list[i])[now_pos]))
		for i in range(10):
			list_2.append(0)
		for i in range(num):
			list_3.append(0)
			list_4.append(0)

		for i in list_1:
			list_2[i] += 1
		for i in range(1, 10):
			list_2[i] += list_2[i-1]
		count = 0
		for i in list_1:
			list_3[list_2[i]-1] = i
			list_4[list_2[i]-1] = data_list[count]
			list_2[i] -= 1
			count += 1

		start = end = 0
		last_list = []
		for i in range(num-1):
			if list_3[i] == list_3[i+1]:
				end += 1
				continue
			else:
				sort_list = radix_sort(list_4[start:end+1], pos=now_pos+1)
				last_list += sort_list
				end += 1
				start = end
		sort_list = radix_sort(list_4[start : end+1], pos=now_pos+1)
		last_list += sort_list

		return last_list
