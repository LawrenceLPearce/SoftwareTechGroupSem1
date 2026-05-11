"""This file is the launcher for all modules in phase 3."""

import pygame
from utils import utilities
from puzzles import path_finder_visualiser, event_queue_simulator, coin_change

def puzzle_menu(screen: pygame.Surface):
    """return button dict for puzzle menu and draw buttons on screen."""
    left_lineup = screen.get_width() // 2 - 100

    utilities.fill_screen(screen)
    utilities.draw_text("Puzzle Challenges", (left_lineup, 50), screen)
    buttons = {
        'Path Finder': pygame.Rect(left_lineup, 150, 250, 50),
        'Event Queue': pygame.Rect(left_lineup, 230, 250, 50),
        'Path Counter': pygame.Rect(left_lineup, 310, 250, 50),
        'Coin Change': pygame.Rect(left_lineup, 390, 250, 50),
        'Back to main menu': pygame.Rect(left_lineup, 470, 250, 50),
    }
    utilities.draw_buttons(buttons, screen)
    pygame.display.flip()
    return buttons


def path_finder(screen: pygame.Surface, clock: pygame.time.Clock):
    path_finder_visualiser.run_sort_menu(screen, clock, buttons={
        'Set Start': pygame.Rect(10, 100, 190, 50),  # side buttons that control node state
        'Set End': pygame.Rect(10, 160, 190, 50),
        'Make Obstacle': pygame.Rect(10, 220, 190, 50),
        'Clear': pygame.Rect(10, 280, 190, 50),

        'Run!': pygame.Rect(220, 540, 150, 50),  # bottom buttons that control graph
        'Reset': pygame.Rect(390, 540, 150, 50),
        'Back': pygame.Rect(560, 540, 150, 50)},
                                         graph_size=11,
                                         title_text="A* Algorithm Path Finder",
                                         description_text="Path can go left, right, up, down.")


def event_queue(screen: pygame.Surface, clock: pygame.time.Clock):
    event_queue_simulator.run_event_queue_simulator(screen, clock)


def path_counter(screen: pygame.Surface, clock: pygame.time.Clock):
    path_finder_visualiser.run_sort_menu(screen, clock, buttons={
        'Set Start': pygame.Rect(10, 100, 190, 50),  # side buttons that control node state
        'Set End': pygame.Rect(10, 160, 190, 50),
        'Make Obstacle': pygame.Rect(10, 220, 190, 50),
        'Clear': pygame.Rect(10, 280, 190, 50),

        'Count Paths': pygame.Rect(220, 540, 150, 50),  # bottom buttons that control graph
        'Reset': pygame.Rect(390, 540, 150, 50),
        'Back': pygame.Rect(560, 540, 150, 50)},
                                         graph_size=5,
                                         title_text="Count Paths in Grid",
                                         description_text="Path can go left, right, up or down")


def coin_simulator(screen: pygame.Surface, clock: pygame.time.Clock):
    coin_change.run_coin_change(screen, clock)


def run_puzzle_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    current_module = None
    buttons = puzzle_menu(screen)

    while running:
        current_module = utilities.handle_events(buttons, current_module)

        if current_module is None:
            buttons = puzzle_menu(screen)
        else:
            utilities.handle_button_click(current_module, buttons, screen)
            match current_module:
                case 'Path Finder':
                    path_finder(screen, clock)
                case 'Event Queue':
                    event_queue(screen, clock)
                case 'Path Counter':
                    path_counter(screen, clock)
                case 'Coin Change':
                    coin_simulator(screen, clock)
                case 'Back to main menu':
                    running = False

            # For demo, after module ends return to menu
            current_module = None

        clock.tick(30)

    return
