from fcm import FCM
import math


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
        for i in range(self.k, len(fileContent[self.k:])+1):
            c = fileContent[i-self.k:i]
            e = fileContent[i]

            if c in self.probs.keys():
                if e in self.probs[c]:

                    if c not in final_dict:
                        final_dict[c] = {}
                        
                    final_dict[c][e] = self.probs[c][e]
                    final_sum -= math.log2(self.probs[c][e])

                # Symbol not in reference text
                else:
                    p =  self.alpha / (sum(self.ref_appearances[c].values()) + (self.alpha*len(self.ref_alphabet)))
                    final_sum -= math.log2(p)
                
            else:
                p =  self.alpha / (self.alpha*len(self.ref_alphabet))
                final_sum -= math.log2(p)

        num_bits = round(final_sum, 2)
        #print("BITS: ", num_bits)
        #print("LEN DICT: ",len(final_dict))

        return num_bits