from heap_visualiser.heap import Heap


class Event:
    """Data type representing events in event queue."""
    def __init__(
            self, hour: int, minute: int, priority: int, title: str
        ) -> None:
        self.hour = hour
        self.minute = minute
        self.priority = priority
        self.title = title


class EventQueue:
    """
    Priority queue implemented using Heap data structure.
    """
    def __init__(self) -> None:
        self._heap = Heap(
            key=lambda e: (-e.hour, -e.minute, -e.priority)
        )
        
    def get(self, index: int) -> Event | None:
        """Returns queue item at given index."""
        return self._heap._arr[index]
    
    def leftChild(self, index) -> int:
        """Returns left child of node at given index."""
        return self._heap.leftChild(index)
    
    def rightChild(self, index) -> int:
        """Returns right child of node at given index."""
        return self._heap.rightChild(index)

    def __len__(self) -> int:
        """Returns number of items stored in heap."""
        return len(self._heap)
    
    def insert(self, event: Event) -> None:
        """Inserts event into priority queue."""
        self._heap.insert(event)
    
    def remove(self) -> None:
        """Removes root of priority queue."""
        self._heap.remove()

    def animate_insert(self, event: Event):
        """
        Inserts event at bottom and sifts up, yielding at
        important stages and returning indices of nodes involved
        in current stage of operation.
        """
        if self._heap.isFull():
            self._heap._growHeap()

        idx = self._heap._nItems
        self._heap._arr[idx] = event # type: ignore
        self._heap._nItems += 1

        # Node added
        yield ([idx], "insert")

        curr = idx

        while curr > 0:
            p_idx = self._heap.parent(curr)

            parent = self._heap._arr[p_idx]
            child = self._heap._arr[curr]

            # Highlight time comparison
            yield ([curr, p_idx], "time")

            parent_time = (parent.hour, parent.minute)
            child_time = (child.hour, child.minute)

            if child_time < parent_time:
                self._heap._swap(curr, p_idx)
                curr = p_idx

                yield ([curr], "swap")

            elif child_time == parent_time:

                # Highlight priority comparison
                yield ([curr, p_idx], "priority")

                if child.priority < parent.priority:
                    self._heap._swap(curr, p_idx)
                    curr = p_idx

                    yield ([curr], "swap")

                else:
                    break

            else:
                break

        yield ([], "")
    

    def animate_extract(self):
        """
        Removes upcoming event from queue, yielding at
        important stages and returning indices of nodes involved
        in current stage of operation.
        """
        if self._heap.isEmpty():
            return

        # Highlight root being removed
        yield ([0], "time")

        self._heap._nItems -= 1

        # Move last node to root
        root = self._heap._arr[0]
        self._heap._arr[0] = self._heap._arr[self._heap._nItems]
        self._heap._arr[self._heap._nItems] = None

        # Show new root
        yield ([0], "time")

        curr = 0

        while True:
            left = self._heap.leftChild(curr)
            right = self._heap.rightChild(curr)

            # No children
            if left >= self._heap._nItems:
                break

            best = left

            # Choose child with earlier time / higher priority
            if right < self._heap._nItems:

                left_event = self._heap._arr[left]
                right_event = self._heap._arr[right]

                left_time = (left_event.hour, left_event.minute)
                right_time = (right_event.hour, right_event.minute)

                # Compare times first
                if right_time < left_time:
                    best = right

                # If same time, compare priority
                elif right_time == left_time:
                    if right_event.priority < left_event.priority:
                        best = right

            curr_event = self._heap._arr[curr]
            best_event = self._heap._arr[best]

            curr_time = (curr_event.hour, curr_event.minute)
            best_time = (best_event.hour, best_event.minute)

            # Highlight time comparison
            yield ([curr, best], "time")

            should_swap = False

            # Earlier time moves upward
            if best_time < curr_time:
                should_swap = True

            # Same time -> compare priority
            elif best_time == curr_time:

                # Highlight priority comparison
                yield ([curr, best], "priority")

                if best_event.priority < curr_event.priority:
                    should_swap = True

            if should_swap:
                self._heap._swap(curr, best)

                curr = best

                # Highlight swap
                yield ([curr], "swap")

            else:
                break

        yield ([root], "")