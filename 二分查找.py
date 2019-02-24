def binary_search(data_list,target):
	num=len(data_list)
	low=0
	high=num-1
	find=False
	while low<=high:
		middle_num=low+(high-low)//2
		if data_list[middle_num]==target:
			find=True
			break
		elif data_list[middle_num]<target:
			low=middle_num+1
		else:
			high=middle_num-1
	if find:
		print(middle_num)
	else:
		print("No data")



def binary_search_1(data_list,target): 					#查找第一个值等于给定值的元素
	num=len(data_list)
	low=0
	high=num-1
	find=False
	while low<=high:
		middle_num=low+(high-low)//2
		if data_list[middle_num]==target:
			find=True
			if middle_num==0 or data_list[middle_num-1]!=target:
				break
			else:
				high=middle_num-1
		elif data_list[middle_num]<target:
			low=middle_num+1
		else:
			high=middle_num-1
	if find:
		print(middle_num)
	else:
		print("No data")



def binary_search_2(data_list,target): 					#查找最后一个值等于给定值的元素
	num=len(data_list)
	low=0
	high=num-1
	find=False
	while low<=high:
		middle_num=low+(high-low)//2
		if data_list[middle_num]==target:
			find=True
			if middle_num==num-1 or data_list[middle_num+1]!=target:
				break
			else:
				low=middle_num+1
		elif data_list[middle_num]<target:
			low=middle_num+1
		else:
			high=middle_num-1
	if find:
		print(middle_num)
	else:
		print("No data")



def binary_search_3(data_list,target): 					#查找第一个大于等于给定值的元素
	num=len(data_list)
	low=0
	high=num-1
	find=False
	while low<=high:
		middle_num=low+(high-low)//2
		if data_list[middle_num]<target:
			low=middle_num+1
		elif middle_num==0 or data_list[middle_num-1]<target:
			find=True
			break
		else:
			high=middle_num-1
	if find:
		print(middle_num)
	else:
		print("No data")



def binary_search_4(data_list,target): 					#查找最后一个小于等于给定值的元素
	num=len(data_list)
	low=0
	high=num-1
	find=False
	while low<=high:
		middle_num=low+(high-low)//2
		if data_list[middle_num]>target:
			high=middle_num-1
		elif middle_num==num-1 or data_list[middle_num+1]>target:
			find=True
			break
		else:
			low=middle_num+1
	if find:
		print(middle_num)
	else:
		print("No data")