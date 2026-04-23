"""This file is for any functions that are used in multiple locations, such as draw text.

This file also controls the theme and style. So call everything from here to keep consistent style"""
import pygame
pygame.init()
FONT = pygame.font.SysFont(None, 36)

BACKGROUND_COLOUR = pygame.Color("#F5F0EB")
TEXT_COLOR = pygame.Color("Black")
SECONDARY_COLOUR = pygame.Color("#7EC8A4")

def draw_text(text, pos, screen):
    txt = FONT.render(text, True, TEXT_COLOR)
    screen.blit(txt, pos)

def draw_button_shadow(rect, screen, radius=10, offset=3):
    """ DO NOT USE OUTSIDE OF utilities.py

    Function that adds a shadow around a button on the screen. Make sure to draw before the rest of the button.
    """
    shadow_rect = pygame.Rect(rect.x + offset, rect.y + offset, rect.width, rect.height)
    shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 50), shadow_surf.get_rect(), border_radius=radius)
    screen.blit(shadow_surf, (shadow_rect.x, shadow_rect.y))

def draw_buttons(buttons, screen):
    """Function that adds buttons to the screen. Call after filling screen. """
    for text, rect in buttons.items():
        draw_button_shadow(rect, screen)
        pygame.draw.rect(screen, pygame.Color(SECONDARY_COLOUR), rect, border_radius=10)
        draw_text(text, (rect.x + 20, rect.y + 10), screen)

def fill_screen(screen):
    screen.fill(pygame.Color(BACKGROUND_COLOUR))

