class Question:
    def __init__(self, text, correct, answers):
        self.text = text
        self.correct = correct
        self.answers = answers


class Quiz:
    def __init__(self, questions):
        self.questions = questions
