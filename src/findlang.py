
from fcm import FCM

from lang import Lang

class FindLang:
    def __init__(self, lang_list, target, k, alpha):
        self.lang_list = lang_list
        self.target = target
        self.k = k
        self.alpha = alpha

    def run(self):
        langs_results = {}
        for lang in self.lang_list:
            print("Learning {} ...".format(lang))
            fcm = FCM("refs/"+lang, self.k, self.alpha)
            probs, prio =fcm.run()
            l = Lang(self.target, self.k, self.alpha, probs, fcm.getAlphabet(), fcm.getAppearances())
            num_bits = l.run()
            langs_results[lang] = num_bits

        sorted_results = dict(sorted(langs_results.items(), key=lambda item: item[1]))
        print(sorted_results)
        
        lang_guess = list(sorted_results.keys())[0]
        return lang_guess