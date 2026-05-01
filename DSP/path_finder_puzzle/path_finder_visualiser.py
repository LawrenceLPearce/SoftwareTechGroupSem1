import pygame

from node_graph import Node, Graph
from utils import utilities, config

pygame.init()

INSTRUCTIONS_RECT = pygame.Rect(150, 50, 600, 25)

# node calculations
# maximise the columns based on the row count to fill rect.
graph_max_area = pygame.Rect(50, 75, 800, 450)  # rect defining the maximum area that the graph can occupy
NODE_COUNT = 15
NODE_SIZE = graph_max_area.height // NODE_COUNT  # maximise the size of each node
graph_area_size = NODE_SIZE * NODE_COUNT + 1  # the new size of the graph area
GRAPH_RECT = pygame.Rect((config.WIDTH - graph_area_size) // 2,  # the rect within which graph is drawn
                         75,
                         graph_area_size,
                         graph_area_size)

# rectangle where information regarding the current node / mode will be printed
MODE_INFO_AREA = pygame.Rect(700, 100, 190, 240)


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
        # selected_node.clear_state()
        pygame.display.flip()
        return None



def run_astar(graph: Graph, screen: pygame.Surface, clock: pygame.time.Clock):
    # check the route is valid
    print(graph.start_node)
    if graph.start_node is None:
        utilities.pop_up_message(screen, "You must define a start Node", error=True)
        return []

    if graph.end_node is None:
        utilities.pop_up_message(screen, "You must define a end Node", error=True)
        return []

    path = graph.a_star_search()

    if path is None:
        utilities.pop_up_message(screen, "No valid path was found", error=True)
        return []

    graph.animate_node_path(path)

    return path


def draw_graph(graph: Graph, screen: pygame.Surface, highlighted_node: Node = None):
    """iteratively draw every node in the graph"""
    for col in graph.grid:
        for node in col:
            if node == highlighted_node:
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

    # innitialise the graph
    graph = Graph(NODE_COUNT, NODE_COUNT, NODE_SIZE, screen, GRAPH_RECT, h_offset=GRAPH_RECT.left,
                  v_offset=GRAPH_RECT.top)
    graph.set_start_node(graph.grid[0][0])
    graph.set_end_node(graph.grid[-1][-1])

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

    # draw_graph(graph, screen)
    # graph.draw_graph(screen)
    command = None  # overall graph controls

    node_command = None  # controlled by side buttons, manage the nodes
    selected_node = None

    found_path = []
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
                    found_path = run_astar(graph, screen, clock)
                case 'Reset':
                    node_command = None
                    selected_node = None
                    found_path = []
                    graph = Graph(NODE_COUNT, NODE_COUNT, NODE_SIZE, screen, GRAPH_RECT, h_offset=GRAPH_RECT.left,
                                  v_offset=GRAPH_RECT.top)
                    graph.set_start_node(graph.grid[0][0])
                    graph.set_end_node(graph.grid[-1][-1])
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
                    node_command = clear_clicked(selected_node, graph, screen)

        command = None
        # utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)

        # wipe screen and draw everything
        utilities.fill_screen(screen)
        utilities.draw_text_in_rect("A* Grid Search", pygame.Rect(0, 20, screen.get_width(), 20), screen)

        if node_command is not None:
            text = f"Current Mode:\n{node_command}"
        elif selected_node is not None:
            text = f"Current Node:\n{selected_node}"
        else:
            text = ""

        utilities.draw_text_in_rect(text, MODE_INFO_AREA, screen)
        utilities.draw_text_in_rect("Up, down, left, right, NO diagonals", INSTRUCTIONS_RECT, screen)

        # pygame.draw.rect(screen, 'light gray', GRAPH_RECT, border_radius=10)
        # draw_graph(graph, screen, highlighted_node=selected_node)
        graph.draw_graph(highlighted_nodes=[selected_node])

        utilities.draw_buttons(buttons, screen)
        graph.static_node_path(found_path)

        pygame.display.flip()
        clock.tick(30)


def main():
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()
    run_sort_menu(screen, clock)


if __name__ == '__main__':
    main()
