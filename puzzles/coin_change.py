# based on https://www.geeksforgeeks.org/dsa/coin-change-dp-7/

import pygame
import pygame.time
from utils import utilities
from utils.config import (SECONDARY_COLOUR, HIGHLIGHT_COLOUR, HIGHLIGHT_FOUND_COLOUR, SECONDARY_COLOUR_SHADOW, TEXT_COLOUR, FONT)

COINS = [1, 2, 3]
SUM = 10 # target sum

ROWS = len(COINS) + 1 # + 1 is extra row
COLS = SUM + 1

CELL_WIDTH = 70
CELL_HEIGHT = 50

TABLE_X = (900 - COLS * CELL_WIDTH) // 2 + CELL_WIDTH // 2
TABLE_Y = 150


def _cell_rect(row, col) -> pygame.Rect:
    # provides cell instance
    return pygame.Rect(TABLE_X + col * CELL_WIDTH, TABLE_Y + row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)


def _draw_table(screen, dp):
    # uses given values to draw out table, inspired by task 3_3's draw_grid()
    small = pygame.font.SysFont(None, 26)

    # column headers
    for c in range(COLS):
        cx = TABLE_X + c * CELL_WIDTH + CELL_WIDTH // 2
        cy = TABLE_Y - CELL_HEIGHT // 2
        lbl = small.render(str(c), True, TEXT_COLOUR)
        screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

    # row headers
    for r in range(ROWS):
        cx = TABLE_X - CELL_WIDTH // 2
        cy = TABLE_Y + r * CELL_HEIGHT + CELL_HEIGHT // 2
        label = "0" if r == 0 else str(COINS[r - 1])
        lbl = small.render(label, True, TEXT_COLOUR)
        screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

    # the cells for the table
    for r in range(ROWS):
        for c in range(COLS):
            rect = _cell_rect(r, c)

            if dp[r][c] == "active":
                col = SECONDARY_COLOUR_SHADOW
            elif dp[r][c] is not None:
                col = HIGHLIGHT_FOUND_COLOUR
            else:
                col = SECONDARY_COLOUR_SHADOW

            utilities.draw_button_shadow(rect, screen)
            pygame.draw.rect(screen, col, rect, border_radius=8)

            if dp[r][c] is not None and dp[r][c] != "active":
                val_lbl = FONT.render(str(dp[r][c]), True, TEXT_COLOUR)
                screen.blit(val_lbl, val_lbl.get_rect(center=rect.center))


def coin_change_count(coins, target):
    # intialises table using base cases, used tabulaiton approach from the GeeksforGeeks article.
    n = len(coins)
    dp = [[None] * (target + 1) for _ in range(n + 1)]

    # exactly 1 way to make sum 0 (choose nothing)
    for i in range(n + 1):
        dp[i][0] = 1

    # 0 ways to make any positive sum using 0 coins
    for j in range(1, target + 1):
        dp[0][j] = 0

    return dp


def run_coin_change(screen: pygame.Surface, clock: pygame.time.Clock):
    # buttons
    btn_y = 530
    btn_w = 150
    btn_h = 50
    buttons = {
        "Run": pygame.Rect(200, btn_y, btn_w, btn_h),
        "Reset": pygame.Rect(375, btn_y, btn_w, btn_h),
        "Back": pygame.Rect(550, btn_y, btn_w, btn_h),
    }

    dp = coin_change_count(COINS, SUM)
    result = None # this is where the result is stored after anim is done
    animating = False # is animation running?
    fill_gen = None # should be generating?
    last_time = 0
    gen_time = 20 # time it take to generate cells in ms

    def make_fill_generator():
        for i in range(1, len(COINS) + 1):
            for j in range(1, SUM + 1):
                yield i, j

    running = True
    while running:
        now = pygame.time.get_ticks()

        # progress to next cell based on fill anim
        if animating and fill_gen and now - last_time >= gen_time:
            try:
                r, c = next(fill_gen)
                # ways excluding this coin and ways including it
                val = dp[r - 1][c]
                if c - COINS[r - 1] >= 0:
                    val += dp[r][c - COINS[r - 1]]
                dp[r][c] = val
                last_time = now
            except StopIteration:
                animating = False
                result = dp[len(COINS)][SUM]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        utilities.handle_button_click(name, buttons, screen)

                        if name == "Run" and not animating:
                            # start over, resetting to base cases
                            dp = coin_change_count(COINS, SUM)
                            fill_gen = make_fill_generator()
                            animating = True
                            result = None
                            last_time = pygame.time.get_ticks()

                        elif name == "Reset":
                            dp = coin_change_count(COINS, SUM)
                            fill_gen = None
                            animating = False
                            result = None

                        elif name == "Back":
                            running = False

        utilities.fill_screen(screen)
        utilities.draw_text_in_rect("Coin Change", pygame.Rect(0, 20, screen.get_width(), 30), screen)

        small = pygame.font.SysFont(None, 26)
        desc = small.render(f"Coins {COINS}    Target sum is {SUM}", True, TEXT_COLOUR)
        screen.blit(desc, desc.get_rect(centerx=screen.get_width() // 2, y=58))

        utilities.draw_buttons(buttons, screen)
        _draw_table(screen, dp)

        # results
        if result is not None:
            res_lbl = FONT.render(f"{result} ways to make {SUM}", True,
                                  TEXT_COLOUR)
            screen.blit(res_lbl, res_lbl.get_rect(
                centerx=screen.get_width() // 2,
                y=TABLE_Y + ROWS * CELL_HEIGHT + 20))

        pygame.display.flip()
        clock.tick(60)