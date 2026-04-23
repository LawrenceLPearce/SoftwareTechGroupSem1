"""This file is for any functions that are used in multiple locations, such as draw text.

There exists:
    - Several button functions: Drawing buttons, drawing pressed buttons, handling button presses
    - Text entry handler that returns string todo: implement lol

This file also controls the theme and style. So call everything from here to keep consistent style"""
import pygame
import random
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

def draw_text_in_rect(text, rect, screen):
    txt = FONT.render(text, True, TEXT_COLOUR)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

def draw_offset_rect(outer_rect, screen, offset=8, outer_colour=SECONDARY_COLOUR, inner_colour=BACKGROUND_COLOUR):
    pygame.draw.rect(screen, outer_colour, outer_rect, border_radius=10)
    # inner
    inner_rect = outer_rect.inflate(-offset, -offset)
    pygame.draw.rect(screen, inner_colour, inner_rect, border_radius=10)



def draw_button_shadow(rect, screen, radius=10, offset=3):
    """ DO NOT USE OUTSIDE OF utilities.py

    Function that adds a shadow around a button on the screen. Make sure to draw before the rest of the button.
    """
    shadow_rect = pygame.Rect(rect.x + offset, rect.y + offset, rect.width, rect.height)
    shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 50), shadow_surf.get_rect(), border_radius=radius)
    screen.blit(shadow_surf, (shadow_rect.x, shadow_rect.y))


def draw_button_pressed(rect, screen, radius=10, offset=3):
    """Makes a button look like it is pressed by adding an internal shadow."""

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
    """Function that adds buttons to the screen. Call after filling screen.
    buttons: Dict {'text', pygame.Rect(coordinates etc)}"""
    for text, rect in buttons.items():
        draw_button_shadow(rect, screen)
        pygame.draw.rect(screen, pygame.Color(SECONDARY_COLOUR), rect, border_radius=10)
        draw_text(text, (rect.x + 20, rect.y + 10), screen)


def handle_button_click(button_text, buttons, screen):
    """draws the button with shadows until the mouse is released (unclicked)."""
    rect = buttons[button_text]  # get correct button

    # draw pressed button
    draw_button_pressed(rect, screen)
    draw_text(button_text, (rect.x + 20 + 2, rect.y + 10 + 2), screen)  # shift text down
    pygame.display.flip()

    # Wait for mouse release
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                return


def fill_screen(screen):
    screen.fill(pygame.Color(BACKGROUND_COLOUR))


def draw_node(rect, text, screen, color=SECONDARY_COLOUR, text_color=TEXT_COLOUR, radius=10):
    # Shadow
    shadow_surf = pygame.Surface((rect.width + 3, rect.height + 3), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 40),
                     pygame.Rect(3, 3, rect.width, rect.height),
                     border_radius=radius)
    screen.blit(shadow_surf, (rect.x, rect.y))

    # Body
    pygame.draw.rect(screen, color, rect, border_radius=radius)

    # Centered text
    txt = FONT.render(text, True, text_color)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)


def draw_node_connects():
    pass


def text_entry(screen: pygame.Surface, entry_rect: pygame.Rect, heading_rect: pygame.Rect,
               heading: str = "Type text then pres ENTER (ESC to exit)") -> str | None:
    # draw shadow over whole screen
    shadow_surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 90),
                     pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
    screen.blit(shadow_surf, (0, 0))


    # draw both rects
    for rect in [entry_rect, heading_rect]:
        draw_offset_rect(rect, screen)

    # draw heading text
    draw_text_in_rect(heading, heading_rect, screen)

    pygame.display.flip()
    # heading within rect
    # get key presses

    text = ''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    running = False
                    break
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                draw_offset_rect(entry_rect, screen)
                draw_text_in_rect(text, entry_rect, screen)
                pygame.display.flip()

    return text
