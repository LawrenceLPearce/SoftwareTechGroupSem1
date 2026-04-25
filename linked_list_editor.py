import pygame
import utilities
from linked_list import LinkedList


NODE_WIDTH = 90
NODE_HEIGHT = 50
NODE_SPACING = NODE_WIDTH + 70


def insert_node(
        screen: pygame.Surface, entry_rect: pygame.Rect, 
        heading_rect: pygame.Rect, linked_list: LinkedList
    ) -> None:
    value = utilities.text_entry(
        screen, entry_rect, heading_rect, 
        heading="Enter numerical value then press ENTER", 
        integer_only=True
    )
        
    if not value: return

    index = utilities.text_entry(
        screen, entry_rect, heading_rect, 
        heading="Enter index then press ENTER", 
        integer_only=True
    )
    
    if not index: return
    
    success = linked_list.insert(int(value), int(index))

    if not success:
        utilities.pop_up_message(screen, "Index out of range", error=True)


def delete_node(
        screen: pygame.Surface, entry_rect: pygame.Rect, 
        heading_rect: pygame.Rect, linked_list: LinkedList
    ) -> None:
    value = utilities.text_entry(
        screen, entry_rect, heading_rect, 
        heading="Enter value of node you wish to delete", 
        integer_only=True
    )

    if not value: return

    success = linked_list.delete(int(value))

    if not success:
        utilities.pop_up_message(screen, "Value not found", error=True)


def draw_linked_list(screen: pygame.Surface, linked_list: LinkedList) -> None:
    current = linked_list.head
    x_position = 30
    y_position = 300
    previous_node = None

    while current:
        current_node = pygame.Rect(x_position, y_position, NODE_WIDTH, 50)
        
        utilities.draw_node(
            rect=current_node, text=str(current.data), 
            screen=screen
        )

        if previous_node:
            utilities.draw_node_connects(
                screen, previous_node, current_node, directed=True
            )

        current = current.next
        previous_node = current_node
        x_position += NODE_SPACING
    
    
def linked_list_editor(screen: pygame.Surface, linked_list: LinkedList):
    utilities.fill_screen(screen)
    utilities.draw_text("Linked List Editor", ((screen.get_width() // 4) + 120, 50), screen)
    buttons = {
        'Insert': pygame.Rect(120, 500, 150, 50),
        'Delete': pygame.Rect(290, 500, 150, 50),
        'Reverse': pygame.Rect(460, 500, 150, 50),
        'Back': pygame.Rect(630, 500, 150, 50)
        }
    utilities.draw_buttons(buttons, screen)
    draw_linked_list(screen, linked_list)
    pygame.display.flip()
    return buttons


def run_linked_list_editor(screen: pygame.Surface, clock: pygame.time.Clock):
    linked_list = LinkedList()
    running = True
    buttons = linked_list_editor(screen, linked_list)
    command = None
    entry_rect = pygame.Rect(190, 150, 520, 70)
    heading_rect = pygame.Rect(190, 250, 520, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for name, rect in buttons.items():
                    if rect.collidepoint(pos):
                        command = name

        if command is None:
            buttons = linked_list_editor(screen, linked_list)

        elif command == "Insert":
            utilities.handle_button_click("Insert", buttons, screen)
            insert_node(screen, entry_rect, heading_rect, linked_list)

        elif command == "Delete":
            utilities.handle_button_click("Delete", buttons, screen)
            delete_node(screen, entry_rect, heading_rect, linked_list)

        elif command == "Reverse":
            utilities.handle_button_click("Reverse", buttons, screen)
            if not linked_list.head:
                utilities.pop_up_message(screen, "Insert nodes before reversing")
            linked_list.reverse()

        elif command == "Back":
            utilities.handle_button_click("Back", buttons, screen)
            running = False

        command = None

        clock.tick(30)