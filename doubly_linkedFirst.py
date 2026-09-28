#Toby strawser

#Reworked code to pass all tests. Fixed remove_back to reset when list is empty

class Node:
    def __init__(self,item,prev=None,next=None):
        self.item = item
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    def __init__(self):
        self.header = Node("HEADER")
        self.header.prev = self.header
        self.header.next = self.header
        self.front = self.header
        self.last = self.header
    def __repr__(self):
        res = '<'
        temp = self.front
        while temp != self.header:
            res += str(temp.item)
            temp = temp.next
            if temp != self.header:
                res += ', '
        res += '>'
        return res



    def add_front(self,num):
        node = Node(num)
        if self.front == self.header:
            node.prev = self.header
            node.next = self.header
            self.header.next = node
            self.header.prev = node
            self.front = node
            self.last = node
        else:
            node.prev = self.header
            node.next = self.front
            self.front.prev = node
            self.header.next = node
            self.front = node
    def add_back(self,num):
        node = Node(num)
        if self.last == self.header:
            node.prev = self.header
            node.next = self.header
            self.header.next = node
            self.header.prev = node
            self.front = node
            self.last = node
        else:
            node.prev = self.last
            node.next = self.header
            self.last.next = node
            self.header.prev = node
            self.last = node

    def remove_front(self):
        if self.front == self.last:
            self.header.prev = self.header
            self.header.next = self.header
            self.front = self.header
        else:
            self.front.next.prev = self.header
            self.header.next = self.front.next
            self.front = self.header.next


    def remove_back(self):
        if self.front == self.last:
            self.header.prev = self.header
            self.header.next = self.header
            self.last = self.header
            self.front = self.header
        else:
            self.last.prev.next = self.header
            self.header.prev = self.last.prev
            self.last = self.header.prev


    def concatenate(self,other):
        last = self.last
        front = other.front

        self.last.next = other.front
        other.front.prev = self.last

        self.header.prev = other.header.prev
        other.header.next = self.header.next

        other.last.next = self.header
        self.front.prev = other.header


