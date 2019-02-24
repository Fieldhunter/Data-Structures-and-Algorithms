class Node():
	def __init__(self,element):			#in_degree表示入度数，out_degree表示出度数
		self.data=element
		self.in_degree=0
		self.out_degree=0

class Adjacency_list():			#邻接表
	def __init__(self):			#node_mapping用来记录节点与节点序数的对应关系
		self.data={}			#mapping用来记录节点数据与节点序数的对应关系
		self.node_mapping=[]	#data中用节点序数来表示指向关系
		self.mapping=[]

	def add_data(self,start,end):
		start,end=str(start),str(end)
		if start not in self.mapping:
			new_node=Node(start)
			self.node_mapping.append(new_node)
			self.mapping.append(start)
			start_num=len(self.mapping)-1
		else:
			start_num=self.mapping.index(start)
		if end not in self.mapping:
			new_node=Node(end)
			self.node_mapping.append(new_node)
			self.mapping.append(end)
			end_num=len(self.mapping)-1
		else:
			end_num=self.mapping.index(end)

		if not self.data.get(start_num,False):
			new_list=[end_num]
			self.data[start_num]=new_list
			self.node_mapping[start_num].out_degree+=1
			self.node_mapping[end_num].in_degree+=1
		else:
			if end_num in self.data[start_num]:
				print("data is in list")
			else:
				self.data[start_num].append(end_num)
				self.node_mapping[start_num].out_degree+=1
				self.node_mapping[end_num].in_degree+=1

	def kahn(self):
		in_list=[]					#in_list记录每个节点的入度数
		for i in self.node_mapping:
			in_list.append(i.in_degree)
		quene=[]					#queue是一个队列，用来存储待处理的节点下标
		result=[]					#result用来存储结果顺序

		try:
			pointer=in_list.index(0)	#找到入度为0的初始节点下标
			quene.append(pointer)
			in_list[pointer]=None
		except:
			pass
		while len(quene)!=0:
			pointer=quene[0]
			del quene[0]
			result.append(self.mapping[pointer])
			if self.data.get(pointer,False):
				for i in self.data.get(pointer):
					in_list[i]-=1
					if in_list[i]==0:		#入度为0的节点设置为None
						quene.append(i)
						in_list[i]=None
		if in_list.count(None)==len(in_list):		#如果最终in_list里不全是None，说明有环
			print(result)
		else:
			print("A ring in map")

	def DFS(self):
		def loop_output(num,result,count):		#循环输出
			count+=1
			if count>len(self.mapping):			#如果函数执行次数超过了总的节点数，说明肯定存在环
				return False
			if inverse_adjacency_list.get(num,False):
				for j in inverse_adjacency_list.get(num):
					result=loop_output(j,result,count)
			if result!=False:
				if check_list[num]!=True:		#该节点如果没有输出过，则输出
					check_list[num]=True
					result.append(self.mapping[num])
			return result

		check_list=[False]*len(self.mapping)		#check_list数组用来判断该下标的节点有没有输出过
		out_list=[]									#out_list记录每个节点的出度数
		result=[]									#result用来存储结果顺序
		count=0										#count用来记录循环输出函数的执行次数
		for i in self.node_mapping:
			out_list.append(i.out_degree)

		inverse_adjacency_list={}					#构建逆邻接表
		for i in self.data:
			if self.data.get(i,False):
				for j in self.data.get(i):
					if inverse_adjacency_list.get(j,False):
						inverse_adjacency_list[j].append(i)
					else:
						new_list=[i]
						inverse_adjacency_list[j]=new_list

		try:
			pointer=out_list.index(0)				#找到出度数初始值为0的节点，即原顺序的末尾
			result=loop_output(pointer,result,count)
			if result==False:
				print("A ring in map")
			else:
				print(result)
		except:
			print("A ring in map")