import pygame


class Node:
    def __init__(self, row, col, cell_size, h_offset=0, v_offset=0, gap=2):
        self.row = row
        self.col = col
        self.neighbours: list[Node] = []  # up to 4, populated once at setup
        self.parent = None  # single node, set during A*
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')

        self.rect = pygame.Rect(col * cell_size + h_offset + gap,
                                row * cell_size + v_offset + gap,
                                cell_size - gap * 2,
                                cell_size - gap * 2)
        self.is_start = False
        self.is_end = False
        self.is_obstacle = False


    def __str__(self):
        return (f"({self.row},{self.col}) "
                f"\n Start: {str(self.is_start)} "
                f"\n End: {str(self.is_end)}"
                f"\n Obstacle: {str(self.is_obstacle)}")

    def clear_state(self):
        self.is_start = False
        self.is_end = False
        self.is_obstacle = False

    def set_start_true(self):
        self.is_start = True
        self.is_end = False
        self.is_obstacle = False

    def set_end_true(self):
        self.is_start = False
        self.is_end = True
        self.is_obstacle = False

    def set_obstacle_true(self):
        self.is_start = False
        self.is_end = False
        self.is_obstacle = True

    def compute_f(self):
        if self.is_obstacle:
            return

        self.f = self.g +self.h


class Graph:
    def __init__(self, rows, cols, cell_size, h_offset=0, v_offset=0):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[Node(r, c, self.cell_size, h_offset, v_offset) for c in range(cols)] for r in range(rows)]

        self.start_node = None
        self.end_node = None

        self.build_neighbours()

    def get_node(self, r, c):
        return self.grid[r][c]

    def clear_node_start(self):
        if self.start_node is not None:
            self.start_node.is_start = False
            self.start_node = None

    def clear_node_end(self):
        if self.end_node is not None:
            self.end_node.is_end = False
            self.end_node = None

    def set_start_node(self, node: Node):
        self.clear_node_start()
        self.start_node = node
        self.start_node.set_start_true()

    def set_end_node(self, node: Node):
        self.clear_node_end()
        self.end_node = node
        self.end_node.set_end_true()

    def clear_node_state(self, node: Node):
        node.clear_state()

        if node == self.start_node:
            self.clear_node_start()
        elif node == self.end_node:
            self.clear_node_end()

    def build_neighbours(self):
        """"""
        for r in range(self.rows):
            for c in range(self.cols):
                node = self.grid[r][c]
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up down left right
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        node.neighbours.append(self.grid[nr][nc])

    def get_clicked_node(self, event: pygame.event.Event):
        for c in self.grid:
            for node in c:
                if node.rect.collidepoint(event.pos):
                    return node

        return None

    def manhattan_distance(self, node1, node2):
        return abs(node1.row - node2.row) + abs(node1.col - node2.col)

    def priority_f_queue_insert(self, node_list: list[Node], node: Node):
        """uses a binary search to insert the given node into the list based on node.f. The lower, the closer to the
        start of the queue"""

        if not node_list:
            node_list.append(node)
            return

        low, high = 0, len(node_list)

        # binary search
        while low < high:
            mid = (low + high) // 2
            if node_list[mid].f < node.f:
                low = mid + 1
            else:
                high = mid

        node_list.insert(low, node)

    def reconstruct_path(self):
        path = []
        current = self.end_node

        while current is not None:
            path.append(current)
            current = current.parent

        return path

    def a_star_search(self):
        open_list: list[Node] = [self.start_node]
        closed_list: list[Node] = []

        self.start_node.g = 0
        self.start_node.h = self.manhattan_distance(self.start_node, self.end_node)
        self.start_node.compute_f()

        while len(open_list) > 0:
            current_node = open_list[0] # this list is sorted, so lowest f value is always at [0]


            if current_node.is_end: # goal found
                return self.reconstruct_path()

            print(str(current_node))

            # move node to other list
            open_list.pop(0)
            closed_list.append(current_node)

            for node in current_node.neighbours:
                if node in closed_list or node.is_obstacle: # don't repeat nodes
                    continue

                tentative_g = self.start_node.g + self.manhattan_distance(current_node, node)

                if node not in open_list:
                    open_list.append(node)

                elif tentative_g >= node.g: # this path is worse, exit
                    continue

                # the path is better
                node.parent = current_node
                node.g = tentative_g
                node.h = self.manhattan_distance(node, current_node)
                node.compute_f()

        return None
