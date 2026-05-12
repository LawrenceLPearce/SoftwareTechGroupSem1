"""This program visualises 3 sort algorithms: bubble, merge and selection. """
import pygame
import random
from utils import utilities, config

# constants
# rectangles defining where elements go on the screen
ARRAY_RECT = pygame.Rect(50, 175, 800, 250)  # rect defining the space the animation can occupy
INSTRUCTIONS_RECT = pygame.Rect(50, 50, 800, 150)
# bar size definitions
BAR_GAP = 2

CANCEL_BUTTON_RECT = pygame.Rect((config.WIDTH // 2) - 50, 175, 100, 50)


def draw_array(array: list, screen: pygame.Surface, colour_positions=None, array_rect=ARRAY_RECT, speed=0,
               buttons=None):
    """draw visual representation of an array, by varying bar height by value. Can take dict colour_positions,
        which defines which elements are currently being compared or swapped"""
    bar_width = array_rect.width // len(array)
    pygame.draw.rect(screen, config.BACKGROUND_COLOUR, ARRAY_RECT)  # fill background

    bar_gap = max(bar_width // 10, 1)
    for i, val in enumerate(array):
        # calculate colour
        color = config.SECONDARY_COLOUR
        if colour_positions and i in colour_positions['compare']:
            color = config.HIGHLIGHT_DELETE_COLOUR
        if colour_positions and i in colour_positions['swap']:
            color = config.HIGHLIGHT_COLOUR
        if colour_positions and i in colour_positions['block']:
            color = config.BLOCK_HIGHLIGHT_COLOUR
        if colour_positions and i in colour_positions['sorted']:
            color = config.HIGHLIGHT_FOUND_COLOUR

        pygame.draw.rect(screen, color, (ARRAY_RECT.left + (i * bar_width),
                                         ARRAY_RECT.bottom - val,
                                         bar_width - bar_gap,
                                         val))

    if buttons:
        # wipe button background
        for rect in buttons.values():
            pygame.draw.rect(screen, config.BACKGROUND_COLOUR, rect)
        utilities.draw_buttons(buttons, screen, colour=config.ERROR_COLOUR)

    pygame.display.flip()

    # handle button pressed
    command = utilities.delay_with_exit_detection(speed, buttons=buttons)
    if command is not None:
        utilities.handle_button_click(command, buttons, screen, colour=config.ERROR_COLOUR)

    return command


def bubble_sort_visualiser(array: list, screen: pygame.Surface, animation_speed, buttons):
    """ Bubble sort implementation with call to visualiser. Iterative approach is used."""
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            command = draw_array(array, screen, {'compare': [j, j + 1], 'swap': [], 'block': [],
                                                 'sorted': list(range(n - i, n))},
                                 speed=animation_speed, buttons=buttons)
            if command == "Cancel":
                return  # button pressed

            if array[j] > array[j + 1]:  # swap case
                array[j], array[j + 1] = array[j + 1], array[j]
                command = draw_array(array, screen,
                                     {'compare': [], 'swap': [j, j + 1], 'block': [],
                                      'sorted': list(range(n - i, n))},
                                     speed=animation_speed, buttons=buttons)
                if command == "Cancel":
                    return

    draw_array(array, screen)


def selection_sort_visualiser(array: list, screen: pygame.Surface, animation_speed, buttons):
    """Selection sort implementation with call to visualiser. Iterative approached used."""

    n = len(array)

    # Move through each position in the array
    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):  # find smallest value
            command = draw_array(
                array,
                screen,
                {'compare': [j], 'swap': [min_idx], 'block': [], 'sorted': list(range(0, i))},
                speed=animation_speed,
                buttons=buttons
            )

            if command == "Cancel":
                return

            if array[j] < array[min_idx]:
                min_idx = j

        if min_idx != i:  # swap condition. Swap minimum.
            array[i], array[min_idx] = array[min_idx], array[i]

            command = draw_array(
                array, screen,
                {'compare': [], 'swap': [i, min_idx], 'block': [], 'sorted': list(range(0, i))},
                speed=animation_speed,
                buttons=buttons
            )

            if command == "Cancel":
                return

    # final draw
    draw_array(array, screen)


def merge(left: list, right: list, screen: pygame.Surface, array: list, start: int, animation_speed, buttons):
    """merge the two given lists such that they are sorted."""
    result = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        li = start + i
        ri = start + len(left) + j

        command = draw_array(array, screen, {'compare': [li, ri], 'swap': [], 'block': [], 'sorted': []},
                             speed=animation_speed, buttons=buttons)
        if command == "Cancel":
            return "Cancel"

        if left[i] <= right[j]:  # left is less so append
            command = draw_array(array, screen, {'compare': [], 'swap': [li], 'block': [], 'sorted': []},
                                 speed=animation_speed, buttons=buttons)

            result.append(left[i])
            i += 1

        else:  # right is less
            command = draw_array(array, screen, {'compare': [], 'swap': [ri], 'block': [], 'sorted': []},
                                 speed=animation_speed, buttons=buttons)
            result.append(right[j])
            j += 1
        if command == "Cancel":
            return "Cancel"

    result += left[i:]
    result += right[j:]
    return result


def merge_sort_iterative(array: list, screen: pygame.Surface, animation_speed, buttons):
    """Iterative merge sort implementation with call to visualiser."""
    n = len(array)
    size = 1

    while size < n:  # run for size of array
        for start in range(0, n, size * 2):

            # calculate mid, end, left, right points
            mid = min(start + size, n)
            end = min(start + size * 2, n)

            left = array[start:mid]
            right = array[mid:end]

            left_indices = list(range(start, mid))
            right_indices = list(range(mid, end))

            command = draw_array(array, screen, {'compare': [], 'swap': [], 'block': left_indices + right_indices,
                                                 'sorted': []}, speed=animation_speed, buttons=buttons)
            if command == "Cancel":
                return array

            merged = merge(left, right, screen, array, start, animation_speed, buttons)  # recurse down
            if merged == "Cancel":
                return array

            array[start:end] = merged

            # highlight the merged region as sorted
            command = draw_array(array, screen, {'compare': [], 'swap': [], 'block': [],
                                                 'sorted': list(range(start, end))}, speed=animation_speed,
                                 buttons=buttons)
            if command == "Cancel":
                return array

        size *= 2

    return array


def generate_random_array(min_int, max_int, size) -> list:
    """return randomised array"""
    return [random.randint(min_int, max_int) for _ in range(size)]

def change_array_size(screen, entry_rect, heading_rect, current_array):
    """Handle user input to return new array size"""

    # get input
    new_size = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)
    if new_size is not None:
        # handle input
        array_size = int(new_size)
        if array_size != 0:  # avoid div by 0 error
            bar_width = ARRAY_RECT.width // array_size  # doing the math, max size is 400
        else:
            bar_width = ARRAY_RECT.width + 1  # will result too small error

        # provide error messages
        if bar_width <= 1:
            utilities.pop_up_message(screen, "Max size is 400", error=True)

        elif bar_width > ARRAY_RECT.width:
            utilities.pop_up_message(screen, "Min size is 1", error=True)

        else:
            # input is valid
            return generate_random_array(10, 200, array_size)

    return current_array # there was an error, so dont change the array


def run_sort_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    """Launch program and handle button clicks."""

    running = True
    command = None

    array_size = 30
    array = generate_random_array(10, 200, array_size)

    entry_rect = pygame.Rect(screen.get_width() // 2 - 320, 150, 640, 70)
    heading_rect = pygame.Rect(screen.get_width() // 2 - 320, 250, 640, 50)
    animation_speed = 150  # milliseconds of delay per frame

    time_taken = "Invalid"

    # list of all buttons and button positions.
    buttons = {
        'Bubble': pygame.Rect(120, 480, 150, 50),
        'Selection': pygame.Rect(290, 480, 150, 50),
        'Merge': pygame.Rect(460, 480, 150, 50),
        'Randomise': pygame.Rect(630, 480, 150, 50),

        'Change Speed': pygame.Rect(120, 540, 213, 50),  # second row
        'Change Size': pygame.Rect(353, 540, 213, 50),
        'Back': pygame.Rect(586, 540, 193, 50), }

    # different instructions are displayed depending on what mode is selected
    instructions = {
        None: f"Select a sort algorithm, randomise the array, or go back \n Time Taken: {time_taken} "
              f"\n Current animation speed: {animation_speed}ms | Current size: {array_size}",
        'Bubble': "Red: swap occurring  \n  Yellow: comparing adjacent pair  |  Green: sorted",
        'Selection': "Yellow: current minimum   \n Red: comparing against minimum  |  Green: sorted",
        'Merge': "Blue: blocks being merged  |  Yellow: comparing elements  |  \n Red: placing element  |  Green: merged region sorted",
        'Reset': "Array has been reset",
        'Back': "Exiting..."
    }

    # cancel button popup that appears while sort is running
    cancel_buttons = {'Cancel': CANCEL_BUTTON_RECT}

    # initial draw
    utilities.fill_screen(screen)
    utilities.draw_buttons(buttons, screen)
    utilities.draw_text_in_rect("Sorting Visualiser", pygame.Rect(0, 20, screen.get_width(), 20), screen)
    draw_array(array, screen)

    while running:

        command = utilities.handle_events(buttons, command)  # get button click

        if command is not None:
            utilities.handle_button_click(command, buttons, screen)

        match command:
            case 'Bubble':

                utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)
                start_time = pygame.time.get_ticks()
                bubble_sort_visualiser(array, screen, animation_speed, cancel_buttons)
                time_taken = f"{(pygame.time.get_ticks() - start_time) / 1000:.2f}s"

            case 'Selection':
                utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)
                start_time = pygame.time.get_ticks()
                selection_sort_visualiser(array, screen, animation_speed, cancel_buttons)
                time_taken = f"{(pygame.time.get_ticks() - start_time) / 1000:.2f}s"

            case 'Merge':
                utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)
                start_time = pygame.time.get_ticks()
                array = merge_sort_iterative(array, screen, animation_speed, cancel_buttons)
                time_taken = f"{(pygame.time.get_ticks() - start_time) / 1000:.2f}s"

            case 'Randomise':
                array = generate_random_array(10, 200, array_size)

            case 'Change Speed':
                new_speed = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)
                if new_speed is not None:
                    animation_speed = int(new_speed)

            case 'Change Size':
                array = change_array_size(screen, entry_rect, heading_rect, array)
                array_size = len(array)

            case 'Back':
                return

        command = None

        # redraw everything
        instructions[None] = (f"Select a sort algorithm, randomise the array, or go back \n Time Taken: {time_taken} "
                              f"\n Current animation speed: {animation_speed}ms | Current size: {array_size}")

        utilities.fill_screen(screen)
        utilities.draw_buttons(buttons, screen)
        utilities.draw_text_in_rect(instructions[command], INSTRUCTIONS_RECT, screen, clear=True)
        utilities.draw_text_in_rect("Sorting Visualiser", pygame.Rect(0, 20, screen.get_width(), 20), screen)
        draw_array(array, screen)

        pygame.display.flip()

        clock.tick(30)


def main():
    """Main function calls visualiser."""
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()
    run_sort_menu(screen, clock)


if __name__ == '__main__':
    main()
