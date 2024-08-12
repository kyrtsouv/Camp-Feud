import pandas as pd
from playsound import playsound as play

from AskTeam import AskTeam


class Game:
    def __init__(self, qna: pd.DataFrame):
        self.team_scores = [0, 0]

        self.qna = [  # questions and answers
            tuple(
                (
                    question,
                    [
                        tuple(answer.split(","))
                        for answer in qna[question].dropna().values.tolist()
                    ],
                )
            )
            for question in qna.keys()
        ]
        self.question_index = -1

    # checked
    def setControlDisplay(self, control, display):
        self.control = control
        self.display = display

    # checked
    def getQna(self):
        self.question_index += 1
        if self.question_index >= len(self.qna):
            return None
        return self.qna[self.question_index]

    # checked
    def nextQuestion(self):
        self.mistakes_counter = 0
        self.current_score = 0
        self.playing_team = None
        self.answersGiven = 0
        self.answersTried = 0
        self.rebound = False

        qna = self.getQna()
        if qna is None:
            return

        self.control.clear()
        self.control.setQna(qna)

        self.display.clear()
        self.display.setQna(qna)

    # checked
    def answerQuestion(self, i):
        self.display.openAnswer(i)
        play("resources/success.mp3")

        self.answersGiven += 1
        self.answersTried += 1

        score = self.qna[self.question_index][1][i][1]

        if self.mistakes_counter < 3:
            self.current_score += int(score)

        if self.rebound:
            self.team_scores[self.getOppositeTeam()] += self.current_score
            self.rebound = False
            self.control.disableFail()

        if self.answersGiven == len(self.qna[self.question_index][1]):
            self.team_scores[self.playing_team] += self.current_score
            self.control.enableNextQuestion()
            self.control.disableFail()

        self.updateScores()

        self.considerAskingForTeam(i)

    # checked
    def fail(self):
        play("resources/fail.mp3")
        self.answersTried += 1

        if self.playing_team is None:
            self.considerAskingForTeam()
            return

        if self.mistakes_counter < 3:
            self.mistakes_counter += 1
            self.display.addX(self.playing_team)
            self.control.addX(self.playing_team)
        if self.mistakes_counter == 3 and not self.rebound:
            self.rebound = True
        elif self.rebound:
            self.team_scores[self.playing_team] += self.current_score
            self.updateScores()
            self.rebound = False
            self.control.disableFail()

    # checked
    def setTeam(self, team):
        self.playing_team = team

    # checked
    def considerAskingForTeam(self, i=None):
        if self.playing_team is None and (
            i == 0 or (self.answersTried % 2 == 0 and self.answersGiven > 0)
        ):
            AskTeam(self)

    # checked
    def getScores(self):
        return self.team_scores

    # checked
    def getOppositeTeam(self):
        return 0 if self.playing_team == 1 else 1

    # checked
    def updateScores(self):
        self.display.drawScores()
        self.control.drawScores()
