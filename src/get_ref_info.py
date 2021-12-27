import os
import pickle

from fcm import FCM

class GetRefInfo:
    def __init__(self, ref, k, alpha):
        self.ref = ref
        self.k = k
        self.alpha = alpha

    def run(self):
        try:
            os.makedirs('fcm_results')
        except:
            pass

        try:
            os.makedirs('alpha')
        except:
            pass

        try:
            os.makedirs('appearances')
        except:
            pass

        aux_ex = self.ref.split("/")
        example_name = aux_ex[len(aux_ex) -1]

        name_file = example_name + "_" + str(self.k) + "_" + str(self.alpha) + ".pkl"
        fcms_path = "fcm_results"
        files_fcm_results = os.listdir(fcms_path)


        if name_file in files_fcm_results: #if the fcm has been calculated previously for the same values, get those values
            print("I've done this before, I'll just read it - Ref: {}".format(example_name))

            probabilities = open(fcms_path + "/" + name_file, "rb")
            probs = pickle.load(probabilities)

            alpha_dict = open("alpha" + "/" + name_file, "rb")
            alphabet = pickle.load(alpha_dict)

            appearances_dict = open("appearances" + "/" + name_file, "rb")
            appearances = pickle.load(appearances_dict)

        else: #else, run the fcm and save the values
            print("Never seen this ref with this k and alpha - Ref: {}".format(example_name))
            # FCM
            print("Learning {} ...".format(example_name))
            fcm = FCM("refs/"+self.ref, self.k, self.alpha)
            probs, prio = fcm.run()

            write_fcm = open(fcms_path + "/" + name_file, "wb")
            pickle.dump(probs, write_fcm)
            write_fcm.close()

            alphabet = fcm.getAlphabet()

            write_alphabet = open("alpha" + "/" + name_file, "wb")
            pickle.dump(alphabet, write_alphabet)
            write_alphabet.close()

            appearances = fcm.getAppearances()

            write_appearances = open("appearances" + "/" + name_file, "wb")
            pickle.dump(appearances, write_appearances)
            write_appearances.close()
    
        return [probs, alphabet, appearances]