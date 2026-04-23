import pygame
import utilities

"""Node and BST classes are based on code pulled from Week8"""
#TODO: reference


class Node:
    """Class representing a single node in the Binary Search Tree."""
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

class BST:
    """Binary Search Tree class implementing insert, search, delete, and traversal methods."""
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert a new node into the BST."""
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, root, key):
        """Helper method for inserting recursively."""
        if key < root.val:
            if root.left is None:
                root.left = Node(key)
            else:
                self._insert_recursive(root.left, key)
        else:
            if root.right is None:
                root.right = Node(key)
            else:
                self._insert_recursive(root.right, key)

    def inorder(self):
        """Perform an inorder traversal (Left → Root → Right) and print elements in sorted order."""
        self._inorder_recursive(self.root)
        print()

    def _inorder_recursive(self, root):
        """Helper method for recursive inorder traversal."""
        if root:
            self._inorder_recursive(root.left)
            print(root.val, end=" ")
            self._inorder_recursive(root.right)

    def preorder(self):
        """Perform a preorder traversal (Root → Left → Right) and print elements."""
        self._preorder_recursive(self.root)
        print()

    def _preorder_recursive(self, root):
        """Helper method for recursive preorder traversal."""
        if root:
            print(root.val, end=" ")
            self._preorder_recursive(root.left)
            self._preorder_recursive(root.right)

    def postorder(self):
        """Perform a postorder traversal (Left → Right → Root) and print elements."""
        self._postorder_recursive(self.root)
        print()

    def _postorder_recursive(self, root):
        """Helper method for recursive postorder traversal."""
        if root:
            self._postorder_recursive(root.left)
            self._postorder_recursive(root.right)
            print(root.val, end=" ")

    def search(self, key):
        """Search for a key in BST. Returns True if found, False otherwise."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, root, key):
        """Helper method for recursive search."""
        if root is None:
            return False
        if root.val == key:
            return True
        if key < root.val:
            return self._search_recursive(root.left, key)
        return self._search_recursive(root.right, key)

    def delete(self, key):
        """Delete a node from BST."""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, root, key):
        """Helper method for recursive deletion."""
        if root is None:
            return root

        if key < root.val:
            root.left = self._delete_recursive(root.left, key)
        elif key > root.val:
            root.right = self._delete_recursive(root.right, key)
        else:
            # Case 1: Node has no child
            if root.left is None and root.right is None:
                return None
            # Case 2: Node has one child
            elif root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            # Case 3: Node has two children
            temp = self._min_value_node(root.right)
            root.val = temp.val
            root.right = self._delete_recursive(root.right, temp.val)

        return root

    @staticmethod
    def _min_value_node(node):
        """Helper function to find the minimum value node in the right subtree."""
        current = node
        while current.left:
            current = current.left
        return current

    def display_tree(self, root=None, level=0, prefix="Root: "):
        """Display tree structure visually in console."""
        if root is None:
            root = self.root
        if root is not None:
            print(" " * (level * 4) + prefix + str(root.val))
            if root.left or root.right:
                if root.left:
                    self.display_tree(root.left, level + 1, "L-- ")
                else:
                    print(" " * ((level + 1) * 4) + "L-- None")
                if root.right:
                    self.display_tree(root.right, level + 1, "R-- ")
                else:
                    print(" " * ((level + 1) * 4) + "R-- None")

#TODO: Instruction Area
#TODO: Add node button + text enter
#TODO: Delete node button + text area
# TODO: Display tree edit
# TODO: SEARCH Highlight

def bst_menu(screen: pygame.Surface):
    utilities.fill_screen(screen)
    utilities.draw_text("Binary Search Tree", ((screen.get_width() // 4) + 30, 30), screen)
    buttons = {
        'Add Node':     pygame.Rect(50, 150, 190, 50),
        'Delete Node':  pygame.Rect(50, 230, 190, 50),
        'Search':       pygame.Rect(50, 310, 190, 50),
        'Back to Menu': pygame.Rect(50, 390, 190, 50),
    }
    utilities.draw_buttons(buttons, screen)
    pygame.display.flip()
    return buttons

def run_bst_menu(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    current_module = None
    buttons = bst_menu(screen)

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

            elif current_module == 'Delete Node':
                utilities.handle_button_click("Delete Node", buttons, screen)

            elif current_module == 'Search':
                utilities.handle_button_click("Search", buttons, screen)

            elif current_module == 'Back to Menu':
                utilities.handle_button_click("Back to Menu", buttons, screen)
                running = False

            # For demo, after module ends return to menu
            current_module = None

        clock.tick(30)

    return


if __name__ == '__main__':
    def main():
        # Example usage
        bst = BST()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)

        print("Inorder Traversal (Sorted):")
        bst.inorder()

        print("Preorder Traversal (Root → Left → Right):")
        bst.preorder()

        print("Postorder Traversal (Left → Right → Root):")
        bst.postorder()

        # Display the BST structure
        print("\nBinary Tree Structure:")
        bst.display_tree()

        # Search for a node
        key = 40
        if bst.search(key):
            print(f"\n{key} found in BST")
        else:
            print(f"\n{key} not found in BST")

        # Delete a node
        bst.delete(50)
        print("\nBinary Tree Structure After Deleting 50:")
        bst.display_tree()
    main()
