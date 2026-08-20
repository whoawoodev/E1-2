"""메뉴 흐름과 게임 진행을 담당하는 모듈."""

import storage


def ask_number(prompt, low, high):
    """low~high 사이의 정수를 받을 때까지 다시 묻는다."""
    while True:
        entered = input(prompt).strip()

        if entered == "":
            print(f"아무것도 입력되지 않았습니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(entered)
        except ValueError:
            print(f"잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue

        if number < low or number > high:
            print(f"{low}-{high} 사이의 숫자를 입력하세요.")
            continue

        return number


def ask_text(prompt):
    """빈 값이 아닌 문자열을 받을 때까지 다시 묻는다."""
    while True:
        entered = input(prompt).strip()
        if entered == "":
            print("빈 값은 입력할 수 없습니다. 다시 입력하세요.")
            continue
        return entered


class QuizGame:
    """퀴즈 목록과 최고 점수를 들고 게임 전체를 진행하는 클래스."""

    def __init__(self):
        self.quizzes = storage.make_default_quizzes()
        self.best_score = 0

    def show_title(self):
        print("=" * 40)
        print("             이산수학 퀴즈")
        print("=" * 40)

    def show_menu(self):
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play(self):
        """저장된 퀴즈를 순서대로 출제하고 점수를 계산한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.\n")
            return

        total = len(self.quizzes)
        print(f"\n퀴즈를 시작합니다! (총 {total}문제)\n")

        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.show(number)
            picked = ask_number("정답 입력: ", 1, 4)
            if quiz.is_correct(picked):
                print("정답입니다!\n")
                correct += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.\n")

        score = round(correct / total * 100)
        print("=" * 40)
        print(f"결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print("=" * 40 + "\n")

    def run(self):
        self.show_title()
        while True:
            self.show_menu()
            picked = ask_number("선택: ", 1, 5)

            if picked == 1:
                self.play()
            elif picked == 2:
                print("\n아직 준비 중인 기능입니다.\n")
            elif picked == 3:
                print("\n아직 준비 중인 기능입니다.\n")
            elif picked == 4:
                print("\n아직 준비 중인 기능입니다.\n")
            elif picked == 5:
                print("\n게임을 종료합니다.\n")
                break
