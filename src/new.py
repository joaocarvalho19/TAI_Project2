import os

from fcm import FCM

sum = 0


def calculate_char_by_char(example, k, alpha):
    #ref_list = os.listdir("../refs")
    ref_list = ["../refs/eng_GB.latn.English.EP7.utf8"]
    for i in ref_list:



        file_path = "../refs/" + i

        print(i)

        fcm = FCM(file_path, k, alpha) #calculate the fcm for the ref
        fcm.run()

        print(fcm.n_appearances)

        example_text = open(example, "r", encoding="UTF-8")
        print(len(fcm.n_appearances))

        example_text = example_text.read()

        print(type(example_text))

        list_values = [0] * (len(example_text) - k)
        count = 0
        wtv_Value = 2
        outercounter = 0
        soma = 0


        for j in range(k, len(example_text[k:])+1):

            c = example_text[count : count + k]
            e = example_text[count + k + 1]

            print(c)


            if c not in fcm.n_appearances: #what should we consider when chars don't appear on the dictionary? 0?
                list_values[count] = 0

            elif e not in fcm.n_appearances [c]:

                list_values[count] = 0


            else: #it exists and next char also exists
                #calculate

                value = fcm.n_appearances [c] [e]

                #print(value)

                list_values[count] = value


            count +=1
        print(list_values)
        smooth(list_values, 3)
        outercounter += 1

def smooth(listValues, interval): #not smoothing last values

    count = 0


    for i in range(interval, len(listValues[interval:])+1):

        subList = listValues[count : count + interval]

        soma = 0

        for j in subList:

            soma += j

        soma = round(soma / len(subList), )

        for j in range(0, interval+1):
            listValues[count] = soma




        count += 1

    print(listValues)




if __name__ == "__main__":

    calculate_char_by_char("../examples/dorian.txt", 2, 0.1)