def identity(x):
    return x

class Heap(object):
    def __init__(self, key=identity, size=2):
        self._arr = [None] * size
        self._nItems = 0
        self._key = key

    def isEmpty(self):
        return self._nItems == 0

    def isFull(self):
        return self._nItems == len(self._arr)

    def __len__(self):
        return self._nItems

    def peek(self):
        return None if self.isEmpty() else self._arr[0]

    def parent(self, i):
        return (i - 1) // 2

    def leftChild(self, i):
        return i * 2 + 1

    def rightChild(self, i):
        return i * 2 + 2

    def _swap(self, i, j):
        self._arr[i], self._arr[j] = self._arr[j], self._arr[i]

    def _growHeap(self):
        current = self._arr
        self._arr = [None] * max(1, 2 * len(self._arr))
        for i in range(self._nItems):
            self._arr[i] = current[i]
    
    def insert(self, item):
        if self.isFull(): 
            self._growHeap()
        self._arr[self._nItems] = item
        self._nItems += 1
        self._siftUp_rec(self._nItems - 1)
    
    def remove(self):
        if self.isEmpty():
            raise Exception("Heap underflow")
        root = self._arr[0]
        self._nItems -= 1
        self._arr[0] = self._arr[self._nItems]
        self._arr[self._nItems] = None
        self._siftDown_rec(0)
        return root

    def _siftUp_rec(self, i):
        if i <= 0: return
        parent = self.parent(i)
        if (self._key(self._arr[parent]) < 
            self._key(self._arr[i])):
            self._swap(parent, i)
            self._siftUp_rec(parent)
    
    def _siftDown_rec(self, i):
        left, right = self.leftChild(i), self.rightChild(i)
        if left < len(self):
            if right < len(self):
                maxi = right if (self._key(self._arr[left]) < 
                                self._key(self._arr[right])
                                ) else left
            else:
                maxi = left
            if (self._key(self._arr[i]) < 
                self._key(self._arr[maxi])):
                self._swap(i, maxi)
                self._siftDown_rec(maxi)
    

    def animate_insert(self, item):
        if self.isFull(): 
            self._growHeap()

        idx = self._nItems
        self._arr[idx] = item
        self._nItems += 1
        # Pause for node placed at end
        yield ([idx])

        curr = idx
        while curr > 0:
            p_idx = self.parent(curr)
            # Pause for comparison
            yield ([curr, p_idx])
            
            if self._key(self._arr[p_idx]) < self._key(self._arr[curr]):
                self._swap(p_idx, curr)
                curr = p_idx
                # Pause for swap
                yield ([curr])
            else:
                break
        yield ([])

    def animate_remove(self):
        if self.isEmpty():
            raise Exception("Heap underflow")
        
        root_val = self._arr[0]
        # Highlight root
        yield ([0])
        
        self._nItems -= 1
        self._arr[0] = self._arr[self._nItems]
        self._arr[self._nItems] = None
        # Show last item at root
        yield ([0])

        curr = 0
        while True:
            left, right = self.leftChild(curr), self.rightChild(curr)
            if left >= self._nItems:
                break
            
            maxi = left
            if right < self._nItems and self._key(self._arr[left]) < self._key(self._arr[right]):
                maxi = right
            # Compare nodes
            yield ([curr, maxi])

            if self._key(self._arr[curr]) < self._key(self._arr[maxi]):
                self._swap(curr, maxi)
                curr = maxi
                # Show swap
                yield ([curr])
            else:
                break
        yield ([])