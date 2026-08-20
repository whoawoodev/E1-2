"""메뉴 흐름과 게임 진행을 담당하는 모듈."""

import datetime
import random

import storage
from quiz import Quiz

HINT_PENALTY = 5   # 힌트 한 번당 깎는 점수
CHOICE_COUNT = 4   # 문제 하나가 갖는 선택지 개수


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
    """퀴즈 목록과 점수 기록을 들고 게임 전체를 진행하는 클래스."""

    def __init__(self):
        self.quizzes, self.best_score, self.history, self.loaded = storage.load_state()

    def show_title(self):
        print("=" * 40)
        print("             이산수학 퀴즈")
        print("=" * 40)
        if self.loaded:
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
            print("=" * 40)

    def show_menu(self):
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    def play(self):
        """문제 수를 고르고, 무작위 순서로 출제해 점수를 계산한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.\n")
            return

        total = len(self.quizzes)
        count = ask_number(f"\n문제 몇 개 풀까요? (1-{total}): ", 1, total)
        picked_quizzes = random.sample(self.quizzes, count)

        print(f"\n퀴즈를 시작합니다! (총 {count}문제, 정답 대신 0을 누르면 힌트)\n")

        correct = 0
        hint_count = 0
        for number, quiz in enumerate(picked_quizzes, start=1):
            quiz.show(number)

            used_hint = False
            while True:
                picked = ask_number("정답 입력 (0: 힌트): ", 0, CHOICE_COUNT)
                if picked != 0:
                    break
                quiz.show_hint()
                if quiz.hint and not used_hint:
                    used_hint = True
                    hint_count += 1

            if quiz.is_correct(picked):
                print("정답입니다!\n")
                correct += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.\n")

        base_score = round(correct / count * 100)
        penalty = hint_count * HINT_PENALTY
        score = max(base_score - penalty, 0)

        print("=" * 40)
        print(f"결과: {count}문제 중 {correct}문제 정답! ({base_score}점)")
        if penalty:
            print(f"힌트 {hint_count}회 사용 → {penalty}점 차감, 최종 {score}점")

        if score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
        print("=" * 40 + "\n")

        self.record_history(count, score)
        self.save()

    def record_history(self, count, score):
        """이번 판의 날짜, 푼 문제 수, 점수를 기록에 남긴다."""
        played_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.history.append({"played_at": played_at, "count": count, "score": score})

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 넣고 파일에 저장한다."""
        print("\n새로운 퀴즈를 추가합니다.\n")

        question = ask_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, CHOICE_COUNT + 1):
            choices.append(ask_text(f"선택지 {i}: "))
        answer = ask_number(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        hint = input("힌트 (없으면 그냥 Enter): ").strip()

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save()
        print(f"\n퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)\n")

    def list_quizzes(self):
        """등록된 퀴즈의 문제 문장을 번호와 함께 보여준다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.\n")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40 + "\n")

    def delete_quiz(self):
        """번호를 골라 퀴즈를 목록에서 지운다."""
        if not self.quizzes:
            print("\n삭제할 퀴즈가 없습니다.\n")
            return

        self.list_quizzes()
        number = ask_number("삭제할 퀴즈 번호 (0: 취소): ", 0, len(self.quizzes))
        if number == 0:
            print("\n취소했습니다.\n")
            return

        removed = self.quizzes.pop(number - 1)
        self.save()
        print(f"\n삭제했습니다: {removed.question}\n")

    def show_score(self):
        """최고 점수와 최근 게임 기록을 보여준다."""
        if self.best_score == 0 and not self.history:
            print("\n아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요.\n")
            return

        print(f"\n최고 점수: {self.best_score}점\n")

        if self.history:
            print("최근 기록")
            print("-" * 40)
            for record in self.history[-5:]:
                print(f"{record['played_at']}   {record['count']}문제   {record['score']}점")
            print("-" * 40 + "\n")

    def save(self):
        """현재 퀴즈 목록과 점수 기록을 state.json에 저장한다."""
        return storage.save_state(self.quizzes, self.best_score, self.history)

    def run(self):
        self.show_title()
        while True:
            self.show_menu()
            picked = ask_number("선택: ", 1, 6)

            if picked == 1:
                self.play()
            elif picked == 2:
                self.add_quiz()
            elif picked == 3:
                self.list_quizzes()
            elif picked == 4:
                self.show_score()
            elif picked == 5:
                self.delete_quiz()
            elif picked == 6:
                self.save()
                print("\n게임을 종료합니다. 데이터를 저장했습니다.\n")
                break
