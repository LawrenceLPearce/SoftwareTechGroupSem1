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

SECONDARY_COLOUR = pygame.Color("#7EC8A4") # also used for buttons
SECONDARY_COLOUR_SHADOW = pygame.Color("#6DB893")

NODE_COLOUR = pygame.Color("#53ffdd")
NODE_EDGE_COLOUR = pygame.Color("#53ffdd")

HIGHLIGHT_COLOUR = pygame.Color("#ffd869")
############################################################

def draw_text(text, pos, screen):
    """
    draw text at given location
    :param text: text to be written
    :param pos: x, y
    :param screen: pygame.Surface
    :return: None
    """
    txt = FONT.render(text, True, TEXT_COLOUR)
    screen.blit(txt, pos)

def draw_text_in_rect(text, rect, screen):
    """
    centers text within given rect
    :param text: text to be written
    :param rect: pygame.Rect
    :param screen: pygame.Surface
    :return: None
    """
    txt = FONT.render(text, True, TEXT_COLOUR)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

def draw_offset_rect(outer_rect, screen, offset=8, outer_colour=SECONDARY_COLOUR, inner_colour=BACKGROUND_COLOUR):
    """
    draws a smaller rect of different colour inside the given rect
    :param outer_rect: pygame.Rect object
    :param screen: pygame.Surface
    :param offset: (optional) the total offset for inner triangle (gets divided in 2 for each side)
    :param outer_colour: (optional) colour of the outer rectangle
    :param inner_colour: (optional) colour of the inner rectangle
    :return: None
    """
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
    """
    Makes a button look like it is pressed by adding an internal shadow.
    :param rect: button rect
    :param screen: screen
    :param radius: (optional) corner radius
    :param offset: (optional) shadow offset
    :return:
    """

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
    """
    function that adds buttons to the screen. Call after filling screen.
    :param buttons: Dict {'text', pygame.Rect(coordinates etc)}
    :param screen: pygame.screen
    :return: None
    """
    for text, rect in buttons.items():
        draw_button_shadow(rect, screen)
        pygame.draw.rect(screen, pygame.Color(SECONDARY_COLOUR), rect, border_radius=10)
        draw_text(text, (rect.x + 20, rect.y + 10), screen)


def handle_button_click(button_text, buttons, screen):
    """
    Waits until mouse is released. Draws button in inverted mode to make it look like it is inverted
    :param button_text: button key
    :param buttons: Dict of buttons
    :param screen: pygame.screen
    :return: None
    """
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
    """
    Function to draw a node. Will be moved to bst if only used there.
    :param rect: Node rectangle
    :param text: text to display within node
    :param screen: screen
    :param color: (optional): colour of node
    :param text_color: (optional): colour of text
    :param radius: (optional): radius of coners
    :return: None
    """

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
               heading: str = None, integer_only = False) -> str | None :
    """
    provides a text box for text entry.
    :param screen: pygame.screen
    :param entry_rect: pygame.Rect for where the text will be displayed
    :param heading_rect: pygame.Rect for where instructions are displayed
    :param heading: (optional) str of what to write in heading
    :param integer_only: (optional) bool whether to only accept number input
    :return: str | None
    """
    if heading is None:
        if integer_only:
            heading = "Type NUMBER only then press ENTER (ESC to exit)"
        else:
            heading = "Type text then press ENTER (ESC to exit)"

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
                elif not integer_only or event.unicode.isdigit(): # check that the input is valid
                    text += event.unicode
                draw_offset_rect(entry_rect, screen)
                draw_text_in_rect(text, entry_rect, screen)
                pygame.display.flip()

    return text
