"""This file is the launcher for all modules in phase 1."""

import pygame
from utils import utilities
from DSP import linked_list_editor, BST_visualiser, stack_visualiser, queue_visualiser


def dsp_menu(screen: pygame.Surface):
    """return button dict for dsp menu and draw buttons on screen."""
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



def stack_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    stack_visualiser.run_stack_visualiser(screen, clock)


def queue_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    queue_visualiser.run_queue_visualiser(screen, clock)


def linked_list_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    linked_list_editor.run_linked_list_editor(screen, clock)


def binary_tree_visual(screen: pygame.Surface, clock: pygame.time.Clock):
    BST_visualiser.run_bst_menu(screen, clock)


def run_dsp_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    current_module = None
    buttons = dsp_menu(screen)

    while running:
        current_module = utilities.handle_events(buttons, current_module)

        if current_module is None:
            buttons = dsp_menu(screen)
        else:
            utilities.handle_button_click(current_module, buttons, screen)
            match current_module:
                case 'Stack Interaction':
                    stack_visual(screen, clock)
                case 'Queue Interaction':
                    queue_visual(screen, clock)
                case 'Linked List Editor':
                    linked_list_visual(screen, clock)
                case 'Binary Search Tree':
                    binary_tree_visual(screen, clock)
                case 'Back to main menu':
                    running = False

            # For demo, after module ends return to menu
            current_module = None

        clock.tick(30)

    return
