# TAI_Project2

Determining the “similarity” between  texts

LINK PARA O RELATORIO 2
https://docs.google.com/document/d/1z1AiyWKscZiu1tkcuAjl8rMg1zbRRKAL0oUSMz94aLA/edit?usp=sharing

## How to execute the program

Lang

```bash
$ python3 src/lang.py refs/<reference file> target_file/<target file> <k> <alpha>
```

FindLang

```bash
$ python3 src/findlang.py target_file/<target file> <k> <alpha>
```

LocateLang

```bash
$ python3 src/locatelang.py target_file/<target file> <k> <alpha>
```

Desafio bonus

```bash
$ python3 src/bonus.py -k1 <value of k1> -k2 <value of k2> -a <value of alpha> -rf <path to reference file> -t <path to example file>
```

O valor de k1 é 2 por default, k2 é 4 por default e o alpha tem o valor de 0.1 por default. O texto de referencia e de exemplo são necessários para a execução do programa.
