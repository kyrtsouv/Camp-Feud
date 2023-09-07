import time
import csv

with open("questions.csv", "r", encoding="utf-8") as file:
    data = csv.reader(file)
    questions = []
    for row in data:
        questions.append((row[0], []))

        for item in row[1:]:
            if item != "":
                questions[-1][1].append(item.split(" "))


import pygame
import sys
from math import ceil

pygame.font.init()
pygame.mixer.init()


pygame.display.set_caption("Άκου τι λέει")

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
FONT = pygame.font.SysFont("cambria", 40)
BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))

ORANGE = (255, 69, 0)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

points = [0, 0]


def play(sound):
    pygame.mixer.music.load(sound + ".mp3")
    pygame.mixer.music.play()


def sleep():
    time.sleep(0.3)


def get_keys():
    return pygame.key.get_pressed()


def check_for_events():
    global WIDTH, HEIGHT, WIN, BG
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, 0)
            BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))


def title_screen():
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("cambria", 20)
    title = title_font.render("Άκου τι λέει", 1, ORANGE)

    while True:
        clock.tick(60)
        WIN.blit(BG, (0, 0))
        font = pygame.font.SysFont("cambria", 80)
        title = font.render("Άκου τι λέει", 1, ORANGE)
        title_rect = title.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        WIN.blit(title, title_rect)

        check_for_events()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            for i in range(22):
                WIN.blit(BG, (0, 0))
                font = pygame.font.SysFont("cambria", 80 * int(i**1.2))
                title = font.render("Άκου τι λέει", 1, ORANGE)
                title_rect = title.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                title_rect.bottom -= i * 20
                title_rect.left += i * 20
                WIN.blit(title, title_rect)
                pygame.display.update()
            break
        pygame.display.update()


def draw_answers(question, hidden, SCORE):
    rows = ceil(len(question[1]) / 2)
    d = (HEIGHT - HEIGHT * rows / 10 - 50 - SCORE.get_height()) / (rows + 1)
    q = 0
    answers = [
        FONT.render(
            str(i + 1) + ". " + "".join(word + " " for word in answer), 1, ORANGE
        )
        for i, answer in enumerate(question[1])
    ]
    length = max([answer.get_width() for answer in answers])

    cover = pygame.Rect(0, 0, length + 10, HEIGHT / 10)
    cover.right = WIDTH / 2 - 20

    for i in range(rows):
        WIN.blit(
            answers[q],
            (
                (
                    WIDTH / 2 - 20 - length + (length - answers[q].get_width()) / 2,
                    50
                    + SCORE.get_height()
                    + d * (i + 1)
                    + (HEIGHT / 10) * i
                    + (HEIGHT / 10 - answers[q].get_height()) / 2,
                )
            ),
        )
        cover.top = 50 + SCORE.get_height() + d * (i + 1) + (HEIGHT / 10) * i
        if hidden[q]:
            pygame.draw.rect(WIN, BLACK, cover)
        q += 1
    cover.left = WIDTH / 2 + 20
    for i in range(len(question[1]) - rows):
        WIN.blit(
            answers[q],
            (
                (
                    WIDTH / 2 + 20 + (length - answers[q].get_width()) / 2,
                    50
                    + SCORE.get_height()
                    + d * (i + 1)
                    + (HEIGHT / 10) * i
                    + (HEIGHT / 10 - answers[q].get_height()) / 2,
                )
            ),
        )
        cover.top = 50 + SCORE.get_height() + d * (i + 1) + (HEIGHT / 10) * i
        if hidden[q]:
            pygame.draw.rect(WIN, BLACK, cover)
        q += 1


def draw_window(question, hidden, score):
    WIN.blit(BG, (0, 0))
    PNT = [
        FONT.render(str(points[0]), 1, ORANGE),
        FONT.render(str(points[1]), 1, ORANGE),
    ]
    WIN.blit(PNT[0], ((20, 20)))
    WIN.blit(PNT[1], ((WIDTH - 20 - PNT[1].get_width(), 20)))

    SCORE = FONT.render(score, 1, ORANGE)
    WIN.blit(SCORE, ((WIDTH / 2 - SCORE.get_width() / 2, 50)))
    draw_answers(question, hidden, SCORE)

    pygame.display.update()


def handle_answers(question, hidden, score, errors, team):
    def fail():
        if errors[0] <= 3:
            play("fail")
        errors[0] += 1
        sleep()
        return True

    def check_key(key, length):
        if get_keys()[key] and len(question[1]) > length:
            if hidden[length]:
                if errors[0] < 3:
                    score[0] += int(question[1][length][-1])
                play("success")

                hidden[length] = False
                draw_window(question, hidden, str(score[0]))
                if errors[0] == 3:
                    team[0] = 1 - team[0]
                sleep()
                return True
            else:
                return fail()

    def check_space():
        if get_keys()[pygame.K_SPACE]:
            return fail()

    if (
        check_key(pygame.K_1, 0)
        or check_key(pygame.K_2, 1)
        or check_key(pygame.K_3, 2)
        or check_key(pygame.K_4, 3)
        or check_key(pygame.K_5, 4)
        or check_key(pygame.K_6, 5)
        or check_key(pygame.K_7, 6)
        or check_key(pygame.K_8, 7)
        or check_key(pygame.K_9, 8)
        or check_key(pygame.K_0, 9)
        or check_space()
    ):
        return True
    return False


def main():
    title_screen()
    for question in questions:
        hidden = [True for i in range(len(question[1]))]
        score = [0]
        errors = [0]

        while True:
            while True:
                check_for_events()
                if handle_answers(question, hidden, score, errors, 0):
                    break
                draw_window(question, hidden, str(score[0]))
            while True:
                check_for_events()
                if handle_answers(question, hidden, score, errors, 0):
                    break
                draw_window(question, hidden, str(score[0]))
            if score[0] > 0:
                break
        team_chosen = False
        sleep()

        while not team_chosen:
            check_for_events()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        team = [0]
                        team_chosen = True
                    elif event.key == pygame.K_2:
                        team = [1]
                        team_chosen = True
        sleep()

        errors[0] = 0
        while errors[0] < 3 and max(hidden) > 0:
            check_for_events()
            handle_answers(question, hidden, score, errors, team)
        sleep()

        while max(hidden) > 0:
            check_for_events()
            handle_answers(question, hidden, score, errors, team)
        points[team[0]] += score[0]
        sleep()

        while True:
            check_for_events()
            if get_keys()[pygame.K_RETURN]:
                break
    while True:
        draw_window(question, hidden, str(score[0]))
        check_for_events()


main()
