"""프로그램 시작점."""

from quiz_game import QuizGame


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 또는 입력 스트림이 끊긴 경우에도 저장하고 조용히 끝낸다.
        print("\n\n입력이 중단되었습니다. 데이터를 저장하고 종료합니다.\n")
        game.save()


if __name__ == "__main__":
    main()
