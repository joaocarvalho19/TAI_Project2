import math

class FCM:
    def __init__(self, text, k, alpha):
        self.text = text
        self.k = k
        self.alpha = alpha
        self.alphabet = set()
        self.n_appearances = {}


    def getAlphabet(self):
        return self.alphabet

    def getAppearances(self):
        return self.n_appearances
        
    def readFile(self, text):
        #reads a .txt file
        file = open(text, "r", encoding="UTF-8")
        fileContent = file.read()
        #print(text, " - LEN: ", len(fileContent))
        return fileContent

    def createAlphabet(self, fileContent):
        #creates a set with all the possible characters
        #each letter only appears once and it's unordered
        prio=""
        alphabet = set()
        for i in fileContent:
            alphabet.add(i)
            if len(prio) < self.k:
                prio += i

        self.alphabet = list(alphabet)
        return prio
    
    def calcEntropy(self):
        H_dict = {}
        Probs = {}
        for c in self.n_appearances.keys():
            Hc = 0
            Probs[c] = {}        
            for s in self.n_appearances[c].keys():
                prob = self.calcProb(c, s)
                Probs[c][s] = prob

                Hc += -prob*math.log2(prob)
                
            H_dict[c] = round(Hc, 2)

        return H_dict, Probs
    
    def calcProb(self, c, e):
        prob = (self.n_appearances[c][e]+self.alpha) / (sum(self.n_appearances[c].values()) + (self.alpha*len(self.n_appearances[c])))
        return prob


    def run(self):
        fileContent = self.readFile(self.text)
        prio = list(self.createAlphabet(fileContent))

        #Make table(Dictionary)
        for i in range(self.k, len(fileContent[self.k:])+1):
            c = fileContent[i-self.k:i]
            e = fileContent[i]

            #Update table
            if c not in self.n_appearances:
                self.n_appearances[c] = {}
                
            if e not in self.n_appearances[c]:
                self.n_appearances[c][e] = 1

            else:
                self.n_appearances[c][e] += 1

        #Entropy of each context
        H_dict, Probs = self.calcEntropy()          #key - context; value - H

        #AVG Entropy
        entropy_sum = 0
        total_sum = sum(sum(i.values()) for i in self.n_appearances.values())
        for c in H_dict:
            Pc = sum(self.n_appearances[c].values()) / total_sum
            entropy_sum += H_dict[c] * Pc

        #print("Value of entropy ", round(entropy_sum, 2), " bits/symbol")

        return Probs, prio
