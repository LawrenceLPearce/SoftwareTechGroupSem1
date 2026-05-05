import pygame

def run_heap_visualiser(screen: pygame.Surface, clock: pygame.time.Clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        pygame.display.flip()

        clock.tick(30)