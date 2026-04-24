import pygame
import utilities


class Node:
    def __init__(self, data):
        self.data = data
        self.next: Node | None = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
    
    def insert(self, data: int, index: int) -> bool:
        """
        Insert node at given index. Return false if index is 
        out of range.
        """
        new_node = Node(data)

        if index == 0:
            new_node.next = self.head
            self.head = new_node
            return True
        
        current = self.head
        count = 0
        while current:
            if count == index - 1:
                new_node.next = current.next
                current.next = new_node
                return True
            count += 1
            current = current.next
        
        return False
    
    def delete(self, value: int) -> bool:
        """
        Deletes first node with given value. Returns false if no node 
        contains value.
        """
        current = self.head
        previous = None

        while current:
            if current.data == value:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False
    

def linked_list_editor(screen: pygame.Surface):
    utilities.fill_screen(screen)
    utilities.draw_text("Linked List Editor", ((screen.get_width() // 4) + 30, 50), screen)
    buttons = {'Back': pygame.Rect(260, 150, 250, 50)}
    utilities.draw_buttons(buttons, screen)
    pygame.display.flip()
    return buttons


def run_linked_list_editor(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    buttons = linked_list_editor(screen)
    command = None

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
            buttons = linked_list_editor(screen)
        elif command == "Back":
            utilities.handle_button_click("Back", buttons, screen)
            running = False

        command = None

        clock.tick(30)

    return