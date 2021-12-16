from random import random
import time
import math
from sys import argv
from fcm import FCM
from findlang import FindLang
from lang import Lang
import os


def bonus_challenge(example, target, k1, k2, alpha):

    fcm1 = FCM(example, k1, alpha)
    probs1, prio1 = fcm1.run()
    lang1 = Lang(target, k1, alpha, probs1, fcm1.getAlphabet(), fcm1.getAppearances())
    bitslist1 = lang1.runBonus()

    somabits1 = 0
    for i in bitslist1:
        somabits1 += i

    print(somabits1)


    fcm2 = FCM(example, k2, alpha)
    probs2, prio2 = fcm2.run()
    lang2 = Lang(target, k2, alpha, probs2, fcm2.getAlphabet(), fcm2.getAppearances())
    bitslist2 = lang2.runBonus()

    somabits2 = 0
    for i in bitslist2:
        somabits2 += i

    print(somabits2)

    lang1.hybrid(bitslist1, bitslist2)

    return lang1, lang2




if __name__ == "__main__":
    k1 = 2
    k2 = 4
    alpha = 0.1
    example = "eng_GB.latn.English.EP7.utf8"
    target = "../examples/dorian.txt"


    lang1, lang2 = bonus_challenge("../refs/" + example, target, k1, k2, alpha)


