"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
import functools


class Dijkstra_Node():
    """
        Self.value is used to store the weight 
          between the node and the pointing node.
    """
    def __init__(self, element):
        self.data = element
        self.value = []


# Implement a small top heap for priority queue of Dijkstra
class Heap():
    def __init__(self):
        self.data = [None]

    """
        The small top heap stores a tuple with two values.
        The first is the corresponding subscript of the node in the adjacency list.
        The second is the distance between the node and the starting node
          in Dijkstra, that is, the value of the node's subscript in the
          following vertex array.
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

    def add_data(self, start, end, weight):
        start, end = str(start), str(end)
        if start not in self.__mapping:
            new_node = Dijkstra_Node(start)
            self.__node_mapping.append(new_node)
            self.__mapping.append(start)
            start_num = len(self.__mapping) - 1
        else:
            start_num = self.__mapping.index(start)
        if end not in self.__mapping:
            new_node = Dijkstra_Node(end)
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

    # Dijkstra algorithm
    def dijkstra(self, start, end):
        start,end = str(start),str(end)

        if start not in self.__mapping or end not in self.__mapping:
            print("No target data in map")
        else:
            """
                Initialization part:
                    Vertex array is used to store the distance between a subscript node and
                      the starting node. It is recorded as dist, and None represents infinity.
                    Predicessor array is used to store the predecessor nodes of each node and
                      output the path.
                    Inqueue array is used to avoid adding a vertex to the priority queue
                      multiple times.
                    Level_queue is the priority queue.
            """
            start_num, end_num = self.__mapping.index(start), self.__mapping.index(end)
            vertexes = [None] * len(self.__mapping)
            predecessor = [-1] * len(self.__mapping)
            inqueue = [False] * len(self.__mapping)
            level_queue = Heap()
            find = False

            # Process the starting node first and put it into the priority queue.
            vertexes[start_num] = 0
            level_queue.add_data((start_num, vertexes[start_num]))
            inqueue[start_num] = True

            while len(level_queue.data) > 1:
                # Take out a node with the shortest distance from the starting node.
                minvertex = level_queue.get_top_element()

                """
                    If the end node exits the queue, then the shortest path is found,
                      and the loop exits.
                """
                if minvertex == end_num:
                    find = True
                    break

                if self.__data.get(minvertex, False):
                    # Traversing the output node of minvertex
                    for num, i in enumerate(self.__data.get(minvertex)):
                        if vertexes[i] == None or vertexes[minvertex] + \
                            self.__node_mapping[minvertex].value[num] < vertexes[i]:

                            """
                                If the dist value of minvertex plus the weight between two nodes
                                  is less than the dist value of the outgoing node or the dist value
                                  of the outgoing node is None, the dist value of the outgoing node
                                  is updated, and the predecessor node is updated at the same time.
                            """
                            vertexes[i] = vertexes[minvertex] + \
                                self.__node_mapping[minvertex].value[num]
                            predecessor[i] = minvertex

                            """
                                Determine whether the outgoing node has previously been added to
                                  the priority queue. If not, add it.
                            """
                            if inqueue[i] == False:
                                level_queue.add_data((i, vertexes[i]))
                                inqueue[i] = True

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
