from operator import itemgetter
from itertools import groupby
from os import listdir
import statistics
from sys import argv
import sys
import time
from lang import Lang


class LocateLang:
    def __init__(self, ref, bits_list, threshold):
        self.ref = ref
        self.bits_list = bits_list
        self.threshold = threshold
        self.listErrorsAllLangs = []

        self.bits_dict = {}


    def run(self):
        self.listErrorsAllLangs += self.detect_changes()
        #print(self.listErrorsAllLangs)
        changes_answer = self.locatelang()

        return changes_answer

    
    # Checks if values are abover or below the threshold, if they are above, they are likely not in accordance with the reference
    def detect_changes(self):
        listErrors = []
        listPositions = []
        count = 0
        for i in self.bits_list:
            if i > self.threshold:
                listErrors.append(i)
                listPositions.append(count)

            count += 1

        #plt.scatter(listPositions, listErrors, 1)
        #plt.show()

        return listPositions


    def locatelang(self):
        aux = []
        count = 0
        answer = []
        outliers = 10

        for i in self.bits_list: #invert to get the positions that match
            if count not in self.listErrorsAllLangs:
                aux.append(count)

            count += 1

        #print(aux)
        for k, g in groupby(enumerate(aux), lambda x: x[0] - x[1]):
            group = list(map(itemgetter(1), g))

            if group[-1] - group[0] > outliers: #tratamento outliers, se forem menos de 10 caracteres não é considerado
                answer.append((group[0], group[-1]))

        '''for i in range(len(answer) - 2, -1, -1):
            if answer[i] == 'a':
                l[i] = l[i] + l.pop(i + 1)
        print(l)'''

        #print("ANS: ",answer)

        for j in range(len(answer) * 10):
            for i in range(len(answer) - 1):
                if len(answer) <= i+1:
                    if i+1 > len(answer):
                        #print("kant")
                        pass

                    if answer[i + 1][0] - answer[i][1] < outliers:
                        #print("here2")
                        aux_answerpop = answer.pop(i + 1)

                        answer[i] = (answer[i][0], aux_answerpop[1])


        #print("answer -", answer)

        #todo - join if the spacing between groups is less than 10 chars

        return answer


def define_Threshold(bits_dict):
    avr_values_list = []

    for ex, bits in bits_dict.items():
        avr_values_list.append(statistics.mean(bits))
        
    threshold = min(avr_values_list) * 1.15
        
    return threshold


if __name__ == "__main__": #python3 src/main.py examples/gatsby.txt 3 0.1
    begin = time.time()
    
    refs_path = "refs"
    ref_files = listdir(refs_path)
    
    k = None
    alpha = None
    target = None

    bits_dict = {}
    try:
        target = argv[1]
        k = int(argv[2])
        alpha = float(argv[3])

    except Exception as err:
        print("Usage: python3 src/locatelang.py target_file/<target file> <k> <alpha>")

    if target and k and alpha:
    
        #make the process for all refs
        for example in ref_files:
            aux_ex = example.split("/")
            example_name = aux_ex[len(aux_ex) -1]

            lang = Lang(example, target, k, alpha)
            num_bits, bits_list = lang.run()

            bits_dict[example_name] = bits_list

        threshold = define_Threshold(bits_dict)
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
                print(" {} starts at char {} and ends at char {}".format(lang, i[0], i[1]))
        
        end = time.time()
        print("\nTime: ",end - begin, len(refs_path))


    else:
        print("Usage: python3 src/locatelang.py target_file/<target file> <k> <alpha>")
        sys.exit()