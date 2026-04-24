from binary_search_tree import Node, BST
import pygame
import utilities

###

NODE_R      = 24
LEVEL_GAP   = 80
H_GAP_BASE  = 60     # horizontal spread at root level
TREE_W = 700

TREE_RECT = pygame.Rect(250, 50, TREE_W -2, 600)


def px(norm_x, norm_y, rect: pygame.Rect):
    x = rect.left + int(norm_x * rect.width)
    y = rect.top + 60 + norm_y * LEVEL_GAP
    return x, y

def compute_positions(node, depth=0, left=0.0, right=1.0, positions=None):
    if positions is None:
        positions = {}
    if node is None:
        return positions
    mid = (left + right) / 2
    positions[id(node)] = (mid, depth)
    compute_positions(node.left,  depth + 1, left, mid,   positions)
    compute_positions(node.right, depth + 1, mid,  right, positions)
    return positions

def draw_tree(screen, node, positions, font=utilities.FONT, highlight_val=None):
    if node is None:
        return

    cx, cy = px(*positions[id(node)], TREE_RECT)

    for child in (node.left, node.right):
        if child and id(child) in positions:
            ccx, ccy = px(*positions[id(child)], TREE_RECT)
            pygame.draw.line(screen, utilities.NODE_EDGE_COLOUR, (cx, cy), (ccx, ccy), 2)

    col = utilities.HIGHLIGHT_COLOUR if (highlight_val is not None and node.val == highlight_val) else utilities.NODE_COLOUR
    pygame.draw.circle(screen, col, (cx, cy), NODE_R)
    pygame.draw.circle(screen, utilities.SECONDARY_COLOUR, (cx, cy), NODE_R, 2)

    label = font.render(str(node.val), True, utilities.TEXT_COLOUR)
    screen.blit(label, label.get_rect(center=(cx, cy)))

    draw_tree(screen, node.left, positions, font, highlight_val)
    draw_tree(screen, node.right, positions, font, highlight_val)

#TODO: Instruction Area
#TODO: Add node button + text enter
#TODO: Delete node button + text area
# TODO: Display tree edit
# TODO: SEARCH Highlight

def bst_menu(screen: pygame.Surface):

    buttons = {
        'Add Node':     pygame.Rect(50, 150, 190, 50),
        'Delete Node':  pygame.Rect(50, 230, 190, 50),
        'Search':       pygame.Rect(50, 310, 190, 50),
        'Back to Menu': pygame.Rect(50, 390, 190, 50),
    }

    return buttons

def run_bst_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    bst = BST()
    # bst.insert(50)
    # bst.insert(30)
    # bst.insert(70)
    # bst.insert(20)
    # bst.insert(40)
    # bst.insert(60)
    # bst.insert(80)
    running = True
    current_module = None
    buttons = bst_menu(screen)

    entry_rect = pygame.Rect(50, 500, 610, 70)
    heading_rect = pygame.Rect(50, 445, 610, 50)





    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_module is None:
                pos = event.pos
                for name, rect in buttons.items():
                    if rect.collidepoint(pos):
                        current_module = name

        if current_module is None:
            buttons = bst_menu(screen)
        if current_module is None:
            buttons = bst_menu(screen)
        else:
            if current_module == 'Add Node':
                utilities.handle_button_click("Add Node", buttons, screen)
                node_value = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)
                if node_value:
                    bst.insert(int(node_value))
            elif current_module == 'Delete Node':
                utilities.handle_button_click("Delete Node", buttons, screen)
                utilities.text_entry(screen, entry_rect, heading_rect)
            elif current_module == 'Search':
                utilities.handle_button_click("Search", buttons, screen)
                utilities.text_entry(screen, entry_rect, heading_rect)
            elif current_module == 'Back to Menu':
                utilities.handle_button_click("Back to Menu", buttons, screen)
                running = False

            # For demo, after module ends return to menu
            current_module = None
        # draw tree




        utilities.fill_screen(screen)
        utilities.draw_text("Binary Search Tree", ((screen.get_width() // 4) + 30, 30), screen)
        utilities.draw_buttons(buttons, screen)
        # pygame.draw.rect(screen,(0, 0, 0, 50), TREE_RECT )
        draw_tree(screen, bst.root, compute_positions(bst.root))
        pygame.display.flip()

        clock.tick(30)
    return

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()
    run_bst_menu(screen, clock)

if __name__ == '__main__':
    main()