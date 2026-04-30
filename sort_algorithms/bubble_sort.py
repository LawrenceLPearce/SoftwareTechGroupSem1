import pygame
import random
from utils import utilities, config

# constants
# rectanlges defining where some things go
ARRAY_RECT = pygame.Rect(50, 200, 800, 250)  # rect defining the space the animation can occupy
INSTRUCTIONS_RECT = pygame.Rect(50, 50, 800, 150)
# bar definitions
BAR_GAP = 2
ARRAY_SIZE = 20
BAR_WIDTH = ARRAY_RECT.width // ARRAY_SIZE



def draw_array(array: list, screen: pygame.Surface, colour_positions=None, bar_width=BAR_WIDTH):
    pygame.draw.rect(screen, config.BACKGROUND_COLOUR, ARRAY_RECT)

    for i, val in enumerate(array):
        color = config.SECONDARY_COLOUR
        if colour_positions and i in colour_positions['compare']:
            color = config.HIGHLIGHT_DELETE_COLOUR
        if colour_positions and i in colour_positions['swap']:
            color = config.HIGHLIGHT_COLOUR
        pygame.draw.rect(screen, color, (ARRAY_RECT.left + (i * bar_width),
                                         ARRAY_RECT.bottom - val,
                                         bar_width - BAR_GAP,
                                         val))
    pygame.display.flip()

def bubble_sort_visualiser(array: list, screen: pygame.Surface):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            draw_array(array, screen, {'compare': [j, j + 1], 'swap': []})
            pygame.time.wait(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if array[j] > array[j + 1]: # swap case. Redraw array with highlighted colours
                array[j], array[j + 1] = array[j + 1], array[j]  # swap
                draw_array(array, screen, {'compare': [], 'swap': [j, j + 1]})
                pygame.time.wait(50)

    draw_array(array, screen)

def selection_sort_visualiser(array: list, screen: pygame.Surface):
    n = len(array)
    for i in range(n):
        min_idx = i # smallest element found so far
        for j in range(i + 1, n): # unsorted side

            # here we are technically comparing both, however pass min_idx as 'swap' to get different colour
            draw_array(array, screen, {'compare': [j], 'swap': [min_idx]})
            pygame.time.wait(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if array[j] < array[min_idx]: # new minimum case
                min_idx = j

        if min_idx != i:  # swap case. Redraw array with highlighted colours
            array[i], array[min_idx] = array[min_idx], array[i]
            draw_array(array, screen, {'compare': [], 'swap': [i, min_idx]})
            pygame.time.wait(50)

    draw_array(array, screen)

def generate_random_array(min_int, max_int, size=ARRAY_SIZE) -> list:
    return [random.randint(min_int, max_int) for _ in range(size)]

def run_sort_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    command = None
    array = generate_random_array(10, 200)
    buttons = {
        'Bubble': pygame.Rect(120, 480, 150, 50),  # row 1
        'Selection': pygame.Rect(290, 480, 150, 50),
        'Randomise': pygame.Rect(460, 480, 150, 50),
        'Back': pygame.Rect(630, 480, 150, 50),}

    instructions = {
        None: "Select a sort algorithm, randomise the array, or go back",
        'Bubble': "Red: comparing adjacent pair  |  Yellow: swap occurring",
        'Selection': "Yellow: current minimum  |  Red: comparing against minimum",
        'Reset': "Array has been reset",
        'Back': "Exiting..."
    }

    utilities.fill_screen(screen)
    utilities.draw_buttons(buttons, screen)
    utilities.draw_text_in_rect("Sorting Visualiser", pygame.Rect(0, 20, screen.get_width(), 20), screen)
    draw_array(array, screen)

    while running:

        command = utilities.handle_events(buttons, command)

        if command is not None:
            utilities.handle_button_click(command, buttons, screen)

        match command:
            case 'Bubble':
                utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)
                bubble_sort_visualiser(array, screen)
                utilities.draw_buttons(buttons, screen) # make button pop back up
            case 'Selection':
                utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)
                selection_sort_visualiser(array, screen)
                utilities.draw_buttons(buttons, screen)
            case 'Randomise':
                array = generate_random_array(10, 200)
                utilities.draw_buttons(buttons, screen)
                draw_array(array, screen)
            case 'Back':
                return

        command = None
        utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)

        # wipe screen and draw everything





        pygame.display.flip()

        clock.tick(30)

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()
    run_sort_menu(screen, clock)

if __name__ == '__main__':
    main()