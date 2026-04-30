import pygame
from utils import utilities, config
from DSP import dsp_playground
from sort_algorithms import bubble_sort
pygame.init()

WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
# todo: verify its ok to change the width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = config.FONT
clock = pygame.time.Clock()


def main_menu():
    left_lineup = WIDTH // 2 - 100

    utilities.fill_screen(screen)
    utilities.draw_text("Algorithm Explorer", (left_lineup, 50), screen)
    buttons = {
        'Data Structures': pygame.Rect(left_lineup, 150, 220, 50),
        'Sorting': pygame.Rect(left_lineup, 230, 220, 50),
        'Graphs': pygame.Rect(left_lineup, 310, 220, 50),
        'Heap': pygame.Rect(left_lineup, 390, 220, 50),
        'Puzzles': pygame.Rect(left_lineup, 470, 220, 50),
    }
    utilities.draw_buttons(buttons, screen)
    pygame.display.flip()
    return buttons


# Placeholder functions for different modules
def data_structures_module():
    # Implement stack, queue, linked list, BST visualization here
    dsp_playground.run_dsp_menu(screen, clock)


def sorting_module():
    # Bubble sort, selection sort, merge sort visualizations
    bubble_sort.run_sort_menu(screen, clock)


def graphs_module():
    # BFS, DFS visualization with interactive graph
    pass


def heap_module():
    # Heap insertion and extraction visualization
    pass


def puzzles_module():
    # Pathfinding, event simulation, DP puzzles
    pass


def main():
    running = True
    current_module = None
    buttons = main_menu()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_module is None:
                pos = event.pos
                for name, rect in buttons.items():
                    if rect.collidepoint(pos):
                        current_module = name

        if current_module is None:
            buttons = main_menu()
        else:
            if current_module == 'Data Structures':
                utilities.handle_button_click("Data Structures", buttons, screen)
                data_structures_module()
            elif current_module == 'Sorting':
                utilities.handle_button_click("Sorting", buttons, screen)
                sorting_module()
            elif current_module == 'Graphs':
                utilities.handle_button_click("Graphs", buttons, screen)
                graphs_module()
            elif current_module == 'Heap':
                utilities.handle_button_click("Heap", buttons, screen)
                heap_module()
            elif current_module == 'Puzzles':
                utilities.handle_button_click("Puzzles", buttons, screen)
                puzzles_module()

            # For demo, after module ends return to menu
            current_module = None

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
