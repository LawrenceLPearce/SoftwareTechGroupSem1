"""This file is the launcher for all modules in phase 1."""

import pygame
import utilities


def dsp_menu(screen: pygame.Surface):
    utilities.fill_screen(screen)
    utilities.draw_text("Algorithm Explorer", (screen.get_width() // 3, 50), screen)
    buttons = {
        'Stack Interaction': pygame.Rect(260, 150, 250, 50),
        'Queue Interaction': pygame.Rect(260, 230, 250, 50),
        'Linked List Editor': pygame.Rect(260, 310, 250, 50),
        'Binary Search Tree': pygame.Rect(260, 390, 250, 50),
        'Back to main menu': pygame.Rect(260, 470, 250, 50),
    }
    utilities.draw_buttons(buttons, screen)
    pygame.display.flip()
    return buttons


# placeholder functions that will call the separate files
def stack_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    pass


def queue_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    pass


def linked_list_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    pass


def binary_tree_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    pass


def run_dsp_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    current_module = None
    buttons = dsp_menu(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_module is None:
                pos = event.pos
                for name, rect in buttons.items():
                    if rect.collidepoint(pos):
                        current_module = name

        if current_module is None:
            buttons = dsp_menu(screen)
        if current_module is None:
            buttons = dsp_menu(screen)
        else:
            if current_module == 'Stack Interaction':
                stack_visual(screen, clock)
            elif current_module == 'Queue Interaction':
                queue_visual(screen, clock)
            elif current_module == 'Linked List Editor':
                linked_list_visual(screen, clock)
            elif current_module == 'Binary Search Tree':
                binary_tree_visual(screen, clock)
            elif current_module == 'Back to main menu':
                running = False

            # For demo, after module ends return to menu
            current_module = None

        clock.tick(30)

    return