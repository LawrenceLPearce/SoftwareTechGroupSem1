"""This file is the launcher for all modules in phase 1."""

import pygame
from utils import utilities
from DSP import linked_list_editor, BST_visualiser, stack_visualiser, queue_visualiser



def dsp_menu(screen: pygame.Surface):
    left_lineup = screen.get_width() // 2 - 100

    utilities.fill_screen(screen)
    utilities.draw_text("Data Structure Playground", (left_lineup, 50), screen)
    buttons = {
        'Stack Interaction': pygame.Rect(left_lineup, 150, 250, 50),
        'Queue Interaction': pygame.Rect(left_lineup, 230, 250, 50),
        'Linked List Editor': pygame.Rect(left_lineup, 310, 250, 50),
        'Binary Search Tree': pygame.Rect(left_lineup, 390, 250, 50),
        'Back to main menu': pygame.Rect(left_lineup, 470, 250, 50),
    }
    utilities.draw_buttons(buttons, screen)
    pygame.display.flip()
    return buttons


# placeholder functions that will call the separate files
def stack_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    stack_visualiser.run_stack_visualiser(screen, clock)
    # ^ added this, will run the stack visualiser - Nathan


def queue_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    queue_visualiser.run_queue_visualiser(screen, clock)
    # ^ added this, will run the queue visualiser - Nathan


def linked_list_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    linked_list_editor.run_linked_list_editor(screen, clock)


def binary_tree_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    BST_visualiser.run_bst_menu(screen, clock)


def run_dsp_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    current_module = None
    buttons = dsp_menu(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
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
                utilities.handle_button_click("Stack Interaction", buttons, screen)
                stack_visual(screen, clock)
            elif current_module == 'Queue Interaction':
                utilities.handle_button_click("Queue Interaction", buttons, screen)
                queue_visual(screen, clock)
            elif current_module == 'Linked List Editor':
                utilities.handle_button_click("Linked List Editor", buttons, screen)
                linked_list_visual(screen, clock)
            elif current_module == 'Binary Search Tree':
                utilities.handle_button_click("Binary Search Tree", buttons, screen)
                binary_tree_visual(screen, clock)
            elif current_module == 'Back to main menu':
                utilities.handle_button_click("Back to main menu", buttons, screen)
                running = False

            # For demo, after module ends return to menu
            current_module = None

        clock.tick(30)

    return
