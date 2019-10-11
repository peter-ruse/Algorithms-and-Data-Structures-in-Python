
class MinHeap:
    def __init__(self, n):
        """The heap consists of elements (x, v), where x is an element label,
        which runs from 0 to n, and the v are the values. pos gives the position
        of x in the heap.
        """
        self.heap = []
        self.pos = [None]*n


    def bubble_up(self, i):
        """Bubbles an element up the heap as needed,
        in order to preserve the heap property
        """
        while True:
            if (i - 1) // 2 >= 0:
                x1, v1 = self.heap[(i - 1) // 2]
                x2, v2 = self.heap[i]
                if v2 < v1:
                    temp1 = self.heap[i]
                    self.heap[i] = self.heap[(i - 1) // 2]
                    self.heap[(i - 1) // 2] = temp1
                    self.pos[x1] = i
                    self.pos[x2] = (i - 1) // 2
                    i = (i - 1) // 2
                else:
                    break
            else:
                break


    def bubble_down(self, i):
        """Bubbles an element down the heap as needed,
        in order to preserve the heap property
        """
        while True:
            if 2*i+1 < len(self.heap):
                if 2*i+2 < len(self.heap):
                    (x1, v1) = self.heap[i]
                    (x2, v2) = self.heap[2 * i + 1]
                    (x3, v3) = self.heap[2 * i + 2]
                    if v2 < v1:
                        if v2 < v3:
                            temp1 = self.heap[i]
                            self.heap[i] = self.heap[2*i+1]
                            self.heap[2 * i + 1] = temp1
                            self.pos[x1] = 2 * i + 1
                            self.pos[x2] = i
                            i = 2 * i + 1
                        else:
                            temp1 = self.heap[i]
                            self.heap[i] = self.heap[2 * i + 2]
                            self.heap[2 * i + 2] = temp1
                            self.pos[x1] = 2 * i + 2
                            self.pos[x3] = i
                            i = 2 * i + 2
                    else:
                        if v3 < v1:
                            temp1 = self.heap[i]
                            self.heap[i] = self.heap[2 * i + 2]
                            self.heap[2 * i + 2] = temp1
                            self.pos[x1] = 2 * i + 2
                            self.pos[x3] = i
                            i = 2 * i + 2
                        else:
                            break
                else:
                    (x1, v1) = self.heap[i]
                    (x2, v2) = self.heap[2 * i + 1]
                    if v2 < v1:
                        temp1 = self.heap[i]
                        self.heap[i] = self.heap[2 * i + 1]
                        self.heap[2 * i + 1] = temp1
                        self.pos[x1] = 2 * i + 1
                        self.pos[x2] = i
                        i = 2 * i + 1
                    else:
                        break
            else:
                break


    def insert(self, x, v):
        """Inserts a new element with label x and value v into the heap"""
        k = len(self.heap)
        self.pos[x] = k
        self.heap.append((x, v))
        self.bubble_up(k)


    def update(self, x, v_new):
        """Updates the heap element (x, v) to (x, v_new),
        and makes the necessary adjustments
        """
        i = self.pos[x]
        (x, v) = self.heap[i]
        self.heap[i] = (x, v_new)
        if v_new < v:
            self.bubble_up(i)
        else:
            self.bubble_down(i)


    def get_value(self, x):
        """Gets the value of the element with label x"""
        i = self.pos[x]
        _, v = self.heap[i]
        return v


    def remove(self):
        """Removes the smallest element of the heap, heap[0], by moving the heap's
        last element into the 0-th position, and making the necessary adjustments
        """
        if not self.heap:
            return
        (first, v_min) = self.heap[0]
        self.pos[first] = None
        (last, v) = self.heap.pop()
        if self.heap:
            self.heap[0] = (last, v)
            self.pos[last] = 0
        self.bubble_down(0)
        return (first, v_min)


class MaxHeap:
    def __init__(self, n):
        """The heap consists of elements (x, v), where x is an element label,
        which runs from 0 to n, and the v are the values. pos gives the position
        of x in the heap.
        """
        self.heap = []
        self.pos = [None] * n


    def bubble_up(self, i):
        """Bubbles an element up the heap as needed,
        in order to preserve the heap property
        """
        while True:
            if (i-1)//2 >= 0:
                x1, v1 = self.heap[(i - 1) // 2]
                x2, v2 = self.heap[i]
                if v2 > v1:
                    temp1 = self.heap[i]
                    self.heap[i] = self.heap[(i - 1) // 2]
                    self.heap[(i - 1) // 2] = temp1
                    self.pos[x1] = i
                    self.pos[x2] = (i - 1) // 2
                    i = (i - 1) // 2
                else:
                    break
            else:
                break


    def bubble_down(self, i):
        """Bubbles an element down the heap as needed,
        in order to preserve the heap property
        """
        while True:
            if 2 * i + 1 < len(self.heap):
                if 2 * i + 2 < len(self.heap):
                    (x1, v1) = self.heap[i]
                    (x2, v2) = self.heap[2 * i + 1]
                    (x3, v3) = self.heap[2 * i + 2]
                    if v2 > v1:
                        if v2 > v3:
                            temp1 = self.heap[i]
                            self.heap[i] = self.heap[2 * i + 1]
                            self.heap[2 * i + 1] = temp1
                            self.pos[x1] = 2 * i + 1
                            self.pos[x2] = i
                            i = 2 * i + 1
                        else:
                            temp1 = self.heap[i]
                            self.heap[i] = self.heap[2 * i + 2]
                            self.heap[2 * i + 2] = temp1
                            self.pos[x1] = 2 * i + 2
                            self.pos[x3] = i
                            i = 2 * i + 2
                    else:
                        if v3 > v1:
                            temp1 = self.heap[i]
                            self.heap[i] = self.heap[2 * i + 2]
                            self.heap[2 * i + 2] = temp1
                            self.pos[x1] = 2 * i + 2
                            self.pos[x3] = i
                            i = 2 * i + 2
                        else:
                            break
                else:
                    (x1, v1) = self.heap[i]
                    (x2, v2) = self.heap[2 * i + 1]
                    if v2 > v1:
                        temp1 = self.heap[i]
                        self.heap[i] = self.heap[2 * i + 1]
                        self.heap[2 * i + 1] = temp1
                        self.pos[x1] = 2 * i + 1
                        self.pos[x2] = i
                        i = 2 * i + 1
                    else:
                        break
            else:
                break


    def insert(self, x, v):
        """Inserts a new element with label x and value v into the heap"""
        k = len(self.heap)
        self.pos[x] = k
        self.heap.append((x, v))
        self.bubble_up(k)


    def update(self, x, v_new):
        """Updates the heap element (x, v) to (x, v_new),
        and makes the necessary adjustments
        """
        i = self.pos[x]
        (x, v) = self.heap[i]
        self.heap[i] = (x, v_new)
        if v_new > v:
            self.bubble_up(i)
        else:
            self.bubble_down(i)


    def get_value(self, x):
        """Gets the value of the element with label x"""
        i = self.pos[x]
        _, v = self.heap[i]
        return v


    def remove(self):
        """Removes the smallest element of the heap, heap[0], by moving the heap's
        last element into the 0-th position, and making the necessary adjustments
        """
        if not self.heap:
            return
        (first, v_max) = self.heap[0]
        del self.pos[first]
        (last, v) = self.heap.pop()
        if self.heap:
            self.heap[0] = (last, v)
            self.pos[last] = 0
        self.bubble_down(0)
        return (first, v_max)
