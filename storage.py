"""기본 퀴즈 데이터를 담아 두는 모듈."""

from quiz import Quiz

# 주제: 이산수학 기초
DEFAULT_QUIZ_DATA = [
    {
        "question": "서로 다른 책 3권을 일렬로 나열하는 방법은 모두 몇 가지인가?",
        "choices": ["3가지", "6가지", "8가지", "9가지"],
        "answer": 2,
    },
    {
        "question": "두 집합 A = {1, 2, 3}, B = {3, 4, 5}의 교집합은?",
        "choices": ["{1, 2}", "{3}", "{1, 2, 3, 4, 5}", "공집합"],
        "answer": 2,
    },
    {
        "question": "원소가 3개인 집합의 부분집합은 모두 몇 개인가?",
        "choices": ["3개", "6개", "8개", "9개"],
        "answer": 3,
    },
    {
        "question": "두 명제가 모두 참일 때만 결과가 참이 되는 논리 연산은?",
        "choices": ["논리합(OR)", "논리곱(AND)", "부정(NOT)", "배타적 논리합(XOR)"],
        "answer": 2,
    },
    {
        "question": "명제 \"P이면 Q이다\"의 역(逆)은?",
        "choices": [
            "Q이면 P이다",
            "P가 아니면 Q가 아니다",
            "Q가 아니면 P가 아니다",
            "P이고 Q이다",
        ],
        "answer": 1,
    },
    {
        "question": "명제 변수가 2개일 때 진리표의 행은 모두 몇 개인가?",
        "choices": ["2개", "3개", "4개", "8개"],
        "answer": 3,
    },
]


def make_default_quizzes():
    """기본 퀴즈 데이터를 Quiz 객체 목록으로 만들어 돌려준다."""
    quizzes = []
    for data in DEFAULT_QUIZ_DATA:
        quizzes.append(Quiz(data["question"], data["choices"], data["answer"]))
    return quizzes
