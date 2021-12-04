from fcm import FCM
import math


class Lang:
    def __init__(self, target, k, alpha, probs):
        self.target = target
        self.k = k
        self.alpha = alpha
        self.probs = probs

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

        print("BITS?: ",round(final_sum, 2))
        print("LEN DICT: ",len(final_dict))