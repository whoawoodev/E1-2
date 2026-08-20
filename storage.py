"""기본 퀴즈 데이터와 state.json 읽기/쓰기를 담당하는 모듈."""

import json
import os

from quiz import Quiz

# 실행 위치와 상관없이 프로젝트 루트의 state.json을 가리키도록 절대경로로 만든다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "state.json")

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


def load_state():
    """state.json에서 퀴즈 목록과 최고 점수를 읽어온다.

    파일이 없으면 기본 퀴즈로 시작하고,
    파일이 깨져 있으면 안내한 뒤 기본 퀴즈로 복구한다.
    돌려주는 값: (퀴즈 목록, 최고 점수, 불러오기 성공 여부)
    """
    if not os.path.exists(STATE_FILE):
        return make_default_quizzes(), 0, False

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

        quizzes = []
        for data in state["quizzes"]:
            quizzes.append(Quiz(data["question"], data["choices"], data["answer"]))
        best_score = int(state["best_score"])

        if not quizzes:
            raise ValueError("저장된 퀴즈가 하나도 없습니다.")

        return quizzes, best_score, True

    except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError):
        print("저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다.")
        return make_default_quizzes(), 0, False


def save_state(quizzes, best_score):
    """퀴즈 목록과 최고 점수를 state.json에 UTF-8로 저장한다."""
    state = {
        "quizzes": [q.to_dict() for q in quizzes],
        "best_score": best_score,
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        print("저장에 실패했습니다.")
        return False
