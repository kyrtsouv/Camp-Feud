from pandas import read_excel as read

from ControlGUI import ControlGui
from DisplayGUI import DisplayGui
from Game import Game


def main():
    questions = read("resources/questions.xlsx")

    game = Game(questions)

    control = ControlGui(game)
    display = DisplayGui(control, game)

    game.setControlDisplay(control, display)

    control.root.mainloop()
    display.root.mainloop()


if __name__ == "__main__":
    main()
