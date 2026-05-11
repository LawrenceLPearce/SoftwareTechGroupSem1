import pygame
from utils import utilities
from puzzles.event_queue import Event, EventQueue
from utils import config


ROW_HEIGHT = 80
NODE_WIDTH = 75
NODE_HEIGHT = 65
HORIZONTAL_OFFSET = 220


def add_event(
        screen: pygame.Surface, entry_rect: pygame.Rect, 
        heading_rect: pygame.Rect, queue: EventQueue
    ) -> None:
    """
    Prompts user for event title, time, and priority, then animates 
    insertion into priority queue.
    """
    title = utilities.text_entry(
        screen, entry_rect, heading_rect,
        heading="Enter title of event", max_chars=25
    )
    if not title: return

    hour = utilities.text_entry(
        screen, entry_rect, heading_rect,
        heading="Enter hour of event (24 hour time)",
        integer_only=True, draw_shadow=False, max_chars=2
    )
    if not hour: 
        return
    
    # Ensure hour is in valid range (0-23)
    hour = int(hour)
    if hour < 0 or hour > 23:
        utilities.pop_up_message(screen, "Invalid hour", error=True)
        return
    
    minute = utilities.text_entry(
        screen, entry_rect, heading_rect,
        heading="Enter minute of event",
        integer_only=True, draw_shadow=False, max_chars=2
    )
    if not minute: 
        return

    # Ensure minute is in valid range (0-59)
    minute = int(minute)
    if minute < 0 or minute > 59:
        utilities.pop_up_message(screen, "Invalid minute", error=True)
        return
    
    heading_rect = pygame.Rect(180, 250, 540, 50)
    priority = utilities.text_entry(
        screen, entry_rect, heading_rect,
        heading="Enter priority of event (highest priority = 1)",
        integer_only=True, draw_shadow=False
    )
    if not priority: 
        return
    
    priority=int(priority)
    if priority < 1:
        utilities.pop_up_message(
            screen, "Priority cannot be less than 1", error=True
        )
        return

    event = Event(
        hour=hour, minute=minute, priority=priority, title=title
    )

    queue_state = queue.animate_insert(event)
    highlights = []
    
    while True:
        utilities.fill_screen(screen)
        utilities.draw_text(
            "Event Queue Simulator", ((screen.get_width() // 4) + 90, 30), screen
        )
        try:
            highlights = next(queue_state)
        except StopIteration:
            break

        draw_event_queue(screen, queue, highlights) # type: ignore
        hold_frame(450)


def extract_event(screen: pygame.Surface, queue: EventQueue) -> None:
    """
    Animates the extraction of the next event / priority queue root.
    """
    if len(queue) == 0:
        utilities.pop_up_message(screen, "Nothing to extract", error=True)
        return
    
    queue_state = queue.animate_extract()
    highlights = []
   
    while True:
        utilities.fill_screen(screen)
        utilities.draw_text(
            "Event Queue Simulator", ((screen.get_width() // 4) + 90, 30), screen
        )
        try:
            highlights = next(queue_state)
        except StopIteration:
            break
        
        draw_event_queue(screen, queue, highlights)
        hold_frame(450)
    
    draw_event_queue(screen, queue)
    utilities.pop_up_message(
        screen, f"Extracted '{highlights[0][0].title}'" # type:ignore
    )
    

def hold_frame(duration: int) -> None:
    """Pauses on frame for given duration."""
    start_time = pygame.time.get_ticks()
    pygame.display.flip()
    while True:
        current_time = pygame.time.get_ticks()

        if current_time - start_time > duration:
            return


def open_event_list(
        screen: pygame.Surface, clock: pygame.time.Clock, 
        queue: EventQueue
    ) -> None:
    """Opens list showing up to three upcoming events."""
    # draw shadow over whole screen
    shadow_surf = pygame.Surface(
        (screen.get_width(), screen.get_height()), pygame.SRCALPHA
    )
    pygame.draw.rect(
        shadow_surf, (0, 0, 0, 90),
        pygame.Rect(0, 0, screen.get_width(), screen.get_height())
    )
    screen.blit(shadow_surf, (0, 0))

    command = None
    while True:
        buttons = draw_event_list(screen, queue)

        pygame.display.flip()

        command = utilities.handle_events(buttons, None)

        if command == "X":
            utilities.handle_button_click(
                "X", buttons, screen, colour=config.ERROR_COLOUR_DARK
            )
            return

        clock.tick(30)


def draw_event_list(
        screen: pygame.Surface, queue: EventQueue
    ) -> dict[str, pygame.Rect]:
    """Draws the event list."""
    # Count events, max of 3 displayed
    count = min(len(queue), 3)
    height = 65 + (90 * count)

    # Background
    rect = pygame.Rect(275, 100, 350, height)
    pygame.draw.rect(
        screen, config.SECONDARY_COLOUR, rect, border_radius=10
    )
    
    # Close button
    buttons = {'X': pygame.Rect(580, 110, 35, 35)}
    utilities.draw_buttons(buttons, screen, colour=config.ERROR_COLOUR)

    # Title
    utilities.draw_text("Upcoming Events:", (300, 120), screen)

    for i in range(count):
        event = queue.get(i)

        if event is None: 
            continue

        y = 160 + (i * 90)

        # Event card
        event_rect = pygame.Rect(295, y, 310, 75)
        pygame.draw.rect(
            screen, pygame.Color("white"), event_rect, border_radius=8
        )

        # Time label
        utilities.draw_text(
            f"{event.hour:02}:{event.minute:02}", (300, y + 8), screen
        )

        # Priority label
        utilities.draw_text(
            f"Priority: {event.priority}", (440, y + 8), screen
        )

        # Title label
        title = event.title
        if len(title) > 20:
            title = event.title[:15] + "..."
        utilities.draw_text(
            title, (300, y + 40), screen
        )

    return buttons


def draw_event_queue(
        screen: pygame.Surface, queue: EventQueue, 
        highlights: tuple[list, str] | None = None
    ) -> None:
    """Draws nodes in priority queue structure."""
    if len(queue) > 0:
        draw_event_node(
            screen, 0, screen.get_width() / 2 - NODE_WIDTH / 2, 
            100, HORIZONTAL_OFFSET, queue, highlights
        )


def draw_event_node(
        screen: pygame.Surface, index: int, x: float, 
        y: float, offset: float, queue: EventQueue,
        highlights: tuple[list, str] | None = None
    ) -> pygame.Rect:
    """Draws node and recusively draws nodes children."""
    # Get event
    event = queue.get(index)

    outer_color = config.SECONDARY_COLOUR
    inner_color = pygame.Color("white")

    if highlights and index in highlights[0]:
        # Highlight inner or outer rectangle 
        # depending on what is being compared
        comparision = highlights[1]
        if comparision == "time":
            outer_color = config.HIGHLIGHT_COLOUR
        elif comparision == "priority":
            inner_color = config.HIGHLIGHT_COLOUR

    # Outer rectangle
    node_rect = pygame.Rect(x, y, NODE_WIDTH, NODE_HEIGHT)
    pygame.draw.rect(screen, outer_color, node_rect, border_radius=10)

    # Time label
    min = str(event.minute) if event else "00"
    if len(min) == 1:
        min = "0" + min # Leading zero format for minutes (e.g. 12:05)

    utilities.draw_text_in_rect(
        f"{event.hour}:{min}", node_rect, screen, # type: ignore
        v_offset=-15 
    )

    # Inner rectangle
    rect = pygame.Rect(x+7, y+33, 60, 25)
    pygame.draw.rect(screen, inner_color, rect, border_radius=5)

    # Priority label
    utilities.draw_text_in_rect(
        str(event.priority), rect, screen # type: ignore
    ) 

    # Get indices of children of node
    left = queue.leftChild(index)   
    right = queue.rightChild(index) 
    
    # Draw child nodes recursively (if they exist)
    if left < len(queue):
        new_x = x - offset
        new_y = y + ROW_HEIGHT
        # Halve offset to avoid overlapping
        new_node = draw_event_node(
            screen, left, new_x, new_y, offset / 2, 
            queue, highlights
        )
        utilities.draw_node_connects(
            screen, node_rect, new_node, 
            start_location="bottom", end_location="top"
        )
        
    if right < len(queue):
        new_x = x + offset
        new_y = y + ROW_HEIGHT
        new_node = draw_event_node(
            screen, right, new_x, new_y, offset / 2, 
            queue, highlights
        )
        utilities.draw_node_connects(
            screen, node_rect, new_node, 
            start_location="bottom", end_location="top"
        )
    
    return node_rect


def event_queue_simulator(
        screen: pygame.Surface, queue: EventQueue
    ) -> dict[str, pygame.Rect]:
    """
    Draws elements of event queue simulator, including title, 
    event queue, and button panel.
    """
    utilities.fill_screen(screen)
    utilities.draw_text(
        "Event Queue Simulator", ((screen.get_width() // 4) + 90, 30), screen
    )
    buttons = {
        'Add Event': pygame.Rect(70, 500, 150, 50),
        'Remove Upcoming': pygame.Rect(240, 500, 250, 50),
        'See Events': pygame.Rect(510, 500, 150, 50),
        'Back': pygame.Rect(680, 500, 150, 50),
    }
    utilities.draw_buttons(buttons, screen)
    
    draw_event_queue(screen, queue)

    pygame.display.flip()

    return buttons


def run_event_queue_simulator(
        screen: pygame.Surface, clock: pygame.time.Clock
    ) -> None:
    """
    Runs the pygame event loop for the heap visualiser module.
    """
    queue = EventQueue()
    buttons = event_queue_simulator(screen, queue)
    command = None
    entry_rect = pygame.Rect(240, 150, 420, 70)
    heading_rect = pygame.Rect(240, 250, 420, 50)
    
    running = True
    while running:
        command = utilities.handle_events(buttons, command)

        if command is None:
            buttons = event_queue_simulator(screen, queue)

        match command:
            case "Add Event":
                utilities.handle_button_click("Add Event", buttons, screen)
                add_event(screen, entry_rect, heading_rect, queue)

            case "Remove Upcoming":
                utilities.handle_button_click("Remove Upcoming", buttons, screen)
                extract_event(screen, queue)

            case "See Events":
                utilities.handle_button_click("See Events", buttons, screen)
                open_event_list(screen, clock, queue)

            case "Back":
                utilities.handle_button_click("Back", buttons, screen)
                running = False

        command = None

        clock.tick(30)