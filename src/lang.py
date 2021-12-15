import statistics
import time

from fcm import FCM
import math
import matplotlib.pyplot as plt
from operator import itemgetter
from itertools import groupby


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
            bits = 0
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

        start_time = time.time()

        #print(len(bits_list))

        length_big_texts = int(len(bits_list)/50)

        #length_big_texts = int(len(bits_list))


        if len(bits_list) > 10000:
            #TODO - decide on values
            # -> if the length of smoothing is too big, it takes a lot of time
            # and the graph is basically a straight line
            # -> if the interval is too small, it does basically nothing

            bits_list = self.smoothing(bits_list, length_big_texts)
        else:
            bits_list = self.smoothing(bits_list, len(bits_list))

        end_time = time.time()

        #print(end_time - start_time)

        x = [i for i in range(len(bits_list))]

        #TODO - temporary solution to threshold, last values have issues in smoothing

        indices = [0, int(len(bits_list) *0.95)]
        temp_list_to_remove = [bits_list[index] for index in indices]
        #temp_list_to_remove = range(0, int(len(bits_list) *0.99)) #removes the last 1% of values to calculate the threshold
        #print("len temp list - ", len(temp_list_to_remove))
        threshold = ((max(temp_list_to_remove) - min(temp_list_to_remove)) / 2)
        threshold += (min(temp_list_to_remove)) * 0.9

        #threshold = ((max(bits_list) - min(bits_list)) / 2 + min(bits_list) ) * 0.9 #TODO - this 0.9 can be replaced by a value from 0.8 to 1, depends of how much we want to detect

        #threshold = statistics.mean(bits_list) * 1.5
        #print("threshold - ", max(temp_list_to_remove), min(temp_list_to_remove), max(bits_list), min(bits_list), threshold)

        self.listErrorsAllLangs += self.detect_changes(bits_list, threshold)
        #print(bits_list)


        #plt.scatter(x, bits_list, 1)
        #plt.show()
        num_bits = round(final_sum, 2)
        #print("BITS: ", num_bits)
        #print("LEN DICT: ",len(final_dict))

        self.find_positions_correspond_lang(ref_material, bits_list)

        return num_bits

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

    def detect_changes(self, listValues, threshold): #checks if values are abover or below the threshold, if they are above, they are likely not in accordance with the reference

        listErrors = []
        listPositions = []
        count = 0

        for i in listValues:

            if i > threshold:

                listErrors.append(i)
                listPositions.append(count)

            count += 1

        #TODO - tratamento de outliers?

        #plt.scatter(listPositions, listErrors, 1)
        #plt.show()

        return listPositions

    def find_positions_correspond_lang(self, ref_material, bitsList): #todo - associate the language with these values

        aux = []
        count = 0
        answer = []


        for i in bitsList: #invert to get the positions that match
            if count not in self.listErrorsAllLangs:
                aux.append(count)

            count += 1

        for k, g in groupby(enumerate(aux), lambda x: x[0] - x[1]):
            group = list(map(itemgetter(1), g))
            answer.append((group[0], group[-1]))

        print("answer -", answer)
        return answer

