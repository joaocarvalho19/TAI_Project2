from random import random
import time
import math
from sys import argv
from fcm import FCM
from lang import Lang
import os

def generator(dictionary, prior, lenText):
    # checks if prior is valid

    aux = list(dictionary.keys())

    if prior in dictionary:
        if len(aux[0]) == len(prior):
            print("VALID")
        else:
            print("INVALID")
            return
    else:
        print("INVALID")
        return


    #for the moment I'll consider a 10000 char generation

    generated_text = [None] * lenText
    index = 0

    for i in range(len(generated_text)):

        if i >= len(prior): # Generates text
            
            aux = generated_text[i-len(prior): i] #last k positions

            aux_str = listToString(aux)
            if dictionary.get(aux_str):

                keys_list = list(dictionary.get(aux_str).keys())
                values_list = list(dictionary.get(aux_str).values())

                position = sorting(values_list)

                answerKey = keys_list[position]

                generated_text[i] = answerKey

                #return next_chars_list[position]
                index += 1

        else: #fills list with prior
            generated_text[i] = prior[i]

            index += 1

    result = listToString(generated_text)

    with open('file.txt', 'w') as data: #writes to file.txt the dictionary #12
        data.write(result)


    return result



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

def main(example, k, alpha):

    # FCM
    begin = time.perf_counter()

    fcm = FCM(example, k, alpha)
    #learnLanguage(k, alpha)
    #deleteFCMFolders()

    probs, prio = fcm.run()
    end = time.perf_counter()
    print("Time elapsed: ",end-begin)

    # Lang
    lang = Lang("target_file/test.txt", k, alpha, probs, fcm.getAlphabet(), fcm.getAppearances())
    lang.run()

    # Generator
    #generator(a, prio, 10000)


if __name__ == "__main__":
    example = None
    k = None
    alpha = None

    try:
        example = argv[1]
        k = int(argv[2])
        alpha = float(argv[3])

    except Exception as err:
        print("Usage: python3 src/main.py refs/<reference file> <k> <alpha>")
    
    if example and k and alpha:
        main(example, k, alpha)
    else:
        print("Usage: python3 src/main.py refs/<reference file> <k> <alpha>")
