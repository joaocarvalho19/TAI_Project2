import argparse
from fcm import FCM
from lang import Lang

def bonus_challenge(example, target, k1, k2, alpha):

    if k1 > k2:
        aux = k1
        k1 = k2
        k2 = aux
        print("Had to switch them")

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


def bonus(): #src/bonus.py -k1 2 -k2 4 -a 0.1 -rf refs/eng_GB.latn.English.EP7.utf8 -t examples/pt_en.txt

    parser = argparse.ArgumentParser(description="Bonus challenge",
                                     usage="python3 src/bonus.py -k1 <value of k1> -k2 <value of k2> -a <value of alpha> -rf <reference file> -t <target file>")

    parser.add_argument("-k1", help="Value of k1", type=int, default=2)
    parser.add_argument("-k2", help="Value of k2", type=int, default=4)
    parser.add_argument("-a", help="Value of alpha", type=float, default=0.1)

    parser.add_argument("-rf", help="Path to reference file", type=str, required=True)
    parser.add_argument("-t", help="Path to target file", type=str, required=True)

    args = parser.parse_args()

    bonus_challenge(args.rf, args.t, args.k1, args.k2, args.a)

if __name__ == "__main__":
    bonus()


'''
if __name__ == "__main__":
    k1 = 2
    k2 = 4
    alpha = 0.1
    example = "eng_GB.latn.English.EP7.utf8"
    target = "../examples/dorian.txt"


    lang1, lang2 = bonus_challenge("../refs/" + example, target, k1, k2, alpha)

'''
