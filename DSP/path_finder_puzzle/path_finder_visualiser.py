from unittest import case

import pygame

from node_graph import Node, Graph
from utils import utilities, config

pygame.init()

INSTRUCTIONS_RECT = pygame.Rect(150, 50, 600, 25)

# node calculations
# maximise the columns based on the row count to fill rect.
graph_max_area = pygame.Rect(50, 75, 800, 450)  # rect defining the maximum area that the graph can occupy
NODE_COUNT = 10
NODE_SIZE = graph_max_area.height // NODE_COUNT  # maximise the size of each node
graph_area_size = NODE_SIZE * NODE_COUNT + 1  # the new size of the graph area
GRAPH_RECT = pygame.Rect((config.WIDTH - graph_area_size) // 2,  # the rect within which graph is drawn
                         75,
                         graph_area_size,
                         graph_area_size)

MODE_INFO_AREA = pygame.Rect(700, 100, 190, 240)

def node_clicked(graph: Graph, screen: pygame.Surface, event: pygame.event.Event, node_command):
    node = graph.get_clicked_node(event)
    match node_command:
        case 'Set Start':
            set_start_clicked(node,graph, screen)
        case 'Set End':
            set_end_clicked(node,graph, screen)
        case 'Make Obstacle':
            make_obstacle_clicked(node, screen)
        case 'Clear':
            clear_clicked(node, screen)

        case _:
            return node, None

    return None, None


def set_start_clicked(selected_node: Node, graph: Graph, screen: pygame.Surface):
    if selected_node is None:
        utilities.draw_text_in_rect("Click a node below to apply!", INSTRUCTIONS_RECT, screen, clear=True)
        return "Set Start"
    else:
        graph.clear_node_start()
        selected_node.set_start_true()
        pygame.display.flip()
        return None


def set_end_clicked(selected_node: Node, graph: Graph, screen: pygame.Surface):
    if selected_node is None:
        utilities.draw_text_in_rect("Click a node below to apply!", INSTRUCTIONS_RECT, screen, clear=True)
        return "Set End"
    else:
        graph.clear_node_end()
        selected_node.set_end_true()
        pygame.display.flip()
        return None


def make_obstacle_clicked(selected_node: Node, screen: pygame.Surface):
    if selected_node is None:
        utilities.draw_text_in_rect("Click a node below to apply!", INSTRUCTIONS_RECT, screen, clear=True)
        return "Make Obstacle"
    else:
        selected_node.set_obstacle_true()
        pygame.display.flip()
        return None


def clear_clicked(selected_node: Node, screen: pygame.Surface):
    if selected_node is None:
        utilities.draw_text_in_rect("Click a node to edit, or hit Run!", INSTRUCTIONS_RECT, screen, clear=True)
        return "Clear"
    else:
        selected_node.clear_state()
        pygame.display.flip()
        return None


def draw_graph(graph: Graph, screen: pygame.Surface, highlighted_Node: Node = None):
    for col in graph.grid:
        for node in col:
            if node == highlighted_Node:
                colour = config.HIGHLIGHT_COLOUR
            elif node.is_obstacle:
                colour = config.GRAPH_OBSTACLE_COLOUR
            elif node.is_start:
                colour = config.GRAPH_START_COLOUR
            elif node.is_end:
                colour = config.GRAPH_END_COLOUR
            else:
                colour = config.SECONDARY_COLOUR

            utilities.draw_button_shadow(node.rect, screen)
            pygame.draw.rect(screen, colour, node.rect, border_radius=10)


def run_sort_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    command = None

    # innitialise the graph
    graph = Graph(NODE_COUNT, NODE_COUNT, NODE_SIZE, h_offset=GRAPH_RECT.left, v_offset=GRAPH_RECT.top)
    graph.grid[0][0].is_start = True
    graph.grid[-1][-1].is_end = True

    buttons = {
        'Set Start': pygame.Rect(10, 100, 190, 50),  # side buttons that control node state
        'Set End': pygame.Rect(10, 160, 190, 50),
        'Make Obstacle': pygame.Rect(10, 220, 190, 50),
        'Clear': pygame.Rect(10, 280, 190, 50),

        'Run!': pygame.Rect(220, 540, 150, 50),  # bottom buttons that control graph
        'Reset': pygame.Rect(390, 540, 150, 50),
        'Back': pygame.Rect(560, 540, 150, 50)}

    utilities.fill_screen(screen)
    utilities.draw_buttons(buttons, screen)
    utilities.draw_text_in_rect("Sorting Visualiser", pygame.Rect(0, 20, screen.get_width(), 20), screen)
    pygame.draw.rect(screen, 'light grey', GRAPH_RECT, border_radius=10)

    draw_graph(graph, screen)
    command = None  # overall graph controls

    node_command = None  # controlled by side buttons, manage the nodes
    selected_node = None
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and command is None:
                # check if a node was clicked first
                if GRAPH_RECT.collidepoint(event.pos):
                    selected_node, node_command = node_clicked(graph, screen, event, node_command)
                    print(selected_node)

                for name, rect in buttons.items():  # check if buttons were clicked
                    if rect.collidepoint(event.pos):

                        command = name


        if command is not None:
            utilities.handle_button_click(command, buttons, screen)

            match command:
                case 'Run!':
                    node_command = None
                    selected_node = None
                case 'Reset':
                    node_command = None
                    selected_node = None
                case 'Back':
                    return

                case 'Set Start':
                    node_command = set_start_clicked(selected_node, graph, screen)
                    selected_node = None
                case 'Set End':
                    node_command = set_end_clicked(selected_node, graph, screen)
                    selected_node = None
                case 'Make Obstacle':
                    node_command = make_obstacle_clicked(selected_node, screen)
                    selected_node = None
                case 'Clear':
                    node_command = clear_clicked(selected_node, screen)



        command = None
        # utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)

        # wipe screen and draw everything
        #utilities.fill_screen(screen)
        pygame.draw.rect(screen, 'light gray', GRAPH_RECT, border_radius=10)
        draw_graph(graph, screen, highlighted_Node=selected_node)
        utilities.draw_buttons(buttons, screen)

        if node_command is not None:
            utilities.draw_text_in_rect(f"Current Mode: \n {node_command}", MODE_INFO_AREA, screen, clear=True)

        elif selected_node is not None:
            utilities.draw_text_in_rect(f"Current Node: \n{selected_node}", MODE_INFO_AREA, screen, clear=True)
        else:
            pygame.draw.rect(screen, config.BACKGROUND_COLOUR, MODE_INFO_AREA)


        pygame.display.flip()

        clock.tick(30)


if __name__ == '__main__':
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()
    run_sort_menu(screen, clock)
