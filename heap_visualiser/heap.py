def identity(x):
    return x

class Heap(object):
    """
    Max-heap data structure which keeps node of higher 
    data values at the top.
    """
    def __init__(self, key=identity, size=2):
        self._arr = [None] * size
        self._nItems = 0
        self._key = key

    def isEmpty(self):
        """Returns true if heap has no elements."""
        return self._nItems == 0

    def isFull(self):
        """Returns true if array is full."""
        return self._nItems == len(self._arr)

    def __len__(self):
        return self._nItems

    def peek(self):
        """Returns root of heap."""
        return None if self.isEmpty() else self._arr[0]

    def parent(self, i):
        """Returns index of parent of node at given index."""
        return (i - 1) // 2

    def leftChild(self, i):
        """Returns index of left child of node at given index."""
        return i * 2 + 1

    def rightChild(self, i):
        """Returns index of right child of node at given index."""
        return i * 2 + 2

    def _swap(self, i, j):
        """Swaps positions of two elements in array."""
        self._arr[i], self._arr[j] = self._arr[j], self._arr[i]

    def _growHeap(self):
        """Doubles size of array."""
        current = self._arr
        self._arr = [None] * max(1, 2 * len(self._arr))
        for i in range(self._nItems):
            self._arr[i] = current[i]
    
    def insert(self, item):
        """
        Inserts a new element into heap, ensuring higher 
        items are at top.
        """
        if self.isFull(): 
            self._growHeap()
        self._arr[self._nItems] = item
        self._nItems += 1
        self._siftUp_rec(self._nItems - 1)
    
    def remove(self):
        """
        Removes element from heap. Moves lowest element 
        to root and sifts down to maintain balance.
        """
        if self.isEmpty():
            raise Exception("Heap underflow")
        root = self._arr[0]
        self._nItems -= 1
        self._arr[0] = self._arr[self._nItems]
        self._arr[self._nItems] = None
        self._siftDown_rec(0)
        return root

    def _siftUp_rec(self, i):
        """Compares elements and swaps if parent is less than child."""
        if i <= 0: return
        parent = self.parent(i)
        if (self._key(self._arr[parent]) < 
            self._key(self._arr[i])):
            self._swap(parent, i)
            self._siftUp_rec(parent)
    
    def _siftDown_rec(self, i):
        """Compares elements and swaps if parent is less than child."""
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
        """
        Inserts into heap, yeilding at important stages and returing 
        indices of nodes involved in current stage of operation.
        """
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
        """
        Removes from heap, yeilding at important stages and returing 
        indices of nodes involved in current stage of operation.
        """
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
            if (
                right < self._nItems 
                and self._key(self._arr[left]) < self._key(self._arr[right])
            ):
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