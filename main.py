import pygame
import sys

# comment

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()


def draw_text(text, pos):
    txt = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt, pos)


def main_menu():
    screen.fill((200, 200, 250))
    draw_text("Algorithm Explorer", (WIDTH // 3, 50))
    buttons = {
        'Data Structures': pygame.Rect(300, 150, 200, 50),
        'Sorting':         pygame.Rect(300, 230, 200, 50),
        'Graphs':          pygame.Rect(300, 310, 200, 50),
        'Heap':            pygame.Rect(300, 390, 200, 50),
        'Puzzles':         pygame.Rect(300, 470, 200, 50),
    }
    for text, rect in buttons.items():
        pygame.draw.rect(screen, (150, 150, 200), rect)
        draw_text(text, (rect.x + 20, rect.y + 10))
    pygame.display.flip()
    return buttons


# Placeholder functions for different modules
def data_structures_module():
    # Implement stack, queue, linked list, BST visualization here
    pass


def sorting_module():
    # Bubble sort, selection sort, merge sort visualizations
    pass


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
                data_structures_module()
            elif current_module == 'Sorting':
                sorting_module()
            elif current_module == 'Graphs':
                graphs_module()
            elif current_module == 'Heap':
                heap_module()
            elif current_module == 'Puzzles':
                puzzles_module()

            # For demo, after module ends return to menu
            current_module = None

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()