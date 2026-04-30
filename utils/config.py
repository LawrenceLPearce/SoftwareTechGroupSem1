import pygame
pygame.init()

FONT = pygame.font.SysFont(None, 36)

# screen
WIDTH, HEIGHT = 900, 600


# colours
BACKGROUND_COLOUR = pygame.Color("#F5F0EB")
TEXT_COLOUR = pygame.Color("Black")
ERROR_COLOUR = pygame.Color("#C44A4A")  # For error messages
SECONDARY_COLOUR = pygame.Color("#7EC8A4")  # also used for buttons
SECONDARY_COLOUR_SHADOW = pygame.Color("#6DB893")
NODE_COLOUR = pygame.Color("#53ffdd")
NODE_EDGE_COLOUR = pygame.Color("#53ffdd")
HIGHLIGHT_COLOUR = pygame.Color("#ffd869")
HIGHLIGHT_FOUND_COLOUR = pygame.Color("#34ff66")
HIGHLIGHT_DELETE_COLOUR = pygame.Color("#C44A4A")

GRAPH_START_COLOUR = pygame.Color("#c679ff")
GRAPH_END_COLOUR = pygame.Color("#3aff7e")
GRAPH_OBSTACLE_COLOUR = pygame.Color("#3a1923")

