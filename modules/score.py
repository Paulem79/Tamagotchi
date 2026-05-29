import config


def score_decompte():
    config.score += 1
    return ("Score :", config.score)
