import tkinter as tk


class AskTeam:
    def __init__(self, game):
        self.root = tk.Toplevel()
        self.root.title("Ask Team")
        self.root.geometry("400x400")
        self.root.configure(bg="#fff88f")

        self.root.grab_set()

        self.game = game

        ask_team_label = tk.Label(
            self.root,
            text="Ποιά ομάδα θα παίξει;",
            font=("cambria", 30),
            bg="#fff88f",
        )

        self.root.protocol("WM_DELETE_WINDOW", self.disableExit)

        ask_team_label.place(relx=0.5, rely=0.5, anchor="center")

        button_frame = tk.Frame(self.root, bg="#fff88f")
        button_frame.pack(side="bottom", pady=20)

        button1 = tk.Button(
            button_frame,
            text="Ομάδα 1",
            font=("cambria", 20),
            command=self.answer0,
        )

        button2 = tk.Button(
            button_frame,
            text="Ομάδα 2",
            font=("cambria", 20),
            command=self.answer1,
        )

        button1.pack(side="left", padx=20)
        button2.pack(side="right", padx=20)

        self.root.mainloop()

    def disableExit(self):
        pass

    def answer0(self):
        self.game.setTeam(0)
        self.root.destroy()

    def answer1(self):
        self.game.setTeam(1)
        self.root.destroy()
