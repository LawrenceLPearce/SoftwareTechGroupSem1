"""This program contains functions to implement and run Graph, allowing users to set node states,
make obstacle and run a* search."""
import random
from typing import Dict

import pygame
from puzzles.node_graph import Node, Graph
from utils import utilities, config

pygame.init()

INSTRUCTIONS_RECT = pygame.Rect(150, 50, 600, 25)

# node calculations
# maximise the columns based on the row count to fill rect.



def node_clicked(graph: Graph, screen: pygame.Surface, event: pygame.event.Event, node_command):
    """set the node to the current command, if there is no command then return the Node to be highlighted"""
    node = graph.get_clicked_node(event)
    command = None
    match node_command:
        case 'Set Start':
            set_start_clicked(node, graph, screen)
        case 'Set End':
            set_end_clicked(node, graph, screen)
        case 'Make Obstacle':
            command = 'Make Obstacle'
            make_obstacle_clicked(node, screen)
        case 'Clear':
            clear_clicked(node, graph, screen)

        case _:
            return node, None

    return None, command


def set_start_clicked(selected_node: Node, graph: Graph, screen: pygame.Surface):
    """If the node is selected, set the start node to that node, otherwise set the mode to start"""
    if selected_node is None:
        utilities.draw_text_in_rect("Click a node below to apply!", INSTRUCTIONS_RECT, screen, clear=True)
        return "Set Start"
    else:
        graph.set_start_node(selected_node)
        pygame.display.flip()
        return None


def set_end_clicked(selected_node: Node, graph: Graph, screen: pygame.Surface):
    """set Node as end if node is not None, otherwise set mode to end."""
    if selected_node is None:
        utilities.draw_text_in_rect("Click a node below to apply!", INSTRUCTIONS_RECT, screen, clear=True)
        return "Set End"
    else:
        graph.set_end_node(selected_node)
        pygame.display.flip()
        return None


def make_obstacle_clicked(selected_node: Node, screen: pygame.Surface):
    """set Node as obstacle if node is not None, otherwise set mode to obstacle"""
    if selected_node is None:
        utilities.draw_text_in_rect("Click a node below to apply!", INSTRUCTIONS_RECT, screen, clear=True)
        return "Make Obstacle"
    else:
        selected_node.set_obstacle_true()
        pygame.display.flip()
        return "Make Obstacle"


def clear_clicked(selected_node: Node, graph: Graph, screen: pygame.Surface):
    """Clear node or mode. Return current mode"""
    if selected_node is None:
        utilities.draw_text_in_rect("Click a node to edit, or hit Run!", INSTRUCTIONS_RECT, screen, clear=True)
        return "Clear"
    else:
        graph.clear_node_state(selected_node)
        pygame.display.flip()
        return None



def run_astar(graph: Graph, screen: pygame.Surface):
    """validate graph and perform a* search."""
    # check the route is valid
    if graph.start_node is None:
        utilities.pop_up_message(screen, "You must define a start Node", error=True)
        return []

    if graph.end_node is None:
        utilities.pop_up_message(screen, "You must define a end Node", error=True)
        return []
    graph.is_running = True
    path = graph.a_star_search()

    if path is None:
        utilities.pop_up_message(screen, "No valid path was found", error=True)
        return []

    graph.animate_node_path(path)

    return path

def count_paths(graph: Graph, description_rect):
    buttons = {"Cancel": pygame.Rect((config.WIDTH -200), 100, 100, 50)}

    total_routes, path = graph.run_route_count(buttons=buttons,
                                               counter_rect=description_rect)

    return path, f"Total routes: {total_routes}"


