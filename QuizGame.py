import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

class QuizLogic:
    def __init__(self):
        self.questions = [
            {"question": "What is the capital of France?", "answers": ["Paris", "Berlin", "London", "Madrid"], "correct": "Paris"},
            {"question": "What is the capital of Mongolia", "answers": ["Beijing", "Ulaan Bator", "Seul", "New Delhi"], "correct": "Ulaan Bator"},
            {"question": "What is the capital of America", "answers": ["New York", "Washington DC", "Austin", "Chicago"], "correct": "Washington DC"}
        ]
        self.current_question = 0
        self.score = 0

    def check_answer(self, selected_answer):
        correct_answer = self.questions[self.current_question]["correct"]
        if selected_answer == correct_answer:
            self.score += 1

    def next_question(self):
        self.current_question += 1

    def get_current_question(self):
        return self.questions[self.current_question] if self.current_question < len(self.questions) else None

    def reset_quiz(self):
        self.current_question = 0
        self.score = 0

class QuizApp(QWidget):
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 300

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quiz Application")
        self.setGeometry(100, 100, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.quiz_logic = QuizLogic()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.question_label = QLabel(self.quiz_logic.get_current_question()["question"])
        layout.addWidget(self.question_label)

        for answer in self.quiz_logic.get_current_question()["answers"]:
            answer_button = QPushButton(answer)
            answer_button.clicked.connect(self.check_answer)
            layout.addWidget(answer_button)

        self.setLayout(layout)

    def check_answer(self):
        selected_button = self.sender()
        selected_answer = selected_button.text()
        self.quiz_logic.check_answer(selected_answer)
        self.next_question()

    def next_question(self):
        self.quiz_logic.next_question()
        current_question = self.quiz_logic.get_current_question()

        if current_question:
            self.update_question(current_question)
        else:
            self.show_result()

    def update_question(self, question):
        self.question_label.setText(question["question"])

        for button in self.findChildren(QPushButton):
            button.setParent(None)

        for answer in question["answers"]:
            answer_button = QPushButton(answer)
            answer_button.clicked.connect(self.check_answer)
            self.layout().addWidget(answer_button)

    def show_result(self):
        result_message = f"You got {self.quiz_logic.score} out of {len(self.quiz_logic.questions)} questions correct!"
        restart = QMessageBox.question(self, "Quiz Result", result_message + "\nDo you want to restart the quiz?", QMessageBox.Yes | QMessageBox.No)

        if restart == QMessageBox.Yes:
            self.quiz_logic.reset_quiz()
            self.update_question(self.quiz_logic.get_current_question())
        else:
            sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    quiz_app.show()
    sys.exit(app.exec_())