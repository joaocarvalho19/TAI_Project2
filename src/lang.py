import statistics
import time

from fcm import FCM
import math
import matplotlib.pyplot as plt
from operator import itemgetter
from itertools import groupby
import statistics


class Lang:
    def __init__(self, target, k, alpha, probs, ref_alphabet, ref_appearances):
        self.target = target
        self.k = k
        self.alpha = alpha
        self.probs = probs
        self.ref_alphabet = ref_alphabet
        self.ref_appearances = ref_appearances

        self.listErrorsAllLangs = []

    def run(self, ref_material):
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
            if len(temp_list) == 5:
                bits_list.append(sum(temp_list)/len(temp_list))
                temp_list=[]


        length_big_texts = int(len(bits_list)/50)
        #length_big_texts = 1500


        if len(bits_list) > length_big_texts:
            #TODO - decide on values
            # -> if the length of smoothing is too big, it takes a lot of time
            # and the graph is basically a straight line
            # -> if the interval is too small, it does basically nothing

            bits_list = self.smoothing(bits_list, length_big_texts)
        else:
            bits_list = self.smoothing(bits_list, len(bits_list))


        x = [i for i in range(len(bits_list))]

        #TODO - temporary solution to threshold because last values have issues in smoothing

        #indices = [0, int(len(bits_list) * 0.95)]
        #temp_list_to_remove = [bits_list[index] for index in indices]

        #threshold = ((max(temp_list_to_remove) - min(temp_list_to_remove)) / 2)
        #threshold += (min(temp_list_to_remove)) * 0.95



        #plt.scatter(x, bits_list, 1)
        #plt.show()

        num_bits = round(final_sum, 2)

        #self.listErrorsAllLangs += self.detect_changes(bits_list, threshold)
        #answer = self.locatelang(bits_list)

        #lang_answer = [ref_material, answer]

        #print(lang_answer)

        print("min - ", min(bits_list), "MAX - ", max(bits_list), "avr - ", statistics.mean(bits_list))
        return num_bits, bits_list


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

    def calculate_langs(self,ref_material, bits_list, threshold):

        self.listErrorsAllLangs += self.detect_changes(bits_list, threshold)
        answer = self.locatelang(bits_list)

        lang_answer = [ref_material, answer]

        print("\n\n",lang_answer)


    def detect_changes(self, listValues, threshold): #checks if values are abover or below the threshold, if they are above, they are likely not in accordance with the reference

        listErrors = []
        listPositions = []
        count = 0

        for i in listValues:

            if i > threshold:

                listErrors.append(i)
                listPositions.append(count)

            count += 1

        #plt.scatter(listPositions, listErrors, 1)
        #plt.show()

        return listPositions


    def locatelang(self, bitsList):
        aux = []
        count = 0
        answer = []

        for i in bitsList: #invert to get the positions that match
            if count not in self.listErrorsAllLangs:
                aux.append(count)

            count += 1

        for k, g in groupby(enumerate(aux), lambda x: x[0] - x[1]):
            group = list(map(itemgetter(1), g))

            if group[-1] - group[0] > 10: #tratamento outliers, se forem menos de 10 caracteres não é considerado
                answer.append((group[0], group[-1]))

        #print("answer -", answer)
        return answer


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
