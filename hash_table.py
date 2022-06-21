"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
import functools


"""
    This hash table stores data in string format.
    The stowage factor is set to 0.2-0.8.
    Using chain list method to solve hash conflict.
"""
class link_Node():
    def __init__(self, num):
        self.data = num
        self.next = None


class Linked_list():
    def __init__(self):
        self.head = None
        self.num = 0


class Hash_table():
    """
        Self.__size is the size of the hash table, which is 10 by default.
        Self.__num is the number of existing data.
        Self.__min_size do not update when not expanding. It is used to
          dynamically shrink the minimum size of the hash table.
        Self.__stowage is the load factor.
        Self.__expansion indicates whether the hash table is expanding.
          (True or False)
        Self.__new_table stores the new extended hash table.
        Self.__expansion_pos represents the position traversed by the original
          hash table during expanding the hash table, so as to facilitate
          deletion and search operations.

        The expansion strategy is that when we need to expand the hash table,
          we can only apply for it without moving the data. When we want to
          add a data, we can add the new data and move several data from the
          original hash table to the new hash table.
    """
    def __init__(self, size=10):
        self.__min_size = size
        self.__size = size
        self.__num = 0
        self.__expansion = False
        self.__expansion_pos = 0
        self.__new_table = None
        self.__stowage = self.__num / self.__size
        self.__data = []
        for _ in range(size):
            self.__data.append(None)

    # Used to check whether the input data is legal, decorator function
    def __check_data_format(func):
        @functools.wraps(func)
        def check(self, data):
            if type(data) != type("1"):
                data = str(data)
            func(self, data)

        return check

    """
        Check if the code used to access the hash table data,Decorator function.
        The purpose of simply adding code is to prevent hash table from 
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

    """
        The hash function computes the sum of the Unicode codes at each position
          on the string, then the average and the remainder with the hash size.
    """
    def __hash_function(self, data):
        num = 0
        sumer = 0
        for i in data:
            num += 1
            sumer += ord(i)
        sumer //= num
        sumer %= self.__size

        return sumer

    """
        Add the data from the old hash table to the new hash table,
          and move up to three at a time.
    """
    def __old_data_move(self):
        for _ in range(3):
            while self.__expansion_pos != len(self.__data) and\
                  self.__data[self.__expansion_pos] == None:
                self.__expansion_pos += 1

            """
                Determine whether the all original hash table data has been moved.
                  If it is True, update the new hash table to the self.__data.
            """
            if self.__expansion_pos == len(self.__data):
                self.__expansion = False
                self.__size = self.__new_table.__size
                self.__num = self.__new_table.__num
                self.__stowage = self.__new_table.__stowage
                self.__data = self.__new_table.__data
                self.__new_table = None
                self.__expansion_pos = 0
                break
            else:
                # process the original Hash table's chain list
                old_data = self.__data[self.__expansion_pos].head
                self.__data[self.__expansion_pos].head = \
                        self.__data[self.__expansion_pos].head.next
                self.__data[self.__expansion_pos].num -= 1
                if self.__data[self.__expansion_pos].head == None:
                    self.__data[self.__expansion_pos] = None

                old_hash_value = self.__new_table.__hash_function(old_data.data)
                if self.__new_table.__data[old_hash_value] == None:
                    link_list = Linked_list()
                    self.__new_table.__data[old_hash_value] = link_list
                else:
                    link_list = self.__new_table.__data[old_hash_value]

                old_data.next = link_list.head
                link_list.head = old_data
                link_list.num += 1
                self.__num -= 1
                self.__new_table.__num += 1
                self.__new_table.__stowage = self.__new_table.__num / self.__new_table.__size

    @__check_data_format
    def add_data(self, data):
        new_node = link_Node(data)

        if self.__expansion == False:
            hash_value = self.__hash_function(data)
            if self.__data[hash_value] == None:
                link_list = Linked_list()
                self.__data[hash_value] = link_list
            else:
                link_list = self.__data[hash_value]

            new_node.next = link_list.head
            link_list.head = new_node
            link_list.num += 1
            self.__num += 1
            self.__stowage = self.__num / self.__size

            # dynamic expansion
            if self.__stowage > 0.8:
                self.__expansion = True
                new_hash_table = Hash_table(self.__size*2)
                self.__new_table = new_hash_table
                self.__old_data_move()
        # during expansion
        else:
            # add new data first
            hash_value = self.__new_table.__hash_function(data)
            if self.__new_table.__data[hash_value] == None:
                link_list = Linked_list()
                self.__new_table.__data[hash_value] = link_list
            else:
                link_list = self.__new_table.__data[hash_value]

            new_node.next = link_list.head
            link_list.head = new_node
            link_list.num += 1
            self.__new_table.__num += 1
            self.__new_table.__stowage = self.__new_table.__num / self.__new_table.__size
            
            self.__old_data_move()

    @__check_data_format
    def del_data(self, data):
        hash_value = self.__hash_function(data)
        find = False

        # finding in the original hash table first
        if self.__data[hash_value] == None:
            pass
        else:
            pointer = self.__data[hash_value].head
            while pointer != None:
                if pointer.data == data:
                    find = True
                    break
                else:
                    prev_pointer = pointer
                    pointer = pointer.next

        if find:
            print("Successful del data")
            try:
                prev_pointer.next = pointer.next
            except:
                self.__data[hash_value].head = pointer.next

            self.__data[hash_value].num -= 1
            if self.__data[hash_value].num == 0:
                self.__data[hash_value] = None
            self.__num -= 1
            self.__stowage = self.__num / self.__size

        # determine whether hash table is in expansion.
        elif self.__expansion == True:
            hash_value = self.__new_table.__hash_function(data)
            if self.__new_table.__data[hash_value] == None:
                pass
            else:
                pointer = self.__new_table.__data[hash_value].head
                while pointer != None:
                    if pointer.data == data:
                        find = True
                        break
                    else:
                        prev_pointer = pointer
                        pointer = pointer.next

            if find:
                print("Successful del data in new_Hash_table")
                try:
                    prev_pointer.next = pointer.next
                except:
                    self.__new_table.__data[hash_value].head = pointer.next

                self.__new_table.__data[hash_value].num -= 1
                if self.__new_table.__data[hash_value].num == 0:
                    self.__new_table.__data[hash_value] = None
                self.__new_table.__num -= 1
                self.__new_table.__stowage = self.__new_table.__num / self.__new_table.__size
            else:
                print("No data in two Hash_table")
        else:
            print("No data in Hash_table")

        """
            If the deletion is successful and in the expansion state,
              then the function of __old_data_move will be implement.
        """
        if find and self.__expansion == True:
            self.__old_data_move()

        # dynamic shrinkage
        if self.__stowage < 0.2 and \
           self.__size > self.__min_size and self.__expansion == False:

            new_table = Hash_table(self.__size//2)
            while len(self.__data) > 0:
                if self.__data[0] == None or self.__data[0].head == None:
                    del self.__data[0]
                    continue
                else:
                    pointer = self.__data[0].head
                    while pointer != None:
                        new_table.add_data(pointer.data)
                        pointer = pointer.next
                        self.__data[0].head = pointer

            self.__data = new_table.__data
            self.__size = new_table.__size
            self.__stowage = self.__num / self.__size

    @__check_data_format
    def find_data(self, data):
        hash_value = self.__hash_function(data)
        find = False

        if self.__data[hash_value] == None:
            pass
        else:
            pointer = self.__data[hash_value].head
            while pointer != None:
                if pointer.data == data:
                    find = True
                    break
                else:
                    prev_pointer = pointer
                    pointer = pointer.next

        if find:
            print("Find data in Hash_table")
        elif self.__expansion == True:
            hash_value = self.__new_table.__hash_function(data)
            if self.__new_table.__data[hash_value] == None:
                pass
            else:
                pointer = self.__new_table.__data[hash_value].head
                while pointer != None:
                    if pointer.data == data:
                        find = True
                        break
                    else:
                        prev_pointer = pointer
                        pointer = pointer.next

            if find:
                print("Find data in new_Hash_table")
            else:
                print("No data in need")
        else:
            print("No data in need")

    def return_basic_information(self):
        return self.__min_size, self.__size, self.__num, \
            self.__expansion, self.__expansion_pos, self.__stowage

    @__check_code
    def return_hash_data(self, code):
        return self.__data

    @__check_code
    def return_hash_expansion_table(self, code):
        return self.__new_table
