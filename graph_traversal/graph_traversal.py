# most of the code used here was from the Week 12 tutorial sheet (Task 3_1)
import pygame
import collections
from utils import utilities
from utils.config import (SECONDARY_COLOUR, HIGHLIGHT_COLOUR, HIGHLIGHT_FOUND_COLOUR, TEXT_COLOUR, FONT)

NODE_SIZE = 25
COLOUR_DEFAULT = SECONDARY_COLOUR
COLOUR_FRONTIER = HIGHLIGHT_COLOUR
COLOUR_VISITED = HIGHLIGHT_FOUND_COLOUR
COLOUR_CURRENT = pygame.Color("#ff6464")
COLOUR_EDGE = pygame.Color("#aaaaaa")

# the positions of the nodes. These are pretty much the same as task 3_1's node positions just altered.
nodes_pos = {
    'A': (350, 200),
    'B': (500, 160),
    'C': (500, 300),
    'D': (650, 200),
    'E': (750, 250),
    'F': (650, 400),
}

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
}


def draw_graph(screen, visited=set(), frontier=set(), current=None):
    # this function draws the edges first, and then the nodes.
    # nodes use colours to reflect their state (e.g. traversed, next to process, etc.)
    # inspired by task 3_1's draw_graph function

    # edge generation
    for node, neighbours in graph.items():
        x1, y1 = nodes_pos[node]
        for n in neighbours:
            x2, y2 = nodes_pos[n]
            pygame.draw.line(screen, COLOUR_EDGE, (x1, y1), (x2, y2), 2)

    # node colours
    for node, (x, y) in nodes_pos.items():
        if node == current:
            color = COLOUR_CURRENT
        elif node in visited:
            color = COLOUR_VISITED
        elif node in frontier:
            color = COLOUR_FRONTIER
        else:
            color = COLOUR_DEFAULT

        shadow_surf = pygame.Surface((NODE_SIZE * 2 + 6, NODE_SIZE * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 50), (NODE_SIZE + 3, NODE_SIZE + 3), NODE_SIZE)
        screen.blit(shadow_surf, (x - NODE_SIZE, y - NODE_SIZE + 3))

        pygame.draw.circle(screen, color, (x, y), NODE_SIZE)

        label = FONT.render(node, True, TEXT_COLOUR)
        screen.blit(label, label.get_rect(center=(x, y)))


def bfs(screen, clock, start, buttons):
    # function heavily inspired by Task 3_1, altered slightly
    visited = set()
    order = []
    queue = collections.deque([start])

    while queue:
        current = queue.popleft()
        visited.add(current)
        order.append(current)

        utilities.fill_screen(screen)
        utilities.draw_text("Graph Traversal", (320, 30), screen)
        utilities.draw_buttons(buttons, screen)
        draw_graph(screen, visited=visited, frontier=set(queue), current=current)
        _draw_order(screen, "BFS", order)
        pygame.display.flip()

        pygame.time.wait(700)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)

    return order


def dfs(screen, clock, start, buttons):
    # function functions similar to BFS, just DFS traversal instead.
    visited = set()
    order = []

    def _recurse(node):
        visited.add(node)
        order.append(node)

        utilities.fill_screen(screen)
        utilities.draw_text("Graph Traversal", (320, 30), screen)
        utilities.draw_buttons(buttons, screen)
        draw_graph(screen, visited=visited, current=node)
        _draw_order(screen, "DFS", order)
        pygame.display.flip()

        pygame.time.wait(400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        for neighbor in sorted(graph[node]):
            if neighbor not in visited:
                _recurse(neighbor)

    _recurse(start)
    return order


def _draw_order(screen, mode, order):
    # this function was added to allow the user to see the traversal order.

    small = pygame.font.SysFont(None, 28)
    order_str = ", ".join(order) if order else ""
    lbl = small.render(f"{mode} order:  {order_str}", True, TEXT_COLOUR)
    screen.blit(lbl, (220, 560))


def run_graph_visualiser(screen: pygame.Surface, clock: pygame.time.Clock):
    # this function lets user interact with nodes and activates DFS or BFS traversal searches
    buttons = {
        "BFS" : pygame.Rect(30, 150, 160, 50),
        "DFS" : pygame.Rect(30, 230, 160, 50),
        "Reset": pygame.Rect(30, 310, 160, 50),
        "Back to Menu": pygame.Rect(30, 530, 160, 50),
    }

    start_node = None # selected node
    last_order = [] # the last order of nodes from traversal
    last_mode  = None # which mode is being used (DFS or BFS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # user click on button check
                for name, (nx, ny) in nodes_pos.items():
                    if (pos[0] - nx) ** 2 + (pos[1] - ny) ** 2 <= NODE_SIZE ** 2:
                        start_node = name
                        last_order = []
                        last_mode  = None

                # main buttons
                for name, rect in buttons.items():
                    if rect.collidepoint(pos):
                        utilities.handle_button_click(name, buttons, screen)

                        if name == "BFS" and start_node:
                            last_order = bfs(screen, clock, start_node, buttons)
                            last_mode  = "BFS"

                        elif name == "DFS" and start_node:
                            last_order = dfs(screen, clock, start_node, buttons)
                            last_mode  = "DFS"

                        elif name == "Reset":
                            start_node = None
                            last_order = []
                            last_mode  = None

                        elif name == "Back to Menu":
                            running = False

        utilities.fill_screen(screen)
        utilities.draw_text("Graph Traversal", (320, 30), screen)
        utilities.draw_buttons(buttons, screen)

        # display visited state
        if last_order:
            draw_graph(screen, visited=set(last_order))
            _draw_order(screen, last_mode, last_order)
        else:
            # highlights selected start nodex
            draw_graph(screen, frontier={start_node} if start_node else set())

        pygame.display.flip()
        clock.tick(30)