import tkinter as tk
from math import ceil

from GUI import Gui


class ControlGui(Gui):
    def __init__(self, game):
        self.root = tk.Tk()
        super().__init__("Control", game)

        self.next_question_button = tk.Button(
            self.root,
            text="Επόμενη Ερώτηση",
            command=self.game.nextQuestion,
            font=("cambria", 20),
        )
        self.next_question_button.pack(side=tk.BOTTOM, pady=20)

    # checked
    def drawContent(self):
        rows = ceil(len(self.qna[1]) / 2)

        question = tk.Label(
            self.content_frame,
            text=self.qna[0],
            font=("cambria", 30),
            fg="orange",
            bg="#fff88f",
        )
        question.pack(side=tk.TOP, pady=20)
        question.bind(
            "<Configure>", lambda e: question.config(wraplength=self.root.winfo_width())
        )

        self.buttons_frame = tk.Frame(self.content_frame, bg="#fff88f")
        self.buttons_frame.pack(side=tk.TOP, padx=20, pady=20)
        self.buttons = []
        for i, answer in enumerate(self.qna[1]):
            self.buttons.append(
                tk.Button(
                    self.buttons_frame,
                    text=str(i) + ")  " + answer[0] + " - " + answer[1],
                    font=("cambria", 20),
                )
            )

        for i, button in enumerate(self.buttons):
            button.grid(row=i % rows, column=i // rows, padx=10, pady=10, sticky="nsew")
            button.bind("<Configure>", lambda e: button.config(wraplength=e.width))
            button.configure(command=lambda i=i: self.openAnswer(i))

        self.fail_button = tk.Button(
            self.content_frame,
            text="Αποτυχία",
            command=self.game.fail,
            font=("cambria", 20),
        )
        self.fail_button.pack(side=tk.BOTTOM, pady=20)

        self.next_question_button.config(state="disabled")

    # checked
    def disableFail(self):
        self.fail_button.config(state="disabled")

    # checked
    def enableNextQuestion(self):
        self.next_question_button.config(state="normal")

    # checked
    def openAnswer(self, i):
        self.buttons[i]["state"] = "disabled"
        self.game.answerQuestion(i)
