import pickle
import statistics
from os import listdir
from random import random
import sys
import time
import math
from sys import argv
from get_ref_info import GetRefInfo
from fcm import FCM
from findlang import FindLang
from locatelang import LocateLang
from lang import Lang
import os

bits_dict = {}

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

def main(example, target, k, alpha):

    #make comparisons
    aux_ex = example.split("/")
    example_name = aux_ex[len(aux_ex) -1]
    lang = Lang(example, target, k, alpha)
    num_bits, bits_list = lang.run()
    print(" Sum of bits: ", num_bits)
    
    bits_dict[example_name] = bits_list


def define_Threshold():
    #print(bits_dict)

    avr_values_list = []

    for ex, bits in bits_dict.items():
        avr_values_list.append(statistics.mean(bits))

    #print(avr_values_list)
    
    threshold = min(avr_values_list) * 1.15
    #1.1 to pt_en
    #print(threshold)
    
    return threshold


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
            

        threshold = define_Threshold()
        print("Threshold: ",threshold)

        # Locate Text Langs
        locate_langs_list = {}
        for ex, bits in bits_dict.items():
            locate = LocateLang(ex, bits, threshold)
            changes_answer = locate.run()

            # Langs that are supposed to be in the text
            if changes_answer:
                locate_langs_list[ex] = changes_answer

        print("Langs in the target text:")
        for lang, l in locate_langs_list.items():
            lang = lang.split(".")[2]
            for i in l:
                print(" {} starts at char {} and ends at char {}".format(lang, i[0]*5, i[1]*5))
        
        end = time.time()
        print("\nTime: ",end - begin, len(refs_path))


    else:
        print("Usage: python3 src/main.py refs/<reference file> <k> <alpha>")
        sys.exit()