class stack(object):
    def  __init__(self):
         self.__list =  []
    def is_empty(self):
        return self.__list ==  []
    def pop(self):
        self.__list.pop()
    def push(self, item):
        self.__list.append(item)
    def size(self):
        return len(self.__list)
    def peek(self):
        if self.__list:
            return self.__list[-1]
        else:
            return None