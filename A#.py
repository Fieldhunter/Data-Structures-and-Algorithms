"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
import functools


class A_Node():
    """
        Self.value is used to store the weight 
          between the node and the pointing node.
        Self.x and self.y stores the X, Y values of the node.
    """
    def __init__(self, element, x_way, y_way):  
        self.data = element
        self.value = []
        self.x = x_way
        self.y = y_way


"""
    Implement a small top heap,
      which is used for priority queue of subsequent A#.
"""
class Heap():
    def __init__(self):
        self.data = [None]

    """
        The small top heap stores a tuple with two values.
        The first is the corresponding subscript of the node in the adjacency list.
        The second is the value of the node in the judge array in the A#.
        The small top heap is heaped up with the second value.
    """
    def add_data(self, element):
        self.data.append(element)
        index = len(self.data) - 1
        while index > 1:
            if self.data[index][1] < self.data[index//2][1]:
                self.data[index], self.data[index//2] = \
                    self.data[index//2], self.data[index]
                index //= 2
            else:
                break

    def get_top_element(self):
        num = len(self.data) - 1
        self.data[num], self.data[1] = self.data[1], self.data[num]

        """
            When getting the heap top element, only the corresponding
              subscript of the node in the adjacency list is returned.
        """
        top_element = self.data[-1][0]
        del self.data[-1]
        num -= 1
        self.__heap_up_down(self.data, num)

        return top_element

    # Heap up from top to bottom
    def __heap_up_down(self, data, num, index=1):
        while (2*index) <= num:
            # Both child nodes exist
            if (2*index+1) <= num:
                if data[2*index][1] <= data[index][1]:
                    if data[2*index+1][1] < data[index][1]:
                        if data[2*index][1] < data[2*index+1][1]:
                            data[index], data[2*index] = data[2*index], data[index]
                            index *= 2
                        else:
                            data[index], data[2*index+1] = data[2*index+1], data[index]
                            index = 2 * index + 1
                    else:
                        data[index], data[2*index] = data[2*index], data[index]
                        index *= 2
                elif data[2*index+1][1] < data[index][1]:
                    data[index], data[2*index+1] = data[2*index+1], data[index]
                    index = 2 * index + 1
                else:
                    break

            # only exist left child node
            else:
                if data[2*index][1] <= data[index][1]:
                    data[index], data[2*index] = data[2*index], data[index]
                    index *= 2
                else:
                    break


class Adjacency_list():
    """
        Self.__mapping is used to record the corresponding relationship
          between node value and node ordinal number.
        In self.__data,using node ordinal number express pointing relationship.
        Self.__node_mapping is used to store the corresponding relationship
          between node and node ordinal number.
    """
    def __init__(self):
        self.__data = {}
        self.__node_mapping = []
        self.__mapping = []

    def add_data(self, start, start_x, start_y, end, end_x, end_y, weight):
        start, end = str(start), str(end)
        if start not in self.__mapping:
            new_node = A_Node(start, start_x, start_y)
            self.__node_mapping.append(new_node)
            self.__mapping.append(start)
            start_num = len(self.__mapping) - 1
        else:
            """
                If the start node already exists,the coordinate
                  value of the start node will not be updated.
                The same is true for the end node.
            """
            start_num = self.__mapping.index(start)

        if end not in self.__mapping:
            new_node = A_Node(end, end_x, end_y)
            self.__node_mapping.append(new_node)
            self.__mapping.append(end)
            end_num = len(self.__mapping) - 1
        else:
            end_num = self.__mapping.index(end)

        if not self.__data.get(start_num, False):
            new_list = [end_num]
            self.__data[start_num] = new_list
            self.__node_mapping[start_num].value.append(weight)
        else:
            """
                If there is already a corresponding relationship between
                  the start node and the end node, the weights between them
                  will be updated.
            """
            if end_num in self.__data[start_num]:
                pointer = self.__data[start_num].index(end_num)
                self.__node_mapping[start_num].value[pointer] = weight
            else:
                self.__data[start_num].append(end_num)
                self.__node_mapping[start_num].value.append(weight)

    # A# algorithm
    def a(self, start, end):
        # calculate manhattan distance
        def manhattan(start_num, end_num):
            start_x, start_y = \
                self.__node_mapping[start_num].x, self.__node_mapping[start_num].y
            end_x , end_y = self.__node_mapping[end_num].x, 
                            self.__node_mapping[end_num].y
            manhattan_dist = abs(start_x-end_x) + abs(start_y-end_y)

            return manhattan_dist

        start,end = str(start), str(end)
        if start not in self.__mapping or end not in self.__mapping:
            print("No target data in map")
        else:
            """
                Initialization part:
                    Vertex array is used to store the distance betweena subscript node and
                      the starting node.It is recorded as g(i), and None represents infinity.

                    Judge array is used to store the sum of the Manhattan distance(h(i))
                      between a subscript node and the end node and the values in the
                      corresponding subscript vertexes array. It is recorded as f(i). 
                      None represents infinity.

                    Predecessor array is used to store the predecessor nodes of each node
                      and output the path.
                    Inqueue array is used to avoid adding a vertex to the priority queue
                      multiple times.
                    Level_queue is the priority queue.
            """
            start_num, end_num = self.__mapping.index(start), self.__mapping.index(end)
            vertexes = [None] * len(self.__mapping)
            judge = [None] * len(self.__mapping)
            predecessor = [-1] * len(self.__mapping)
            inqueue = [False] * len(self.__mapping)
            level_queue = Heap()
            find = False

            # Process the starting node first and put it into the priority queue
            vertexes[start_num] = 0
            judge[start_num] = manhattan(start_num, end_num)
            level_queue.add_data((start_num, judge[start_num]))
            inqueue[start_num] = True

            while len(level_queue.data) > 1 and find == False:
                # Take a node with the shortest judge value
                minvertex = level_queue.get_top_element()

                if self.__data.get(minvertex,False):
                    # Traversing the output node of minvertex
                    for num, i in enumerate(self.__data.get(minvertex)):
                        """
                            Judge array records f(i),f(i)=g(i)+h(i),and h(i) is manhattan distance.
                            The Manhattan distance of a node is constant, so the comparison of f(i)
                              in A# is also the comparison of g(i).That's how it's judged here.
                            If the g(i) value of minvertex plus the weight between two nodes is
                              less than the g(i) value of the outgoing node or the g(i) value of the
                              outgoing node is none, the g(i) value of the outgoing node is updated.
                        """
                        if vertexes[i] == None or \
                            (vertexes[minvertex] + self.__node_mapping[minvertex].value[num])\
                                < vertexes[i]:

                            """
                                At the same time, update the judge array, the f(i) value,
                                  and the predecessor node.
                            """
                            vertexes[i] = \
                                vertexes[minvertex] + self.__node_mapping[minvertex].value[num]
                            judge[i] = vertexes[i] + manhattan(i, end_num)
                            predecessor[i] = minvertex

                            """
                                Judge whether the outgoing node has previously been added to
                                  the priority queue. If not, add it.
                            """
                            if inqueue[i] == False:
                                level_queue.add_data((i, judge[i]))
                                inqueue[i] = True

                            # Exit the loop if traversing to the end node.
                            if i == end_num:
                                find = True
                                break

            # If the path is found, traverse the predecess array output.
            if find:
                pointer = predecessor[end_num]
                result = [self.__mapping[end_num]]
                while pointer != -1:
                    result.insert(0, self.__mapping[pointer])
                    pointer = predecessor[pointer]

                print(result)
            else:
                print("No way from start to end")

    """
        Check if the code used to access the class information,Decorator function.
        The purpose of simply adding code is to prevent Adjacency list from 
          being tampered with maliciously and to provide the API for developers.
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
    def return_data(self, code):
        return self.__data

    @__check_code
    def return_mapping(self, code):
        return self.__mapping, self.__node_mapping
