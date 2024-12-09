# Madeline Clausen
# 60633236

import pygame
import project4_logic
import random

FALLER_SPEED = 1000

class JewelGame:

    def __init__(self):
        self._game = project4_logic.GameState()
        self._board = self._game.get_board()


    def display_board(self, surface: pygame.Surface):
        """ Loads the jewel images and prints a 13x6 grid. """
        grid_size_x = int(surface.get_width() / 6)
        grid_size_y = int(surface.get_height() / 13)
        for row in range(2, 15):
            for col in range(6):
                rect = pygame.Rect(col*grid_size_x, (row-2)*grid_size_y,
                                   grid_size_x, grid_size_y)
                if self._board[row][col].value() == 'S':
                    if self._board[row][col].state() == 'MATCH':
                        image = pygame.image.load('jewel1_match.png')
                    elif self._board[row][col].state() == 'LANDED':
                        image = pygame.image.load('jewel1_landed.png')
                    else:
                        image = pygame.image.load('jewel1.png')
                elif self._board[row][col].value() == 'T':
                    if self._board[row][col].state() == 'MATCH':
                        image = pygame.image.load('jewel2_match.png')
                    elif self._board[row][col].state() == 'LANDED':
                        image = pygame.image.load('jewel2_landed.png')
                    else:
                        image = pygame.image.load('jewel2.png')
                elif self._board[row][col].value() == 'V':
                    if self._board[row][col].state() == 'MATCH':
                        image = pygame.image.load('jewel3_match.png')
                    elif self._board[row][col].state() == 'LANDED':
                        image = pygame.image.load('jewel3_landed.png')
                    else:
                        image = pygame.image.load('jewel3.png')
                elif self._board[row][col].value() == 'W':
                    if self._board[row][col].state() == 'MATCH':
                        image = pygame.image.load('jewel4_match.png')
                    elif self._board[row][col].state() == 'LANDED':
                        image = pygame.image.load('jewel4_landed.png')
                    else:
                        image = pygame.image.load('jewel4.png')
                elif self._board[row][col].value() == 'X':
                    if self._board[row][col].state() == 'MATCH':
                        image = pygame.image.load('jewel5_match.png')
                    elif self._board[row][col].state() == 'LANDED':
                        image = pygame.image.load('jewel5_landed.png')
                    else:
                        image = pygame.image.load('jewel5.png')
                elif self._board[row][col].value() == 'Y':
                    if self._board[row][col].state() == 'MATCH':
                        image = pygame.image.load('jewel6_match.png')
                    elif self._board[row][col].state() == 'LANDED':
                        image = pygame.image.load('jewel6_landed.png')
                    else:
                        image = pygame.image.load('jewel6.png')
                elif self._board[row][col].value() == 'Z':
                    if self._board[row][col].state() == 'MATCH':
                        image = pygame.image.load('jewel7_match.png')
                    elif self._board[row][col].state() == 'LANDED':
                        image = pygame.image.load('jewel7_landed.png')
                    else:
                        image = pygame.image.load('jewel7.png')
                else:
                    image = pygame.image.load('jewel0.PNG')
                    
                jewel_image = pygame.transform.scale(image, (grid_size_x, grid_size_y))
                surface.blit(jewel_image, rect)

    def run(self) -> None:
        """ Main loop of code. Handles time, the actions to
            take when the user presses certain keys, and
            the GameState. """
        pygame.init()
        self._game.create(13, 6, ['#' * 6] * 13)
        jewel_options = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        faller_move_event = pygame.USEREVENT + 1
        try:
            surface = pygame.display.set_mode((300, int((300/6)*13)), pygame.RESIZABLE)
            running = True
            clock = pygame.time.Clock()
            surface.fill(pygame.Color(168, 169, 173))
            pygame.time.set_timer(faller_move_event, FALLER_SPEED)
            while running:
                clock.tick(3000)
                random.shuffle(jewel_options)
                faller = [jewel_options[0], jewel_options[1], jewel_options[2]]
                self._game.create_faller(random.randint(1, 6), faller)
                JewelGame.display_board(self, surface)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    elif event.type == pygame.VIDEORESIZE:
                        surface = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    elif event.type == faller_move_event:
                        self._game.passage_of_time()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self._game.move_faller_left()
                        elif event.key == pygame.K_RIGHT:
                            self._game.move_faller_right()
                        elif event.key == pygame.K_SPACE:
                            self._game.rotate_faller()
                        else:
                            pass
                    else:
                        pass
                self._game.update()
                if self._game.check_game_over():
                    surface.fill(pygame.Color(235, 75, 211))
                    font = pygame.font.SysFont(None, 40)
                    game_over = font.render('GAME OVER', True, pygame.Color(0,0,0))
                    surface.blit(game_over, (65, 150))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    break
                pygame.display.flip()

        finally:
            pygame.quit()


if __name__ == '__main__':
    JewelGame().run()
