"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
import functools


"""
    In the binary search tree, the value of each node in the left subtree is
      less than or equal to the value of this node, and the value of the right
      subtree node is greater than the value of this node.
"""
class tree_Node():
    def __init__(self, num):
        self.data = num
        self.left = None
        self.right = None


class Binary_search_tree():
    """
        Self__left and self.__right num are used to record the number of left and
          right subtree nodes of the root node.
        It is used for proper left and right rotation (refer to red black tree) to
          improve the operation efficiency as much as possible.
    """
    def __init__(self):
        self.__head = None
        self.__left_num = 0
        self.__right_num = 0

    def __left_rotate(self):
        while self.__left_num < self.__right_num:
            focus_node = self.__head
            right_node = self.__head.right
            right_node_son = right_node.left

            focus_node.right = right_node_son
            right_node.left = focus_node
            self.__head = right_node

            if right_node_son == None:
                self.__left_num += 1
                self.__right_num -= 1
            else:
                self.__left_num += 2
                self.__right_num -= 2

    def __right_rotate(self):
        while self.__right_num < self.__left_num:
            focus_node = self.__head
            left_node = self.__head.left
            left_node_son = left_node.right

            focus_node.left = left_node_son
            left_node.right = focus_node
            self.__head = left_node

            if left_node_son == None:
                self.__left_num -= 1
                self.__right_num += 1
            else:
                self.__left_num -= 2
                self.__right_num += 2

    def add_data(self, element):
        new_node = tree_Node(element)
        if self.__head == None:
            self.__head = new_node
        else:
            pointer = self.__head
            if element > self.__head.data:
                self.__right_num += 1
            else:
                self.__left_num += 1

            while pointer != None:
                prev_pointer = pointer
                if element > pointer.data:
                    pointer = pointer.right
                    pos = "right"
                else:
                    pointer = pointer.left
                    pos = "left"

            if pos == "right":
                prev_pointer.right = new_node
            else:
                prev_pointer.left = new_node

        # When the number of two subtrees differs by 5, rotate left and right
        if self.__left_num - self.__right_num == 5:
            self.__right_rotate()
        elif self.__right_num - self.__left_num == 5:
            self.__left_rotate()

    def del_data(self, element):
        prev_pointer = None
        pos = None
        pointer = self.__head
        find = False

        """
            convenient to reduce the number of left and
              right subtree nodes of root node
        """
        if pointer != None:
            if pointer.data < element:
                direction = "right"
            else:
                direction = "left"

        while pointer != None and find == False:
            if pointer.data == element:
                find = True
            else:
                prev_pointer = pointer
                if pointer.data < element:
                    pointer = pointer.right
                    pos = "right"
                else:
                    pointer = pointer.left
                    pos = "left"
        
        if find:
            if pointer != self.__head:
                if direction == "right":
                    self.__right_num -= 1
                else:
                    self.__left_num -= 1
            elif pointer.right != None:
                self.__right_num -= 1
            elif pointer.left != None:
                self.__left_num -= 1

            """
                Because the second step of deletion has the operation of
                  reusing the second step, so the second step is carried 
                  out separately.
            """
            self.__del_step(prev_pointer, pointer, pos)

            print("Successful to del data")
        else:
            print("No data in need")

        # When the number of two subtrees differs by 5, rotate left and right.
        if self.__left_num - self.__right_num == 5:
            self.__right_rotate()
        elif self.__right_num - self.__left_num == 5:
            self.__left_rotate()

    def __del_step(self, prev_pointer, pointer, pos):
        # when the node to be deleted has no child nodes
        if pointer.left == None and pointer.right == None:
            if pointer == self.__head:
                self.__head == None
            else:
                if pos == "right":
                    prev_pointer.right = None
                else:
                    prev_pointer.left = None

        # when the node to be deleted has two child nodes
        elif pointer.left != None and pointer.right != None:
            min_node_prev = pointer
            min_node = pointer.right
            new_pointer = min_node.left
            new_pos = "right"

            while new_pointer != None:
                new_pos = "left"
                min_node_prev = min_node
                min_node = new_pointer
                new_pointer = new_pointer.left
            new_node = tree_Node(min_node.data)
            new_node.left = pointer.left
            new_node.right = pointer.right

            if self.__head == pointer:
                self.__head = new_node
            else:
                if pos == "right":
                    prev_pointer.right = new_node
                else:
                    prev_pointer.left = new_node

            if min_node_prev == pointer:
                min_node_prev = new_node
            self.__del_step(min_node_prev, min_node, new_pos)

        # when the node to be deleted has only one child
        else:
            if pointer == self.__head:
                if self.__head.left != None:
                    self.__head = self.__head.left
                else:
                    self.__head = self.__head.right
            else:
                if pos == "right":
                    if pointer.right != None:
                        prev_pointer.right = pointer.right
                    else:
                        prev_pointer.right = pointer.left
                else:
                    if pointer.right != None:
                        prev_pointer.left = pointer.right
                    else:
                        prev_pointer.left = pointer.left

    def find_data(self, element):
        pointer = self.__head
        find = False

        while pointer != None and find == False:
            if pointer.data == element:
                find = True
            elif pointer.data < element:
                pointer = pointer.right
            else:
                pointer = pointer.left

        if find:
            print("find data")
        else:
            print("No data in need")

    def inorder_traversal(self, pointer=self.__head):
        if pointer != None:
            self.inorder_traversal(pointer.left)
            print(pointer.data, end=" ")
            self.inorder_traversal(pointer.right)
        elif pointer == self.__head:
            print(None)

    """
        Check if the code used to access the tree information,Decorator function.
        The purpose of simply adding code is to prevent binary search tree from 
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
    def return_basic_information(self, code):
        return self.__head, self.__left_num, self.__right_num
