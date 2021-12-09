def smoothing(listValues, smoothingInterval):
    count = 0

    for i in range(smoothingInterval, len(listValues[smoothingInterval:]) + smoothingInterval * 2):

        subList = listValues[count: count + smoothingInterval]

        soma = 0

        for j in subList:
            soma += j

        soma = round(soma / len(subList), 2)

        for j in range(0, smoothingInterval + 1):
            listValues[count] = soma

        count += 1