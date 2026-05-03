"""This file is for any functions that are used in multiple locations, such as draw text"""
import pygame
import math
from utils.config import FONT, BACKGROUND_COLOUR, TEXT_COLOUR, ERROR_COLOUR, SECONDARY_COLOUR, SECONDARY_COLOUR_SHADOW

pygame.init()


def handle_events(buttons: dict, current_module: str | None):
    """
    handle event loop, return clicked button text
    :param buttons:
    :param current_module:
    :return:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and current_module is None:
            for name, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    current_module = name
    return current_module


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


def draw_text_in_rect(text, rect, screen, clear=False, v_offset=0, h_offset=0):
    """
    Centers text within given rect, supports newline characters.

    :param text: text to be written
    :param rect: pygame.Rect
    :param screen: pygame.Surface
    :param clear: whether to clear the rect first or not
    :param v_offset: vertical offset in pixels (positive = down, negative = up)
    :param h_offset: horizontal offset in pixels (positive = right, negative = left)
    :return: None
    """
    if clear:
        pygame.draw.rect(screen, BACKGROUND_COLOUR, rect)

    lines = text.split('\n')
    line_height = FONT.get_height()
    total_height = line_height * len(lines)

    for i, line in enumerate(lines):
        txt = FONT.render(line, True, TEXT_COLOUR)
        center = (
            rect.centerx + h_offset,
            rect.centery + v_offset - total_height // 2 + line_height * i + line_height // 2
        )
        txt_rect = txt.get_rect(center=center)
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
        draw_text_in_rect(text, rect, screen)
        #draw_text(text, (rect.x + 20, rect.y + 10), screen)


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
    #draw_text(button_text, (rect.x + 20 + 2, rect.y + 10 + 2), screen)  # shift text down
    draw_text_in_rect(button_text, rect, screen, v_offset=2)
    pygame.display.flip()

    # Wait for mouse release
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                return


def fill_screen(screen):
    """fill the screen with background colour"""
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


def draw_node_connects(
        screen: pygame.Surface, node_1: pygame.Rect, node_2: pygame.Rect,
        color=pygame.Color("Black"), directed: bool = False,
        arrow_length: int = 8, arrow_width: int = 8,
        start_location: str = "right", end_location: str = "left"):
    """
    draws a connection between two nodes. If directed, draws an arrow 
    pointing from node 1 to node 2.
    """

    match start_location:
        case "left":
            line_start = node_1.midleft
        case "right":
            line_start = node_1.midright
        case "top":
            line_start = node_1.midtop
        case "bottom":
            line_start = node_1.midbottom
        case _:
            raise ValueError("start_location is not valid. Please implement or make a valid choice.")
    match end_location:
        case "left":
            line_end = node_2.midleft
        case "right":
            line_end = node_2.midright
        case "top":
            line_end = node_2.midtop
        case "bottom":
            line_end = node_2.midbottom
        case _:
            raise ValueError("end_location is not valid. Please implement or make a valid choice.")

    pygame.draw.line(screen, pygame.Color("Black"), line_start, line_end)

    if not directed:
        return

    dx = line_end[0] - line_start[0]
    dy = line_end[1] - line_start[1]
    length = math.hypot(dx, dy)

    if length == 0:
        return  # avoid division by zero

    # unit direction vector
    ux = dx / length
    uy = dy / length

    # perpendicular vector
    px = -uy
    py = ux

    # move back from the tip to get the base center
    base_x = line_end[0] - ux * arrow_length
    base_y = line_end[1] - uy * arrow_length

    # offset sideways to get base corners
    left = (base_x + px * arrow_width, base_y + py * arrow_width)
    right = (base_x - px * arrow_width, base_y - py * arrow_width)

    # Draw arrowhead
    pygame.draw.polygon(screen, color, [line_end, left, right])


def text_entry(screen: pygame.Surface, entry_rect: pygame.Rect, heading_rect: pygame.Rect,
               heading: str | None = None, integer_only=False) -> str | None:
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
            heading = "Enter numerical value then press ENTER (ESC to exit)"
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
                # special keys
                if event.key == pygame.K_ESCAPE: # cancel
                    return None
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN: # save and exit
                    running = False
                    break
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                elif not integer_only or event.unicode.isdigit():  # check that the input is valid
                    text += event.unicode

                draw_offset_rect(entry_rect, screen)
                draw_text_in_rect(text, entry_rect, screen)
                pygame.display.flip()

    return text


def pop_up_message(
        screen: pygame.Surface, message: str, duration: int = 1000, error=False) -> None:
    """Draws a rectangle with a text message that disappears after millisecond duration.
Uses different styles if communicating error or information.
    :param screen: screen instance to draw to
    :param message: str message to display
    :param duration: length of time in milliseconds to display message for
    :param error: bool whether message is an error or not
    :return: None
    """

    def draw_pop_up():
        # Place pop up in center of screen
        outer_rect = pygame.Rect(0, 0, width + padding, height + padding)
        screen_center = screen.get_rect().center
        outer_rect.center = screen_center[0], screen_center[1] - 250

        draw_offset_rect(outer_rect, screen, outer_colour=outer_colour, inner_colour=inner_colour)

        draw_text_in_rect(message, outer_rect, screen)

        pygame.display.flip()

    padding = 30
    width, height = FONT.size(message)

    outer_colour = ERROR_COLOUR if error else SECONDARY_COLOUR
    inner_colour = pygame.Color("white")

    start_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()

        if current_time - start_time > duration:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_pop_up()

def delay_with_exit_detection(duration):
    """
    Delay for given duration and detect quit button pressed.
    :param duration: length of time in milliseconds to delay for
    :return: None
    """
    start_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()

        if current_time - start_time > duration:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return