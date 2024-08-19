import pygame
from Game import Game

if __name__ == '__main__':
    try:
        game = Game(0)
        game.run()
        pygame.quit()
    except Exception as e:
        print(f"Извините за недразумение :( "
              f"\nНапишите, пожалуйста, в поддержку прикрепив код ошибки : {e}")

