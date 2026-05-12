"""this module contains the Node class and Graph class. The Graph class implements the Node class by containing a list
of them. The Graph class contains several methods, for drawing with pygame, animation, and
an a* algorithm implementation."""
import random

import pygame

from utils import config, utilities


class Node:
    def __init__(self, row, col, cell_size, h_offset=0, v_offset=0, gap=2):
        # x, y
        self.row = row
        self.col = col

        # variables used by the a* algorithm.
        self.neighbours: list[Node] = []  # up to 4, populated once at setup
        self.parent = None  # single node, set during A*
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')

        # this rect is used when drawing the graph.
        self.rect = pygame.Rect(col * cell_size + h_offset + gap,
                                row * cell_size + v_offset + gap,
                                cell_size - gap * 2,
                                cell_size - gap * 2)

        # state variables
        self.is_start = False
        self.is_end = False
        self.is_obstacle = False

    def __str__(self):
        """return coordinates and state variables in string format"""
        return (f"({self.row},{self.col}) "
                f"\n Start: {str(self.is_start)} "
                f"\n End: {str(self.is_end)}"
                f"\n Obstacle: {str(self.is_obstacle)}")

    def clear_state(self):
        """set all three state vars to false"""
        self.is_start = False
        self.is_end = False
        self.is_obstacle = False

    def set_start_true(self):
        """set start to true and other state variables to false."""
        self.is_start = True
        self.is_end = False
        self.is_obstacle = False

    def set_end_true(self):
        """set end to true and other state variables to false."""
        self.is_start = False
        self.is_end = True
        self.is_obstacle = False

    def set_obstacle_true(self):
        """set obstacle to true and other state variables to false."""
        self.is_start = False
        self.is_end = False
        self.is_obstacle = True

    def compute_f(self):
        """compute the f value of the node for a* algorithm."""
        if self.is_obstacle:
            self.f = float('inf')
            self.h = float('inf')
            self.g = float('inf')
            return

        self.f = self.g + self.h


