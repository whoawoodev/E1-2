"""퀴즈 한 문제를 표현하는 모듈."""


class Quiz:
    """문제 하나를 담는 클래스.

    question: 문제 문장 (str)
    choices : 선택지 4개 (list)
    answer  : 정답 번호 1~4 (int)
    hint    : 힌트 문장 (str, 없으면 빈 문자열)
    """

    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def show(self, number):
        """문제와 선택지를 화면에 출력한다."""
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def is_correct(self, picked):
        """사용자가 고른 번호가 정답인지 알려준다."""
        return picked == self.answer

    def show_hint(self):
        """힌트를 보여준다. 힌트가 없으면 없다고 알린다."""
        if self.hint:
            print(f"힌트: {self.hint}\n")
        else:
            print("이 문제에는 힌트가 없습니다.\n")

    def to_dict(self):
        """state.json에 저장할 수 있는 형태로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }
