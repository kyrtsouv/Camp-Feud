import tkinter as tk

from PIL import Image, ImageTk

from Game import Game


class Gui:

    def __init__(self, title, game: Game):
        self.game = game

        self.root.title(title)
        self.root.geometry("900x900")

        self.scores_frame = tk.Frame(self.root, bg="#fff88f")
        self.scores_frame.pack(side=tk.TOP, fill=tk.X)

        self.x_frame = tk.Frame(self.root, bg="#fff88f", height=50)
        self.x_frame.pack(side=tk.TOP, fill=tk.X)

        self.content_frame = tk.Frame(self.root, background="#fff88f")
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        label = tk.Label(
            self.content_frame,
            text="Άκου τι λέει",
            font=("cambria", 80),
            fg="orange",
            bg="#fff88f",
        )
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # checked
    def setQna(self, qna):
        self.qna = qna
        self.drawContent()

    # checked
    def clearFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # checked
    def clear(self):
        self.drawScores()
        self.clearFrame(self.x_frame)
        self.x_image = None
        self.x_labels = []
        self.clearFrame(self.content_frame)

    # checked
    def drawScores(self):

        self.clearFrame(self.scores_frame)

        scores = self.game.getScores()
        current_score = self.game.current_score
        self.scoreLabel1 = tk.Label(
            self.scores_frame, text=scores[0], font=("cambria", 20), bg="#fff88f"
        )
        self.scoreLabel2 = tk.Label(
            self.scores_frame, text=scores[1], font=("cambria", 20), bg="#fff88f"
        )
        self.currentScoreLabel = tk.Label(
            self.scores_frame, text=current_score, font=("cambria", 20), bg="#fff88f"
        )
        self.scoreLabel1.pack(side=tk.LEFT, padx=20)
        self.scoreLabel2.pack(side=tk.RIGHT, padx=20)
        self.currentScoreLabel.pack(side=tk.BOTTOM, pady=20)

    def addX(self, team):
        side = tk.LEFT if team == 0 else tk.RIGHT

        if self.x_image is None:
            self.x_image = ImageTk.PhotoImage(
                Image.open("resources/redX.png").resize(
                    (50, 50), Image.Resampling.LANCZOS
                )
            )
        self.x_labels.append(tk.Label(self.x_frame, image=self.x_image, bg="#fff88f"))
        self.x_labels[-1].pack(side=side)
