"""
@version: python3.6
@author: Fieldhunter
@contact: 1677532160yuan@gmail.com
@time: 2020-05-03
"""
import functools


# AC automata based on Trie
class AC_Node():
    """
        The string types stored in the trie tree contain
          only 26 English lowercase letters.
        Self.length records the subscript of the character in the string.
        Self.end indicates whether the character is the end of a pattern string.
    """
    def __init__(self, string, pointer=None):
        self.data = string
        self.length = 0
        self.next = [None] * 26
        self.end = False
        self.fail= pointer


class AC_automata():
    def __init__(self):
        self.__head = AC_Node(None)

    def add_data(self, string):
        pointer = self.__head

        for num, character in enumerate(string):
            character_ascll = ord(character) - 97
            if pointer.next[character_ascll] == None:
                pointer.next[character_ascll] = AC_Node(character, self.__head)

            pointer = pointer.next[character_ascll]
            pointer.length = num
        pointer.end = True

        self.__structure()

    # Building AC_automata
    def __structure(self):
        queue = [self.__head]
        while len(queue) != 0:
            index = queue[0]
            del queue[0]

            for i in range(26):
                if index.next[i] == None:
                    continue

                fail_pointer = index.fail
                pointer = index
                while fail_pointer != None:
                    if fail_pointer.next[i] != None:
                        fail_pointer = fail_pointer.next[i]
                        pointer.next[i].fail = fail_pointer
                        break
                    else:
                        fail_pointer = fail_pointer.fail

                queue.append(pointer.next[i])

    def find_data(self, main):
        len_main = len(main)
        fail_pointer = self.__head

        for i in range(len_main):
            i_ascll = ord(main[i]) - 97
            while fail_pointer != None:
                if fail_pointer.next[i_ascll] == None:
                    fail_pointer = fail_pointer.fail
                else:
                    fail_pointer = fail_pointer.next[i_ascll]
                    break

            if fail_pointer == None:
                fail_pointer = self.__head
                continue

            index = fail_pointer
            while index != self.__head:
                if index.end == True:
                    print("The initial subscript of the matched string:{}，length:{}"\
                        .format(i-index.length,index.length+1))
                index = index.fail

    """
        Check if the code used to access self.__head,Decorator function.
        The purpose of simply adding code is to prevent AC automata from 
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
