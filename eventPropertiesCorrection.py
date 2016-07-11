'''
This script takes the provided event properties file and puts it into the correct format for use in the LightCurve Code
Mostly, it corrects for 123e+456 and makes it a float value

Written by:  S.R. Moorhead
Last Edit:  2015.06.16 YYYY.MM.DD
'''

def correction(fin, fout):
    with open(fin) as inputFile:
        # create an array holding each line of data
        data = inputFile.read().split("\n")
        outFile = open(fout, "w")
        data.pop(0)
        for line in data:
            lineList = line.split()
            for i, item in enumerate(lineList):
                value_power_pair = item.split('e+')
                lineList[i] = str(float(value_power_pair[0]) * (10 ** float(value_power_pair[1])))
            string_output = str(" ".join(lineList[0:4]))
            outFile.write(string_output + "\n")

        outFile.close()

fileIn = "Q11-Q17eventproperties.dat"
fileOut = "q11_q17_eventproperties_abridged.dat"

test = correction(fileIn, fileOut)