class Graph:
    def __init__(self, rows, cols, cell_size, screen, background_rect, h_offset=0, v_offset=0, headless=False):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[Node(r, c, self.cell_size, h_offset, v_offset) for c in range(cols)] for r in range(rows)]

        self.start_node = None
        self.end_node = None

        self.build_neighbours()

        # pygame attributes, needed for visualisation
        self.screen = screen
        self.background_rect = background_rect

        self.headless = headless

        self.total_routes = 0
        self.is_running = False

    def __str__(self):
        string = ""

        for c in self.grid:
            for node in c:
                string = f"{string} \n {node}"

        return string

    def get_node(self, r, c):
        """return a Node instance at the given coordinates"""
        return self.grid[r][c]

    def clear_node_start(self):
        """remove start node and update the Node instance"""
        if self.start_node is not None:
            self.start_node.is_start = False
            self.start_node = None

    def clear_node_end(self):
        """remove end node and update the Node instance"""
        if self.end_node is not None:
            self.end_node.is_end = False
            self.end_node = None

    def set_start_node(self, node: Node):
        """save start node and update the Node instance"""
        self.clear_node_start()
        self.start_node = node
        self.start_node.set_start_true()

    def set_end_node(self, node: Node):
        """save end node and update the Node instance"""
        self.clear_node_end()
        self.end_node = node
        self.end_node.set_end_true()

    def clear_node_state(self, node: Node):
        """clear node of its state and remove from graph if required"""
        node.clear_state()

        if node == self.start_node:
            self.clear_node_start()
        elif node == self.end_node:
            self.clear_node_end()

    def build_neighbours(self):
        """iteratively create all the nodes in the graph. Run on initialisation."""
        for r in range(self.rows):
            for c in range(self.cols):
                node = self.grid[r][c]
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up down left right
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        node.neighbours.append(self.grid[nr][nc])

    def get_clicked_node(self, event: pygame.event.Event):
        """return a Node instance given a mouse click event"""

        # iterate over every node and check the rect collision
        for c in self.grid:
            for node in c:
                if node.rect.collidepoint(event.pos):
                    return node

        return None

    @staticmethod
    def manhattan_distance(node1, node2):
        """compute the manhattan distance between two nodes"""
        return abs(node1.row - node2.row) + abs(node1.col - node2.col)

    @staticmethod
    def priority_f_queue_insert(node_list: list[Node], node: Node):
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

    def draw_graph(self, highlighted_nodes: list[Node] = None, buttons=None, speed=0):
        """draw every node in the graph. Change node colour to match state."""
        pygame.draw.rect(self.screen, 'light gray', self.background_rect, border_radius=10)
        text=""
        if highlighted_nodes is None:
            highlighted_nodes = []

        for col in self.grid:
            for node in col:
                if node in highlighted_nodes:
                    colour = config.HIGHLIGHT_COLOUR
                    text=""
                elif node.is_obstacle:
                    colour = config.GRAPH_OBSTACLE_COLOUR
                elif node.is_start:
                    colour = config.GRAPH_START_COLOUR
                    text = "S"
                elif node.is_end:
                    colour = config.GRAPH_END_COLOUR
                    text="E"
                else:
                    colour = config.SECONDARY_COLOUR
                    text=""

                utilities.draw_button_shadow(node.rect, self.screen)
                pygame.draw.rect(self.screen, colour, node.rect, border_radius=10)
                utilities.draw_text_in_rect(text, node.rect, self.screen)

        # detect cancel pressed
        if buttons:
            # wipe button background
            for rect in buttons.values():
                pygame.draw.rect(self.screen, config.BACKGROUND_COLOUR, rect)
            utilities.draw_buttons(buttons, self.screen, colour=config.ERROR_COLOUR)
            pygame.display.flip()
            command = utilities.delay_with_exit_detection(speed, buttons=buttons)
            if command is not None:
                utilities.handle_button_click(command, buttons, self.screen, colour=config.ERROR_COLOUR)
            if command == "Cancel":
                self.is_running = False


    def connect_nodes(self, first_node: Node, second_node: Node):
        """Draw red line between two given nodes. If either node is start or end, draw circle in it."""
        if first_node.is_start or first_node.is_end:
            pygame.draw.circle(self.screen, config.HIGHLIGHT_DELETE_COLOUR, first_node.rect.center, 5)

        elif second_node.is_start or second_node.is_end:
            pygame.draw.circle(self.screen, config.HIGHLIGHT_DELETE_COLOUR, second_node.rect.center, 5)

        pygame.draw.line(self.screen, config.HIGHLIGHT_DELETE_COLOUR, first_node.rect.center,
                         second_node.rect.center, 2)

    def animate_node_path(self, path: list[Node]):
        """connect all nodes in path with delay to create animated effect."""
        for i in range(len(path) - 1):
            first_node = path[i]
            second_node = path[i + 1]

            self.connect_nodes(first_node, second_node)

            utilities.delay_with_exit_detection(25)
            pygame.display.flip()

    def static_node_path(self, path: list[Node]):
        """connect all nodes in path."""
        for i in range(len(path) - 1):
            first_node = path[i]
            second_node = path[i + 1]

            self.connect_nodes(first_node, second_node)

        pygame.display.flip()

    def reconstruct_path(self):
        """trace from the end node to start node, and return inverted list."""
        path = []
        current = self.end_node

        while current is not None:
            path.append(current)
            current = current.parent

        # invert path and return
        return path[::-1]
    def clear_node_states(self):
        """clear all node states that relate to a* search / heuristics"""
        for row in self.grid:
            for node in row:
                node.parent = None
                node.g = float('inf')
                node.h = 0
                node.f = float('inf')

    def a_star_search(self):
        """perform a* search on graph. Return Path."""
        # Reset all node state before search
        for row in self.grid:
            for node in row:
                node.parent = None
                node.g = float('inf')
                node.h = 0
                node.f = float('inf')

        if not self.is_running:
            return [] # search has been cancelled

        open_list: list[Node] = [self.start_node]
        closed_list: list[Node] = []

        self.start_node.g = 0
        self.start_node.h = self.manhattan_distance(self.start_node, self.end_node)
        self.start_node.compute_f()

        while len(open_list) > 0:

            current_node = open_list[0]  # this list is sorted at insertion time, so lowest f value is always at [0]

            if current_node.is_end:  # goal found
                return self.reconstruct_path()

            # move node to other list
            open_list.pop(0)
            closed_list.append(current_node)

            for node in current_node.neighbours:
                if node in closed_list or node.is_obstacle:  # don't repeat nodes
                    continue

                tentative_g = current_node.g + self.manhattan_distance(current_node, node)

                if node in open_list:
                    if tentative_g >= node.g:
                        continue
                    # better path found - remove so we can re-insert at correct position
                    open_list.remove(node)

                # the path is better
                node.parent = current_node
                node.g = tentative_g
                node.h = self.manhattan_distance(node, self.end_node)
                node.compute_f()
                self.priority_f_queue_insert(open_list, node)

            if self.headless:
                continue
            self.draw_graph(closed_list)
            pygame.display.flip()

        return None


    def count_all_routes(self, current_node: Node, closed_set: set[Node], buttons=None, counter_rect=None):
        if not self.is_running: # count was cancelled
            return

        if not self.headless:
            self.draw_graph(list(closed_set), buttons=buttons)
            if counter_rect is not None:
                utilities.draw_text_in_rect(f"Total Paths: {self.total_routes}", counter_rect, self.screen, clear=True)

            pygame.display.flip()
        for node in current_node.neighbours:
            if node in closed_set or node.is_obstacle:
                continue
            elif node.is_end:
                self.total_routes += 1
            else:
                closed_set.add(current_node)
                self.count_all_routes(node, closed_set, buttons=buttons, counter_rect=counter_rect)
                closed_set.remove(current_node)  # backtrack


        # copy list
        # go to all neighbors that are not in closed_list
        # if all are in closed list, then return 0
        # if node is obstical, add it to closed list
        # if node is end node, return 1

    def run_route_count(self, buttons=None, counter_rect=None):
        self.is_running = True
        self.total_routes = 0
        start_set = {self.start_node}
        self.count_all_routes(self.start_node, start_set, buttons=buttons, counter_rect=counter_rect)

        if self.total_routes > 0:
            # animate a path
            path = self.random_route(self.start_node, start_set) + [self.end_node]
            if not self.headless:
                self.animate_node_path(path)

        else:
            path = []
        return self.total_routes, path

    def random_route(self, current_node: Node, closed_set: set[Node]) -> list[Node] | None:
        """find a random route"""
        neighbours = list(current_node.neighbours)
        random.shuffle(neighbours)

        for node in neighbours:
            if node in closed_set or node.is_obstacle:
                continue
            elif node.is_end:
                return [current_node, node]

            closed_set.add(current_node)
            result = self.random_route(node, closed_set)
            closed_set.remove(current_node)

            if result:
                return [current_node] + result

        return None  # dead end, backtrack


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    graph = Graph(5, 5, 4, screen, pygame.rect.Rect(0, 0, 800, 600))

    graph.set_start_node(graph.get_node(0, 0))
    graph.set_end_node(graph.get_node(-1, -1))
    starting_set: set = {graph.start_node}
    graph.run_route_count()
    print(graph.total_routes)


if __name__ == '__main__':
    main()
