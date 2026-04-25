# visualiser for the queue. similar to stack visualiser, may touch up visuals but for now this is the basic setup
# code inspired by stack_visualiser, also used code from Task 1.3 in the Week 10 tutorial sheet. Adjusted for queue format
import pygame
from utils import utilities
from DSP.queue_script import Queue

BLOCK_W = 90
BLOCK_H = 54
BLOCK_GAP = 10
MAX_VISIBLE = 7
QUEUE_Y = 300
QUEUE_START_X = 220


def _draw_queue(screen, font, queue):
    for i, val in enumerate(queue.items()):
        x = QUEUE_START_X + i * (BLOCK_W + BLOCK_GAP)
        rect = pygame.Rect(x, QUEUE_Y, BLOCK_W, BLOCK_H)
        pygame.draw.rect(screen, utilities.SECONDARY_COLOUR, rect, border_radius=8)
        label = font.render(str(val), True, utilities.TEXT_COLOUR)
        screen.blit(label, label.get_rect(center=rect.center))


def run_queue_visualiser(screen: pygame.Surface, clock: pygame.time.Clock):
    queue = Queue()
    font = utilities.FONT
    counter = 1

    buttons = {
        "Enqueue": pygame.Rect(30, 150, 160, 50),
        "Dequeue": pygame.Rect(30, 230, 160, 50),
        "Return to Menu": pygame.Rect(30, 550, 250, 50),
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        utilities.handle_button_click(name, buttons, screen)
                        if name == "Enqueue" and queue.size() < MAX_VISIBLE:
                            queue.enqueue(counter)
                            counter += 1
                        elif name == "Dequeue" and not queue.is_empty():
                            queue.dequeue()
                        elif name == "Return to Menu":
                            running = False

        utilities.fill_screen(screen)
        utilities.draw_text("Queue Visualiser", (320, 30), screen)
        utilities.draw_buttons(buttons, screen)
        _draw_queue(screen, font, queue)
        pygame.display.flip()
        clock.tick(30)
