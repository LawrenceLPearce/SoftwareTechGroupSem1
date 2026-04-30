from DSP.binary_search_tree import BST
import pygame
from utils import utilities, config

###


LEVEL_GAP = 80  # vertical gap between nodes

TREE_RECT = pygame.Rect(0, 50, 900, 400)  # rect defining the space the bst can occupy


def normalise_positions(norm_x, norm_y, rect: pygame.Rect):
    """adjust x and y coordinates of a node to account for width of rectangle"""
    x = rect.left + int(norm_x * rect.width)
    y = rect.top + 60 + norm_y * LEVEL_GAP
    return x, y


def calc_positions(root, depth=0, left=0.0, right=1.0, positions=None):
    """iteratively calculate the relative positions of each node in the bst"""
    if positions is None:
        positions = {}
    if root is None:
        return positions
    mid = (left + right) / 2
    positions[id(root)] = (mid, depth)
    calc_positions(root.left, depth + 1, left, mid, positions)
    calc_positions(root.right, depth + 1, mid, right, positions)
    return positions


def draw_tree(screen, node, positions, font=config.FONT, highlight_val=None,
              parent_rect: pygame.Rect = None,
              node_width=50, highlight_colour=config.HIGHLIGHT_COLOUR):
    """iteratively draw full bst tree"""
    if node is None:
        return
    # x and y
    node_x, node_y = normalise_positions(*positions[id(node)], TREE_RECT)
    node_x -= node_width / 2  # adjust for width

    col = highlight_colour if (
            highlight_val is not None and id(node) == highlight_val) else config.SECONDARY_COLOUR

    # draw node
    node_rect = pygame.Rect(node_x, node_y, node_width, 30)
    utilities.draw_node(screen=screen, color=col, rect=node_rect, text=str(node.val))

    # draw line to parent.
    if parent_rect:
        utilities.draw_node_connects(screen, parent_rect, node_rect, start_location="bottom", end_location="top")

    draw_tree(screen, node.left, positions, font, highlight_val, parent_rect=node_rect, node_width=node_width,
              highlight_colour=highlight_colour)
    draw_tree(screen, node.right, positions, font, highlight_val, parent_rect=node_rect, node_width=node_width,
              highlight_colour=highlight_colour)


# TODO: Better Comments

def tree_animation(bst: BST, order_list: list, screen: pygame.Surface, duration: int = 500,
                   highlight_col=config.HIGHLIGHT_COLOUR, final_highlight_col=config.HIGHLIGHT_COLOUR):
    """Given an order, highlight a specific node in the bst tree for the given duration. Repeat for each order."""
    for node_val in order_list:

        utilities.fill_screen(screen)
        utilities.draw_text("Binary Search Tree", ((screen.get_width() // 4) + 30, 30), screen)

        if node_val == order_list[-1]:
            draw_tree(screen, bst.root, calc_positions(bst.root), highlight_val=node_val,
                      highlight_colour=final_highlight_col)
        else:
            draw_tree(screen, bst.root, calc_positions(bst.root), highlight_val=node_val,
                      highlight_colour=highlight_col)

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


def run_search_animation(bst: BST, val: int, screen: pygame.Surface):
    """check if value exists, return found and order, and run unsuccessful animation if not"""


    # first search to see if the key exists. This is for visual prompts only
    found, order = bst.search(val)
    if not found:
        tree_animation(bst, order, screen)
        utilities.pop_up_message(screen, "Value not found", error=True)
        return None, None

    return found, order


def delete_node(bst, val: int | str | None, screen: pygame.Surface):
    """attempt to delete given value from the bst tree, and run animation."""
    if val is None:
        return None, None
    else:
        val = int(val)

    found, order = run_search_animation(bst, val, screen)

    if not found: return None
    tree_animation(bst, order, screen, final_highlight_col=config.HIGHLIGHT_DELETE_COLOUR)
    bst.delete(val)

    return None


def search_node(bst: BST, val: int | str | None, screen: pygame.Surface):
    if val is None:
        return None, None
    else:
        val = int(val)
    """attempt to find given value in the bst tree, and run animation."""
    found, order = run_search_animation(bst, val, screen)

    if not found: return None

    tree_animation(bst, order, screen, final_highlight_col=config.HIGHLIGHT_FOUND_COLOUR)

    return order[-1]


def insert_node(bst: BST, val: int | str | None, screen: pygame.Surface):
    """insert given value into the bst tree, and run animation"""
    if val is None:
        return None
    else:
        val = int(val)

    found, order = bst.search(val)
    tree_animation(bst, order, screen)

    bst.insert(val)
    return val


def inorder(bst: BST, screen: pygame.Surface):
    """inorder traversal of the bst tree. Animate given order."""
    order = bst.inorder()
    tree_animation(bst, order, screen)


def preorder(bst: BST, screen: pygame.Surface):
    """preorder traversal of the bst tree. Animate given order."""
    order = bst.preorder()
    tree_animation(bst, order, screen)


def postorder(bst: BST, screen: pygame.Surface):
    """preorder traversal of the bst tree. Animate given order."""
    order = bst.postorder()
    tree_animation(bst, order, screen)


def run_bst_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    bst = BST()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(60)
    bst.insert(80)

    running = True
    current_module = None
    buttons = {
        'Insert': pygame.Rect(120, 480, 150, 50),  # row 1
        'Delete': pygame.Rect(290, 480, 150, 50),
        'Search': pygame.Rect(460, 480, 150, 50),
        'Back': pygame.Rect(630, 480, 150, 50),

        'Pre-Order': pygame.Rect(206, 540, 150, 50),  # row 2
        'Post-Order': pygame.Rect(376, 540, 150, 50),
        'In-Order': pygame.Rect(546, 540, 150, 50),
    }

    entry_rect = pygame.Rect(190, 150, 640, 70)
    heading_rect = pygame.Rect(190, 250, 640, 50)

    current_highlight = None

    while running:

        current_module = utilities.handle_events(buttons, current_module)

        if current_module is not None:
            utilities.handle_button_click(current_module, buttons, screen)

        match current_module:
            case 'Insert':
                node_value = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)
                node_value = insert_node(bst, node_value, screen)
                current_highlight = bst.search(node_value)[1][-1]

            case 'Delete':
                node_value = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)
                delete_node(bst, node_value, screen)
                current_highlight = None

            case 'Search':
                node_value = utilities.text_entry(screen, entry_rect, heading_rect, integer_only=True)
                current_highlight = search_node(bst, node_value, screen)

            case 'Back':
                running = False

            # traversals

            case 'Pre-Order':
                preorder(bst, screen)
            case 'Post-Order':
                postorder(bst, screen)
            case 'In-Order':
                inorder(bst, screen)

        current_module = None

        # wipe screen and draw everything
        utilities.fill_screen(screen)
        utilities.draw_text_in_rect("Binary Search Tree", pygame.Rect(0, 20, screen.get_width(), 20), screen)
        utilities.draw_buttons(buttons, screen)
        draw_tree(screen, bst.root, calc_positions(bst.root), highlight_val=current_highlight)

        pygame.display.flip()

        clock.tick(30)
    return


def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()
    run_bst_menu(screen, clock)


if __name__ == '__main__':
    main()
