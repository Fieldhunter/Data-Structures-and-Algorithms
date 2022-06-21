"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
import functools


class link_Node():
    """
        The next list represents the list of nodes the node points to.
        Different positions in the list represent the nodes pointed to by
          different index layers of the node in the skip list. The 0-bit is the
          chain table itself, the 1-bit is the first level index, and so on.
        Later implementation phase will initialize and update the skip list.
    """
    def __init__(self, data):
        self.data = data
        self.next = []


class Skip_list():
    def __init__(self):
        self.__head = None
        self.__add_num = 0
        self.__del_num = 0
        self.__num = 0

    def __index(self):
        # calculate the number of levels of the index
        num = self.__num
        max_level = 0
        while num > 3:
            max_level += 1
            num //= 3

        # initialize the next list for each node
        pointer = self.__head
        while pointer:

            # increase index layer's number
            if len(pointer.next) - 1 < max_level:
                for _ in range(max_level - (len(pointer.next)-1)):
                    pointer.next.append(None)

            # reduce index layer's number
            elif len(pointer.next) - 1 > max_level: 
                del pointer.next[-(len(pointer.next)-1-max_level) : ]
            pointer = pointer.next[0]

        # update the next list of nodes that build the index
        for i in range(max_level):
            pointer = self.__head
            while pointer:
                try:
                    next_pointer = pointer.next[i].next[i].next[i]
                    pointer.next[i+1] = next_pointer
                    pointer = next_pointer
                except:
                    # process the last node of this index layer
                    pointer.next[i+1] = None
                    break

    # add data, and keep the list in order from small to large
    def add_data(self, element):
        new_data = link_Node(element)
        self.__num += 1
        self.__add_num += 1

        if self.__head == None or new_data.data <= self.__head.data:
            new_data.next.append(self.__head)
            self.__head = new_data
        else:
            pointer = self.__head
            for i in range(len(self.__head.next), 0, -1):
                while pointer.next[i-1] != None:
                    if new_data.data <= pointer.next[i-1].data:
                        break
                    else:
                        pointer = pointer.next[i-1]

            new_data.next.append(pointer.next[0])
            pointer.next[0] = new_data

        # update index every three data added
        if self.__add_num == 3:
            self.__index()
            self.__add_num = 0

    def del_data(self, num):
        if self.__head == None:
            print("No data in Skip_list")
        elif self.__head.data == num:
            self.__head = self.__head.next[0]
            self.__num -= 1
            self.__index()
        else:
            prev_pointer = self.__head
            find = False

            for i in range(len(self.__head.next), 0, -1):
                if not find:
                    pointer = prev_pointer.next[i-1]

                while pointer != None:
                    if pointer.data == num:
                        """
                            update the prev_pointer, and ensure the anterior and
                              posterior relationship between the two pointers
                        """
                        while prev_pointer.next[i-1] != pointer:    
                            prev_pointer = prev_pointer.next[i-1]

                        prev_pointer.next[i-1] = pointer.next[i-1]
                        find = True
                        break
                    elif pointer.data < num:
                        prev_pointer = prev_pointer.next[i-1]
                        pointer = pointer.next[i-1]
                    else:
                        break

            if find:
                self.__num -= 1
                self.__del_num += 1
            else:
                print("No data in Skip_list")

            """
                The index is updated every three data deleted.
                Deleting the header node does not count.
            """
            if self.__del_num == 3:
                self.__index()
                self.__del_num = 0

    def find_data(self, num):
        if self.__head == None:
            print("No data in Skip_list")
        else:
            find = False
            pointer = self.__head
            for i in range(len(self.__head.next), 0, -1):
                if find:
                    break
                while pointer.next[i-1] != None:
                    if pointer.data == num:
                        find = True
                        break
                    elif pointer.next[i-1].data <= num:
                        pointer = pointer.next[i-1]
                    else:
                        break

            if find:
                print("Find your data")
            else:
                print("No this data in Skip_list")

    """
        Check if the code used to access the skip list information,
          Decorator function.
        The purpose of simply adding code is to prevent skip list from 
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
    def return_head(self, code):
        return self.__head

    @__check_code
    def return_num(self, code):
        return self.__num, self.__add_num, self.__del_num
