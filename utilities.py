"""This file is for any functions that are used in multiple locations, such as draw text.

This file also controls the theme and style. So call everything from here to keep consistent style"""
import pygame
pygame.init()
FONT = pygame.font.SysFont(None, 36)


############################ COLOURS #########################
# Add any colours here so that if we change anything, it will apply everywhere.
# Also, import colours from here so that it all stays consistent
BACKGROUND_COLOUR = pygame.Color("#F5F0EB")
TEXT_COLOUR = pygame.Color("Black")

SECONDARY_COLOUR = pygame.Color("#7EC8A4")
SECONDARY_COLOUR_SHADOW = pygame.Color("#6DB893")
############################################################

def draw_text(text, pos, screen):
    txt = FONT.render(text, True, TEXT_COLOUR)
    screen.blit(txt, pos)

def draw_button_shadow(rect, screen, radius=10, offset=3):
    """ DO NOT USE OUTSIDE OF utilities.py

    Function that adds a shadow around a button on the screen. Make sure to draw before the rest of the button.
    """
    shadow_rect = pygame.Rect(rect.x + offset, rect.y + offset, rect.width, rect.height)
    shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 50), shadow_surf.get_rect(), border_radius=radius)
    screen.blit(shadow_surf, (shadow_rect.x, shadow_rect.y))

def draw_button_pressed(rect, screen, radius=10, offset=3):

    # put shadow in top left to make it look indented
    shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 50),
                     pygame.Rect(0, 0, rect.width, rect.height),
                     border_radius=radius)
    pygame.draw.rect(shadow_surf, SECONDARY_COLOUR_SHADOW,  # darker fill
                     pygame.Rect(offset, offset, rect.width - offset, rect.height - offset),
                     border_radius=radius)
    screen.blit(shadow_surf, (rect.x, rect.y))

def draw_buttons(buttons, screen):
    """Function that adds buttons to the screen. Call after filling screen. """
    for text, rect in buttons.items():
        draw_button_shadow(rect, screen)
        pygame.draw.rect(screen, pygame.Color(SECONDARY_COLOUR), rect, border_radius=10)
        draw_text(text, (rect.x + 20, rect.y + 10), screen)

def handle_button_click(button_text, buttons, screen):
    rect = buttons[button_text] # get correct button

    # draw pressed button
    draw_button_pressed(rect, screen)
    draw_text(button_text, (rect.x + 20 + 2, rect.y + 10 + 2), screen)  # shift text down
    pygame.display.flip()

    # Wait for mouse release
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                return

def fill_screen(screen):
    screen.fill(pygame.Color(BACKGROUND_COLOUR))

