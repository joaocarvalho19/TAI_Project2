from os import listdir
from sys import argv
import sys
import time
from fcm import FCM
import math
import matplotlib.pyplot as plt

from get_ref_info import GetRefInfo


class Lang:
    def __init__(self, ref, target, k, alpha, isLocate):
        self.ref = ref
        self.target = target
        self.k = k
        self.alpha = alpha
        self.probs = {}
        self.ref_alphabet = set()
        self.ref_appearances = {}
        self.isLocate = isLocate

        self.listErrorsAllLangs = []
        #Check if ref fcm is on disk
        self.getFCM()

    def run(self):
        fileContent = FCM.readFile(self, self.target)
        final_dict = {}
        final_sum = 0
        bits_list = []
        temp_list = []
        for i in range(self.k, len(fileContent[self.k:])+1):
            c = fileContent[i-self.k:i]
            e = fileContent[i]

            if c in self.probs.keys():
                if e in self.probs[c]:

                    if c not in final_dict:
                        final_dict[c] = {}

                    final_dict[c][e] = self.probs[c][e]
                    bits = -math.log2(self.probs[c][e])
                    final_sum += bits

                # Symbol not in reference text
                else:
                    p =  self.alpha / (sum(self.ref_appearances[c].values()) + (self.alpha*len(self.ref_alphabet)))
                    bits = -math.log2(p)
                    final_sum += bits
                
            else:
                p =  self.alpha / (self.alpha*len(self.ref_alphabet))
                bits = -math.log2(p)
                final_sum += bits
            
            temp_list.append(bits)

            # Avg of 10 symbols - to smoth
            if len(temp_list) == 5:
                bits_list.append(sum(temp_list)/len(temp_list))
                temp_list=[]


        length_big_texts = int(len(bits_list)/50)
        #length_big_texts = 1500

        if self.isLocate:
            if len(bits_list) > length_big_texts:
                #TODO - decide on values
                # -> if the length of smoothing is too big, it takes a lot of time
                # and the graph is basically a straight line
                # -> if the interval is too small, it does basically nothing

                bits_list = self.smoothing(bits_list, length_big_texts)
            else:
                bits_list = self.smoothing(bits_list, len(bits_list))


            x = [i for i in range(len(bits_list))]


        #plt.scatter(x, bits_list, 1)
        #plt.show()

        num_bits = round(final_sum, 2)


        #print("min - ", min(bits_list), "MAX - ", max(bits_list), "avr - ", statistics.mean(bits_list))
        return num_bits, bits_list
    
    
    # Check if ref fcm is on disk
    def getFCM(self):
        get_ref_info = GetRefInfo(self.ref, self.k, self.alpha)
        [self.probs, self.ref_alphabet, self.ref_appearances] = get_ref_info.run()


    def smoothing(self, listValues, smoothingInterval): #weird values at the end of the text which affect the threshold choice
        count = 0

        for i in range(smoothingInterval, len(listValues[smoothingInterval:]) + smoothingInterval *2):

            subList = listValues[count: count + smoothingInterval]

            soma = 0

            for j in subList:
                soma += j

            soma = round(soma / len(subList), 2)

            for j in range(0, smoothingInterval + 1):
                listValues[count] = soma

            count += 1

        return listValues

    
    #--------bonus---------


    def runBonus(self):
        fileContent = FCM.readFile(self, self.target)
        final_dict = {}
        final_sum = 0
        bits_list = []
        temp_list = []
        for i in range(self.k, len(fileContent[self.k:]) + 1):
            c = fileContent[i - self.k:i]
            e = fileContent[i]

            if c in self.probs.keys():
                if e in self.probs[c]:

                    if c not in final_dict:
                        final_dict[c] = {}

                    final_dict[c][e] = self.probs[c][e]
                    bits = -math.log2(self.probs[c][e])
                    final_sum += bits

                # Symbol not in reference text
                else:
                    p = self.alpha / (sum(self.ref_appearances[c].values()) + (self.alpha * len(self.ref_alphabet)))
                    bits = -math.log2(p)
                    final_sum += bits

            else:
                p = self.alpha / (self.alpha * len(self.ref_alphabet))
                bits = -math.log2(p)
                final_sum += bits

            temp_list.append(bits)
            if len(temp_list) == 5:
                bits_list.append(sum(temp_list) / len(temp_list))
                temp_list = []

        length_big_texts = int(len(bits_list) / 50)
        bits_list1 = self.smoothing(bits_list, length_big_texts)


        return bits_list1



    def hybrid(self, list1, list2): #returns a list of hybrid entropies with graph

        count = 0
        listBest = []

        for i in list2:

            if i > list1[count]:

                listBest.append((1, list1[count], count))

            else:
                listBest.append((2, i, count))

            count += 1

            best1 = []
            best2 = []

        x1 = []
        x2 = []

        soma_bits = 0

        for j in listBest:

            soma_bits += j[1]

            if j[0] == 1:
                best1.append(j[1])
                x1.append(j[2])
            else:
                best2.append(j[1])
                x2.append(j[2])

        print(soma_bits)

        plt.scatter(x1, best1, 1, c= 'coral')
        plt.scatter(x2, best2, 1)
        plt.show()

        return listBest

if __name__ == "__main__":
    begin = time.time()
    
    k = None
    alpha = None
    ref = None
    target = None

    try:
        ref = argv[1]
        target = argv[2]
        k = int(argv[3])
        alpha = float(argv[4])

    except Exception as err:
        print("Usage: python3 src/lang.py refs/<reference file> target_file/<target file> <k> <alpha>")

    if target and ref and k and alpha:

        #Lang
        aux_ex = ref.split("/")
        ref_name = aux_ex[len(aux_ex) -1]
        l = Lang(ref_name, target, k, alpha)
        num_bits, bits_list = l.run()
        print("Estimated number of bits: {}".format(num_bits))
    
    else:
        print("Usage: python3 src/lang.py refs/<reference file> target_file/<target file> <k> <alpha>")
        sys.exit(1)