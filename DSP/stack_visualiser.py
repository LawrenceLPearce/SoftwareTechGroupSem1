# visualiser for the stack demonstration. may touch up the visuals to show the top and bottom more clearly if I have time. Tired to make it match the visuals with the menus.
# some code taken from Task 1.3 in Week 10 tutorial sheet (mainly loops, stack blocks, event handling). removed key controls and just made it clickable buttons
import pygame
from utils import utilities, config
from DSP.stack import Stack

BLOCK_W = 220
BLOCK_H = 44
BLOCK_GAP = 6
MAX_VISIBLE = 9
STACK_CX = 550
STACK_BASE_Y = 500


def target_y(index):
    return STACK_BASE_Y - index * (BLOCK_H + BLOCK_GAP)

def draw_stack(screen, font, stack):
    for i, val in enumerate(stack.items()):
        x = STACK_CX - BLOCK_W // 2
        y = target_y(i)
        rect = pygame.Rect(x, y, BLOCK_W, BLOCK_H)
        pygame.draw.rect(screen, config.SECONDARY_COLOUR, rect, border_radius=8)
        label = font.render(str(val), True, config.TEXT_COLOUR)
        screen.blit(label, label.get_rect(center=rect.center))


def run_stack_visualiser(screen: pygame.Surface, clock: pygame.time.Clock):
    stack = Stack()
    font = config.FONT
    counter = 1

    buttons = {
        "Push": pygame.Rect(60, 150, 100, 50),
        "Pop": pygame.Rect(60, 230, 100, 50),
        "Return to Menu": pygame.Rect(60, 550, 250, 50),
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
                        if name == "Push" and stack.size() < MAX_VISIBLE:
                            stack.push(counter)
                            counter += 1
                        elif name == "Pop" and not stack.is_empty():
                            stack.pop()
                        elif name == "Return to Menu":
                            running = False

        utilities.fill_screen(screen)
        utilities.draw_text("Stack Visualiser", (310, 30), screen)
        utilities.draw_buttons(buttons, screen)
        draw_stack(screen, font, stack)
        pygame.display.flip()
        clock.tick(30)
