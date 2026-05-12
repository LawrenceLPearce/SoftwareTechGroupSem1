"""A coin change visualiser.
based on https://www.geeksforgeeks.org/dsa/coin-change-dp-7/
Visualisation approach inspired by task_3_3.py (ST2 Week 12 Tutorial)
"""

import pygame
import pygame.time
from utils import utilities
from utils.config import (SECONDARY_COLOUR, HIGHLIGHT_COLOUR, HIGHLIGHT_FOUND_COLOUR, SECONDARY_COLOUR_SHADOW, TEXT_COLOUR, FONT)

COINS = [1, 2, 3]

CELL_WIDTH = 70
CELL_HEIGHT = 50

ENTRY_RECT   = pygame.Rect(300, 280, 300, 60)
HEADING_RECT = pygame.Rect(300, 200, 300, 60)


def _cell_rect(row, col, table_x, table_y) -> pygame.Rect:
    # provides cell instance
    return pygame.Rect(table_x + col * CELL_WIDTH, table_y + row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)


def _draw_table(screen, dp, coins, target_sum, table_x, table_y):
    # uses given values to draw out table, inspired by task 3_3's draw_grid()
    small = pygame.font.SysFont(None, 26)
    rows = len(coins) + 1
    cols = target_sum + 1

    # column headers
    for c in range(cols):
        cx = table_x + c * CELL_WIDTH + CELL_WIDTH // 2
        cy = table_y - CELL_HEIGHT // 2
        lbl = small.render(str(c), True, TEXT_COLOUR)
        screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

    # row headers
    for r in range(rows):
        cx = table_x - CELL_WIDTH // 2
        cy = table_y + r * CELL_HEIGHT + CELL_HEIGHT // 2
        label = "0" if r == 0 else str(coins[r - 1])
        lbl = small.render(label, True, TEXT_COLOUR)
        screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

    # the cells for the table
    for r in range(rows):
        for c in range(cols):
            rect = _cell_rect(r, c, table_x, table_y)

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
    # initialises table using base cases, used tabulation approach from the GeeksforGeeks article.
    n = len(coins)
    dp = [[None] * (target + 1) for _ in range(n + 1)]

    # exactly 1 way to make sum 0 (choose nothing)
    for i in range(n + 1):
        dp[i][0] = 1

    # 0 ways to make any positive sum using 0 coins
    for j in range(1, target + 1):
        dp[0][j] = 0

    return dp


def coin_change_solve(coins, target):
    # computes and returns table
    dp = coin_change_count(coins, target)
    n = len(coins)
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            val = dp[i - 1][j]
            if j - coins[i - 1] >= 0:
                val += dp[i][j - coins[i - 1]]
            dp[i][j] = val
    return dp


def _prompt_target_sum(screen):
    # input box
    background = screen.copy()
    while True:
        screen.blit(background, (0, 0))
        pygame.display.flip()

        raw = utilities.text_entry(screen, ENTRY_RECT, HEADING_RECT,  heading="Enter target sum (1-10)", integer_only=True, max_chars=2)
        if raw is None:
            return None
        if 1 <= int(raw) <= 10:
            return int(raw)
        utilities.pop_up_message(
            screen, "Please enter a number between 1 and 10", error=True
        )


def run_coin_change(screen: pygame.Surface, clock: pygame.time.Clock):
    utilities.fill_screen(screen)
    utilities.draw_text_in_rect("Coin Change", pygame.Rect(0, 20, screen.get_width(), 30), screen)
    pygame.display.flip()

    # initial target sum on entry
    target_sum = _prompt_target_sum(screen)
    if target_sum is None:
        return

    # regenerates layout based on new sum
    cols = target_sum + 1
    rows = len(COINS) + 1
    table_x = (900 - cols * CELL_WIDTH) // 2 + CELL_WIDTH // 2
    table_y = 150

    # buttons
    btn_y = 530
    btn_w = 150
    btn_h = 50
    buttons = {
        "Run": pygame.Rect(130, btn_y, btn_w, btn_h),
        "Reset": pygame.Rect(300, btn_y, btn_w, btn_h),
        "New Sum": pygame.Rect(470, btn_y, btn_w, btn_h),
        "Back": pygame.Rect(640, btn_y, btn_w, btn_h),
    }

    dp = coin_change_count(COINS, target_sum)
    result = None # this is where the result is stored after anim is done
    animating = False # is animation running?
    fill_gen  = None # should be generating?
    last_time = 0
    gen_time  = 20 # time it takes to generate cells in ms

    def make_fill_generator():
        for i in range(1, len(COINS) + 1):
            for j in range(1, target_sum + 1):
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
                result = dp[len(COINS)][target_sum]

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
                            dp = coin_change_count(COINS, target_sum)
                            fill_gen = make_fill_generator()
                            animating = True
                            result = None
                            last_time = pygame.time.get_ticks()

                        elif name == "Reset":
                            dp = coin_change_count(COINS, target_sum)
                            fill_gen = None
                            animating = False
                            result = None

                        elif name == "New Sum":
                            new = _prompt_target_sum(screen)
                            if new is not None:
                                target_sum = new
                                cols = target_sum + 1
                                rows = len(COINS) + 1
                                table_x = (900 - cols * CELL_WIDTH) // 2 + CELL_WIDTH // 2
                                dp = coin_change_count(COINS, target_sum)
                                fill_gen = None
                                animating = False
                                result = None

                                def make_fill_generator():
                                    for i in range(1, len(COINS) + 1):
                                        for j in range(1, target_sum + 1):
                                            yield i, j

                        elif name == "Back":
                            running = False

        utilities.fill_screen(screen)
        utilities.draw_text_in_rect("Coin Change", pygame.Rect(0, 20, screen.get_width(), 30), screen)

        small = pygame.font.SysFont(None, 26)
        desc = small.render(f"Coins {COINS}    Target sum is {target_sum}", True, TEXT_COLOUR)
        screen.blit(desc, desc.get_rect(centerx=screen.get_width() // 2, y=58))

        utilities.draw_buttons(buttons, screen)
        _draw_table(screen, dp, COINS, target_sum, table_x, table_y)

        # results
        if result is not None:
            res_lbl = FONT.render(f"{result} ways to make {target_sum}", True, TEXT_COLOUR)
            screen.blit(res_lbl, res_lbl.get_rect(
                centerx=screen.get_width() // 2,
                y=table_y + rows * CELL_HEIGHT + 20))

        pygame.display.flip()
        clock.tick(60)