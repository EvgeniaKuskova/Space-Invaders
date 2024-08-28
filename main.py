from Game import Game

if __name__ == '__main__':
    try:
        game = Game(0, 0)
        game.run()
    except Exception as e:
        print(f"Извините за недразумение, обратитесь в поддержку, прикрепив текст ошибки {e}")
