import tkinter as tk
from math import ceil

from GUI import Gui


class DisplayGui(Gui):
    def __init__(self, control, game):
        self.root = tk.Toplevel()
        super().__init__("Display", game)

        self.root.bind("f", self.toggleFullscreen)
        self.root.protocol("WM_DELETE_WINDOW", control.root.destroy)

    def toggleFullscreen(self, e):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def drawContent(self):
        self.clearFrame(self.content_frame)
        rows = ceil(len(self.qna[1]) / 2)

        self.clearFrame(self.x_frame)

        self.drawScores()
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

        self.answersFrame = tk.Frame(self.content_frame, bg="#fff88f")
        self.answersFrame.pack(side=tk.TOP, padx=20, pady=20)
        self.answers = [
            tk.Label(
                self.answersFrame,
                text=self.qna[1].index(answer) + 1,
                font=("cambria", 20),
                bg="orange",
                border=2,
                relief="raised",
            )
            for answer in self.qna[1]
        ]

        for i, answer in enumerate(self.answers):
            answer.grid(row=i % rows, column=i // rows, padx=10, pady=10, sticky="nsew")

    def openAnswer(self, i):
        self.answers[i].config(text=self.qna[1][i][0] + " - " + self.qna[1][i][1])
