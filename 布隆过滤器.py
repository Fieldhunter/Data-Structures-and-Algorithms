class Bloom_Filter():
	def __init__(self,number):
		self.data=[bytearray(number)]		#布隆过滤器的data用一个数组存储，目的是可以存储多个扩容后的二进制表
		self.size=number					#size表示当前二进制表的尺寸大小
		self.num=0							#num表示当前表中已经改动的二进制个数（无论有没有重复，每添加一个数据num就增加3，目的是最大限度减少冲突）
		self.stowage=self.num/self.size 	#stowage是装载因子，最大限度为0.8，大于0.8则增加一个大小为原来一倍的新表到data中

	def hash_function_1(self,data,size):	#ASCll码法
		if type(data)!=type("1"):
			data=str(data)
		num=0
		sumer=0
		for i in data:
			num+=1
			sumer+=ord(i)
		sumer//=num
		sumer%=size
		return sumer

	def hash_function_2(self,data,size):	#对每一位上的ASCll值整除以本身的位数，累加，再与表的尺寸求余
		if type(data)!=type("1"):
			data=str(data)
		num=0
		sumer=0
		for i in data:
			num+=1
			sumer+=ord(i)//num
		sumer%=size
		return sumer

	def hash_function_3(self,data,size):	#平方求余
		if type(data)!=type(1):
			num=0
			sumer=0
			for i in data:
				num+=1
				sumer+=ord(i)
			data=sumer
		sumer=pow(data,2)
		sumer%=size
		return sumer

	def add_data(self,data):
		self.num+=3
		byte_list=self.data[-1]
		hash_value_1=self.hash_function_1(data,self.size)
		hash_value_2=self.hash_function_2(data,self.size)
		hash_value_3=self.hash_function_3(data,self.size)
		byte_list[hash_value_1]=1
		byte_list[hash_value_2]=1
		byte_list[hash_value_3]=1

		self.stowage=self.num/self.size
		if self.stowage>0.8: 			#是否要增加一个大小2倍的表
			self.data.append(bytearray(self.size*2))
			self.num=0					#将num，size，stowage更新为新表的数值
			self.size*=2
			self.stowage=0

	def find_data(self,data):
		find=False
		for num,byte_list in enumerate(self.data):
			hash_value_1=self.hash_function_1(data,len(byte_list))
			hash_value_2=self.hash_function_2(data,len(byte_list))
			hash_value_3=self.hash_function_3(data,len(byte_list))
			if byte_list[hash_value_1]==1 and byte_list[hash_value_2]==1 and byte_list[hash_value_3]==1:
				find=True
				break

		if find:
			print("Find data in list_{}".format(num+1))
		else:
			print("No target data")