import pygame
from utils import utilities
from heap_visualiser.heap import Heap
from utils import config


# TODO: add comments, error messages, instructions


ROW_HEIGHT = 70
NODE_WIDTH = 50
NODE_HEIGHT = 30
HORIZONTAL_OFFSET = 200


def insert(
        screen: pygame.Surface, entry_rect: pygame.Rect, 
        heading_rect: pygame.Rect, heap: Heap
    ) -> None:

    value = utilities.text_entry(
        screen, entry_rect, heading_rect,
        heading="Enter numerical value then press ENTER",
        integer_only=True
    )

    if not value: return
  
    heap_state = heap.animate_insert(int(value))
    highlights = []
    running = True

    while True:
        utilities.fill_screen(screen)
        utilities.draw_text("Heap Visualiser", ((screen.get_width() // 4) + 120, 50), screen)

        try:
            highlights = next(heap_state)
        except StopIteration:
            break

        draw_heap(screen, heap, highlights)
        
        hold_frame(400)


def extract(screen: pygame.Surface, heap: Heap) -> None:
    if len(heap) == 0:
        return
    
    heap_state = heap.animate_remove()
    highlights = []
    running = True

    while True:
        utilities.fill_screen(screen)
        utilities.draw_text("Heap Visualiser", ((screen.get_width() // 4) + 120, 50), screen)

        try:
            highlights = next(heap_state)
        except StopIteration:
            break

        draw_heap(screen, heap, highlights)
        
        hold_frame(600)


def hold_frame(duration: int) -> None:
    start_time = pygame.time.get_ticks()
    pygame.display.flip()
    while True:
        current_time = pygame.time.get_ticks()

        if current_time - start_time > duration:
            return


def draw_heap(
        screen: pygame.Surface, heap: Heap, 
        highlights: list[int] | None = None
    ) -> None:
    if len(heap) > 0:
        draw_heap_node(
            screen, 0, screen.get_width() / 2 - NODE_WIDTH / 2, 
            120, HORIZONTAL_OFFSET, heap, highlights
        )


def draw_heap_node(
        screen: pygame.Surface, index: int, x: float, 
        y: float, offset: float, heap: Heap,
        highlights: list[int] | None = None
    ) -> pygame.Rect:
    node_rect = pygame.Rect(x, y, NODE_WIDTH, NODE_HEIGHT)

    if highlights and index in highlights:
        color = config.HIGHLIGHT_COLOUR
    else:
        color = config.SECONDARY_COLOUR

    utilities.draw_node(
        screen=screen, rect=node_rect, color=color, 
        text=str(heap._arr[index])
    )

    # Get indices of children of node
    left = heap.leftChild(index)   
    right = heap.rightChild(index) 
    
    # Draw child nodes recursively (if they exist)
    if left < heap._nItems:
        new_x = x - offset
        new_y = y + ROW_HEIGHT
        # Halve offset to avoid overlapping
        new_node = draw_heap_node(
            screen, left, new_x, new_y, offset / 2, heap, highlights
        )
        utilities.draw_node_connects(
            screen, node_rect, new_node, 
            start_location="bottom", end_location="top"
        )
        
    if right < heap._nItems:
        new_x = x + offset
        new_y = y + ROW_HEIGHT
        new_node = draw_heap_node(
            screen, right, new_x, new_y, offset / 2, heap, highlights
        )
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
        'Insert': pygame.Rect(205, 500, 150, 50),
        'Extract': pygame.Rect(375, 500, 150, 50),
        'Back': pygame.Rect(545, 500, 150, 50),
    }
    utilities.draw_buttons(buttons, screen)
    draw_heap(screen, heap)
    pygame.display.flip()
    return buttons


def run_heap_visualiser(screen: pygame.Surface, clock: pygame.time.Clock):
    heap = get_default_heap()
    buttons = heap_visualiser(screen, heap)
    command = None
    entry_rect = pygame.Rect(190, 150, 520, 70)
    heading_rect = pygame.Rect(190, 250, 520, 50)
    
    running = True
    while running:
        command = utilities.handle_events(buttons, command)

        if command is None:
            buttons = heap_visualiser(screen, heap)

        match command:
            case "Insert":
                utilities.handle_button_click("Insert", buttons, screen)
                insert(screen, entry_rect, heading_rect, heap)

            case "Extract":
                utilities.handle_button_click("Extract", buttons, screen)
                extract(screen, heap)

            case "Back":
                utilities.handle_button_click("Back", buttons, screen)
                running = False

        command = None

        clock.tick(30)