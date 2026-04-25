from DSP.binary_search_tree import BST
import pygame
from utils import utilities

###

NODE_R = 24
LEVEL_GAP = 80
H_GAP_BASE = 60  # horizontal spread at root level
TREE_W = 700

TREE_RECT = pygame.Rect(0, 50, 900, 400)


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
    compute_positions(node.left, depth + 1, left, mid, positions)
    compute_positions(node.right, depth + 1, mid, right, positions)
    return positions


def draw_tree(screen, node, positions, font=utilities.FONT, highlight_val=None,
              parent_rect: pygame.Rect = None,
              node_width=50, highlight_colour=utilities.HIGHLIGHT_COLOUR):
    if node is None:
        return
    # x and y
    cx, cy = px(*positions[id(node)], TREE_RECT)
    cx -= node_width / 2  # adjust for width

    col = highlight_colour if (
            highlight_val is not None and id(node) == highlight_val) else utilities.SECONDARY_COLOUR

    # draw node
    node_rect = pygame.Rect(cx, cy, node_width, 30)
    utilities.draw_node(screen=screen, color=col, rect=node_rect, text=str(node.val))

    # draw line to parent.
    if parent_rect:
        utilities.draw_node_connects(screen, parent_rect, node_rect, start_location="bottom", end_location="top")

    draw_tree(screen, node.left, positions, font, highlight_val, parent_rect=node_rect, node_width=node_width, highlight_colour=highlight_colour)
    draw_tree(screen, node.right, positions, font, highlight_val, parent_rect=node_rect, node_width=node_width, highlight_colour=highlight_colour)


# TODO: Better Comments

def tree_animation(bst: BST, order_list: list, screen: pygame.Surface, duration: int = 500,
                   highlight_col=utilities.HIGHLIGHT_COLOUR, final_highlight_col=utilities.HIGHLIGHT_COLOUR):

    for node_val in order_list:

        utilities.fill_screen(screen)
        utilities.draw_text("Binary Search Tree", ((screen.get_width() // 4) + 30, 30), screen)

        if node_val == order_list[-1]:
            draw_tree(screen, bst.root, compute_positions(bst.root), highlight_val=node_val, highlight_colour=final_highlight_col)
        else:
            draw_tree(screen, bst.root, compute_positions(bst.root), highlight_val=node_val, highlight_colour=highlight_col)

        # hold animation
        start_time = pygame.time.get_ticks()
        pygame.display.flip()
        while True:
            current_time = pygame.time.get_ticks()

            if current_time - start_time > duration:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return



def delete_node(bst, val: int| str | None, screen: pygame.Surface):
    if val is None:
        return None
    else:
        val = int(val)

    # first search to see if the key exists. This is for visual prompts only
    found, order = bst.search(val)
    if not found:
        tree_animation(bst, order, screen)
        utilities.pop_up_message(screen, "Value not found", error=True)
        return None

    tree_animation(bst, order, screen, final_highlight_col=utilities.HIGHLIGHT_DELETE_COLOUR)

    bst.delete(val)
    return None


def search_node(bst: BST, val: int | str | None, screen: pygame.Surface):
    if val is None:
        return None
    else:
        val = int(val)

    found, order = bst.search(val)
    if not found:
        tree_animation(bst, order, screen)
        utilities.pop_up_message(screen, "Value not found", error=True)

    tree_animation(bst, order, screen, final_highlight_col=utilities.HIGHLIGHT_FOUND_COLOUR)

    if found: return order[-1]
    return None

def insert_node(bst: BST, val: int | str | None, screen: pygame.Surface):
    if val is None:
        return None
    else:
        val = int(val)

    found, order = bst.search(val)
    tree_animation(bst, order, screen)

    bst.insert(val)
    return val

def bst_menu(screen: pygame.Surface):
    buttons = {

        'Insert': pygame.Rect(120, 500, 150, 50),
        'Delete': pygame.Rect(290, 500, 150, 50),
        'Search': pygame.Rect(460, 500, 150, 50),
        'Back': pygame.Rect(630, 500, 150, 50)

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

    entry_rect = pygame.Rect(190, 150, 640, 70)
    heading_rect = pygame.Rect(190, 250, 640, 50)

    current_highlight = None

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
            match current_module:
                case 'Insert':
                    utilities.handle_button_click("Insert", buttons, screen)
                    node_value = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)
                    node_value = insert_node(bst, node_value, screen)
                    current_highlight = bst.search(node_value)[1][-1]
                case 'Delete':
                    utilities.handle_button_click("Delete", buttons, screen)
                    node_value = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)

                    delete_node(bst, node_value, screen)
                    current_highlight = None
                case 'Search':
                    utilities.handle_button_click("Search", buttons, screen)
                    node_value = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)
                    current_highlight = search_node(bst, node_value, screen)

                case 'Back':
                    utilities.handle_button_click("Back", buttons, screen)
                    running = False

            # For demo, after module ends return to menu
            current_module = None
        # draw tree

        utilities.fill_screen(screen)
        utilities.draw_text("Binary Search Tree", ((screen.get_width() // 4) + 30, 30), screen)
        utilities.draw_buttons(buttons, screen)
        # pygame.draw.rect(screen,(0, 0, 0, 50), TREE_RECT )
        draw_tree(screen, bst.root, compute_positions(bst.root), highlight_val=current_highlight)
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
