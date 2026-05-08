import pygame
from utils import utilities
from puzzles.event_queue import Event, EventQueue


def add_event(
        screen: pygame.Surface, entry_rect: pygame.Rect, 
        heading_rect: pygame.Rect, queue: EventQueue
    ) -> None:
    title = utilities.text_entry(
        screen, entry_rect, heading_rect,
        heading="Enter event title", max_chars=25
    )
 
    if not title: return

    hour = utilities.text_entry(
        screen, entry_rect, heading_rect,
        heading="Enter hour of event (24 hour time)",
        integer_only=True
    )

    if not hour: 
        return
    
    minute = utilities.text_entry(
        screen, entry_rect, heading_rect,
        heading="Enter minute of event",
        integer_only=True
    )

    if not hour: 
        return


def event_queue_simulator(screen: pygame.Surface, queue: EventQueue):
    utilities.fill_screen(screen)
    utilities.draw_text(
        "Event Queue Simulator", ((screen.get_width() // 4) + 100, 50), screen
    )
    buttons = {
        'Add Event': pygame.Rect(155, 500, 150, 50),
        'Remove Upcoming': pygame.Rect(325, 500, 250, 50),
        'Back': pygame.Rect(595, 500, 150, 50),
    }
    utilities.draw_buttons(buttons, screen)
    #draw_event_queue(screen, queue)
    pygame.display.flip()
    return buttons


def run_event_queue_simulator(screen: pygame.Surface, clock: pygame.time.Clock):
    queue = EventQueue()
    buttons = event_queue_simulator(screen, queue)
    command = None
    entry_rect = pygame.Rect(190, 150, 520, 70)
    heading_rect = pygame.Rect(190, 250, 520, 50)
    
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
                #extract(screen, queue)

            case "Back":
                utilities.handle_button_click("Back", buttons, screen)
                running = False

        command = None

        clock.tick(30)