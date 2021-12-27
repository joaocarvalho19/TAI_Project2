from os import listdir
from sys import argv
import sys
import time
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
            l = Lang(lang, self.target, self.k, self.alpha)
            num_bits, bits_list = l.run()
            langs_results[lang] = num_bits

        sorted_results = dict(sorted(langs_results.items(), key=lambda item: item[1]))        
        lang_guess = list(sorted_results.keys())[0]
        return lang_guess


if __name__ == "__main__":
    begin = time.time()
    
    refs_path = "refs"
    ref_files = listdir(refs_path)
    
    k = None
    alpha = None
    target = None

    try:
        target = argv[1]
        k = int(argv[2])
        alpha = float(argv[3])

    except Exception as err:
        print("Usage: python3 src/findlang.py target_file/<target file> <k> <alpha>")

    if target and k and alpha:

        #FindLang
        find = FindLang(ref_files, target, k, alpha)
        lang = find.run()
        lang_name = lang.split(".")[2]
        print("\nLanguage Guess: {}".format(lang_name))
    
    else:
        print("Usage: python3 src/findlang.py target_file/<target file> <k> <alpha>")
        sys.exit(1)