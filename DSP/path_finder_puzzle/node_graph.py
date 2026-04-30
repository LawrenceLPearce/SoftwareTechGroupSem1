import pygame


class Node:
    def __init__(self, row, col, cell_size, h_offset=0, v_offset=0, gap=2):
        self.row = row
        self.col = col
        self.neighbours = []  # up to 4, populated once at setup
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


class Graph:
    def __init__(self, rows, cols, cell_size, h_offset=0, v_offset=0):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[Node(r, c, self.cell_size, h_offset, v_offset) for c in range(cols)] for r in range(rows)]

    def get_node(self, r, c):
        return self.grid[r][c]

    def clear_node_start(self):
        for c in self.grid:
            for node in c:
                node.is_start = False

    def clear_node_end(self):
        for c in self.grid:
            for node in c:
                node.is_end = False

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
