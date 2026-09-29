#Made by Toby Strawser

class IndexMinPQ:
    def __init__(self):
        self.keys = []
        self.priority = {}
        self.position = {}


    def is_empty(self):
        if len(self.keys) == 0:
            return True
        else:
            return False

    def enqueue(self, key, priority):
        self.keys.append(key)
        self.priority[key] = priority
        self.position[key] = len(self.keys) - 1
        self._swap(self.position[key])
        pass

    def dequeue(self):
        if not self.keys:
            return None

        min_key = self.keys[0]

        last_key = self.keys.pop()

        if self.keys:
            self.keys[0] = last_key
            self.position[last_key] = 0
            self._swap_down(0)

        self.position.pop(min_key, None)

        return min_key


    def reduce_priority(self, key, num):
        if key not in self.position:
            return

        if num >= self.priority[key]:
            return

        self.priority[key] = num

        index = self.position[key]
        self._swap(index)

    def _swap(self,index):
        while index > 0:
            parent = (index - 1) // 2

            if self.priority[self.keys[index]] >= self.priority[self.keys[parent]]:
                break

            child = index
            kc = self.keys[child]
            kp = self.keys[parent]

            self.keys[child] = kp
            self.keys[parent] = kc

            self.position[kp] = child
            self.position[kc] = parent

            index = parent

    def _swap_down(self,index):

        size = len(self.keys)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            # compare left child
            if left < size and self.priority[self.keys[left]] < self.priority[self.keys[smallest]]:
                smallest = left

            # compare right child
            if right < size and self.priority[self.keys[right]] < self.priority[self.keys[smallest]]:
                smallest = right

            # no change → heap property holds
            if smallest == index:
                break

            # swap index with smallest child
            kc = self.keys[index]
            ks = self.keys[smallest]

            self.keys[index] = ks
            self.keys[smallest] = kc

            self.position[ks] = index
            self.position[kc] = smallest

            index = smallest