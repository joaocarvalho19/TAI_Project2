from fcm import FCM
import math
import matplotlib.pyplot as plt

class Lang:
    def __init__(self, target, k, alpha, probs, ref_alphabet, ref_appearances):
        self.target = target
        self.k = k
        self.alpha = alpha
        self.probs = probs
        self.ref_alphabet = ref_alphabet
        self.ref_appearances = ref_appearances

    def run(self):
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

        x = [i for i in range(len(bits_list))]
        plt.scatter(x, bits_list)
        plt.show()
        num_bits = round(final_sum, 2)
        #print("BITS: ", num_bits)
        #print("LEN DICT: ",len(final_dict))

        return num_bits