def run_sort_menu(screen: pygame.Surface, clock: pygame.time.Clock, buttons:Dict, graph_size, title_text, description_text):
    graph_max_area = pygame.Rect(50, 75, 800, 450)  # working rect defining the maximum area that the graph can occupy

    node_size = graph_max_area.height // graph_size  # maximise the size of each node
    graph_area_size = node_size * graph_size + 1  # the new size of the graph area
    graph_rect = pygame.Rect((config.WIDTH - graph_area_size) // 2,  # the rect within which graph is drawn
                             75,
                             graph_area_size,
                             graph_area_size)



    # rectangle where information regarding the current node / mode will be printed
    MODE_INFO_AREA = pygame.Rect(700, 100, 190, 240)
    running = True

    # initialise the graph
    graph = Graph(graph_size, graph_size, node_size, screen, graph_rect, h_offset=graph_rect.left,
                  v_offset=graph_rect.top)
    graph.set_start_node(graph.get_node(0, 0))
    graph.set_end_node(graph.get_node(-1, -1))
    # add three random obsticles
    for i in range(3):

        graph.get_node(random.randint(1, graph_size-2), random.randint(1, graph_size-2)).set_obstacle_true()



    command = None  # overall graph controls
    node_command = None  # controlled by side buttons, manage the nodes
    selected_node = None # current node that node command will be applied to
    found_path = [] # result of the a* search. Empty until search is performed.


    # main program loop
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and command is None:
                # check if a node was clicked first
                if graph_rect.collidepoint(event.pos):
                    selected_node, node_command = node_clicked(graph, screen, event, node_command)

                for name, rect in buttons.items():  # check if buttons were clicked
                    if rect.collidepoint(event.pos):
                        command = name

        if command is not None:
            utilities.handle_button_click(command, buttons, screen)

            match command:
                # control commands for A*
                case 'Run!':
                    node_command = None
                    selected_node = None
                    found_path = run_astar(graph, screen)
                case 'Reset':
                    node_command = None
                    selected_node = None
                    found_path = []
                    graph = Graph(graph_size, graph_size, node_size, screen, graph_rect, h_offset=graph_rect.left,
                                  v_offset=graph_rect.top)
                    graph.set_start_node(graph.grid[0][0])
                    graph.set_end_node(graph.grid[-1][-1])
                case 'Back':
                    return

                # node commands (used in both menus)
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
                    node_command = clear_clicked(selected_node, graph, screen)

                # count command (used in counting menu)
                case 'Count Paths':
                    utilities.draw_text_in_rect("Current Mode: \n Count", MODE_INFO_AREA, screen)
                    found_path, description_text = count_paths(graph, INSTRUCTIONS_RECT)


        command = None

        # wipe screen and draw everything
        utilities.fill_screen(screen)
        utilities.draw_text_in_rect(title_text, pygame.Rect(0, 20, screen.get_width(), 20), screen)

        # display node stats / current mode info
        if node_command is not None:
            text = f"Current Mode:\n{node_command}"
        elif selected_node is not None:
            text = f"Current Node:\n{selected_node}"
        else:
            text = ""

        utilities.draw_text_in_rect(text, MODE_INFO_AREA, screen)
        utilities.draw_text_in_rect(description_text, INSTRUCTIONS_RECT, screen)

        graph.draw_graph(highlighted_nodes=[selected_node])

        utilities.draw_buttons(buttons, screen)
        graph.static_node_path(found_path)

        pygame.display.flip()
        clock.tick(30)




def main():
    """Launch the graph"""
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()
    run_sort_menu(screen, clock, buttons = {
        'Set Start': pygame.Rect(10, 100, 190, 50),  # side buttons that control node state
        'Set End': pygame.Rect(10, 160, 190, 50),
        'Make Obstacle': pygame.Rect(10, 220, 190, 50),
        'Clear': pygame.Rect(10, 280, 190, 50),

        'Count Paths': pygame.Rect(220, 540, 150, 50),  # bottom buttons that control graph
        'Reset': pygame.Rect(390, 540, 150, 50),
        'Back': pygame.Rect(560, 540, 150, 50)}, graph_size=5, title_text="Count Paths in Grid",
                  description_text="Path can go left, right, up or down")


if __name__ == '__main__':
    main()
