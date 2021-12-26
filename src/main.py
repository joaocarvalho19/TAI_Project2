import pickle
from os import listdir
from random import random
import time
import math
from sys import argv
from fcm import FCM
from findlang import FindLang
from lang import Lang
import os


def listToString (l):
    aux = ""
    for a in l:  # last k positions in a string
        if a:
            aux += a

    return aux


def sorting (values): #returns the position chosen
    random_variable_instance = random()
    entropySum = values[0]

    for i in range(len(values)):
        if entropySum < random_variable_instance:
            if i != 0:
                entropySum = entropySum + values[i]
        else:
            return i

    return len(values)-1

def learnLanguage(k, alpha):
    ref_path = 'refs/'
    files = os.listdir(ref_path)
    fcm = {}
    for file in files:
        if os.path.isfile(os.path.join(ref_path, file)):
            fcm = FCM(ref_path+file, k, alpha).run()
            writeFCM(file, fcm)

def getRefs():
    ref_path = 'refs/'
    files = os.listdir(ref_path)
    return files

def writeFCM(file, fcm):
    with open("fcm/"+file, 'w')as f:
        print(fcm, file=f)

def readFCM(file):
    with open("fcm/"+file, 'r')as f:
        fcm = f.readlines()

def deleteFCMFolders():
    dir = 'fcm/'
    for f in os.listdir(dir):
        print("Deleting fcm files...")
        os.remove(os.path.join(dir,f))

def main(example, target, k, alpha):

    try:
        os.makedirs('fcm_results')
    except:
        pass

    try:
        os.makedirs('alpha')
    except:
        pass

    try:
        os.makedirs('appearances')
    except:
        pass

    aux_ex = example.split("/")
    example_name = aux_ex[len(aux_ex) -1]

    name_file = example_name + "_" + str(k) + "_" + str(alpha) + ".pkl"
    fcms_path = "fcm_results"
    files_fcm_results = listdir(fcms_path)


    if name_file in files_fcm_results: #if the fcm has been calculated previously for the same values, get those values
       print("i've done this before, I'll just read it")

       probabilities = open(fcms_path + "/" + name_file, "rb")
       probs = pickle.load(probabilities)

       alpha_dict = open("alpha" + "/" + name_file, "rb")
       alphabet = pickle.load(alpha_dict)

       appearances_dict = open("appearances" + "/" + name_file, "rb")
       appearances = pickle.load(appearances_dict)

    else: #else, run the fcm and save the values
        print("never seen this ref with this k and alpha")
        # FCM
        fcm = FCM(example, k, alpha)
        probs, prio = fcm.run()

        write_fcm = open(fcms_path + "/" + name_file, "wb")
        pickle.dump(probs, write_fcm)
        write_fcm.close()

        alphabet = fcm.getAlphabet()

        write_alphabet = open("alpha" + "/" + name_file, "wb")
        pickle.dump(alphabet, write_alphabet)
        write_alphabet.close()

        appearances = fcm.getAppearances()

        write_appearances = open("appearances" + "/" + name_file, "wb")
        pickle.dump(appearances, write_appearances)
        write_appearances.close()

    #make comparisons
    lang = Lang(target, k, alpha, probs, alphabet, appearances)
    num_bits = lang.run(example)

    print("Sum of bits: ", num_bits)


if __name__ == "__main__": #python3 src/main.py examples/gatsby.txt 3 0.1

    begin = time.time()

    refs_path = "refs"
    ref_files = listdir(refs_path)

    k = None
    alpha = None
    target = None

    try:
        target = argv[1]
        k = int(argv[2])
        alpha = float(argv[3])

    except Exception as err:
        print("Usage: python3 src/main.py refs/<reference file> <k> <alpha>")
    
    if target and k and alpha:

        #make the process for all files

        for example in ref_files:
            print(example)
            main("refs/" + example, target, k, alpha)
    else:
        print("Usage: python3 src/main.py refs/<reference file> <k> <alpha>")

    end = time.time()

    print(end - begin, len(refs_path))

