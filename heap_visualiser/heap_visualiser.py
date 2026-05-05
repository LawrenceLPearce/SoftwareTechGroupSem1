import pygame
from utils import utilities
from heap_visualiser.heap import Heap


ROW_HEIGHT = 70
HORIZONTAL_OFFSET = 200


def draw_heap(screen: pygame.Surface, heap: Heap):
    if len(heap) > 0:
        draw_heap_node(
            screen, 0, screen.get_width() / 2 - 25, 
            120, HORIZONTAL_OFFSET, heap
        )


def draw_heap_node(
        screen: pygame.Surface, index: int, x: float, 
        y: float, offset: float, heap: Heap
    ) -> pygame.Rect:
    node_rect = pygame.Rect(x, y, 50, 30)
    utilities.draw_node(screen=screen, rect=node_rect, text=str(heap._arr[index]))

    # Get indices of children of node
    left = heap.leftChild(index)   
    right = heap.rightChild(index) 
    
    # Draw child nodes recursively if they exist
    if left < heap._nItems:
        new_x = x - offset
        new_y = y + ROW_HEIGHT
        new_node = draw_heap_node(screen, left, new_x, new_y, offset / 2, heap)
        utilities.draw_node_connects(
            screen, node_rect, new_node, 
            start_location="bottom", end_location="top"
        )
        
    if right < heap._nItems:
        new_x = x + offset
        new_y = y + ROW_HEIGHT
        new_node = draw_heap_node(screen, right, new_x, new_y, offset / 2, heap)
        utilities.draw_node_connects(
            screen, node_rect, new_node, 
            start_location="bottom", end_location="top"
        )
    
    return node_rect


def get_default_heap() -> Heap:
    default_values = [1, 3, 4, 10, 20, 35, 5]
    heap = Heap(size=len(default_values))

    for value in default_values:
        heap.insert(value)
    
    return heap


def heap_visualiser(screen: pygame.Surface, heap: Heap):
    utilities.fill_screen(screen)
    utilities.draw_text("Heap Visualiser", ((screen.get_width() // 4) + 120, 50), screen)
    buttons = {
        'Insert': pygame.Rect(120, 500, 150, 50),
        'Extract': pygame.Rect(290, 500, 150, 50),
        'Back': pygame.Rect(460, 500, 150, 50),
    }
    utilities.draw_buttons(buttons, screen)
    draw_heap(screen, heap)
    pygame.display.flip()
    return buttons


def run_heap_visualiser(screen: pygame.Surface, clock: pygame.time.Clock):
    heap = get_default_heap()
    buttons = heap_visualiser(screen, heap)
    command = None
    
    running = True
    while running:
        command = utilities.handle_events(buttons, command)

        if command is None:
            buttons = heap_visualiser(screen, heap)

        elif command == "Back":
            utilities.handle_button_click("Back", buttons, screen)
            running = False

        command = None

        clock.tick(30)