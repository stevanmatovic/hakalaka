f1 = open('soc.txt','r')
#iteration soc penalty solar load
import matplotlib.pyplot as plt
listSoc = []
listPenalty = []
listSolar = []
for i in f1:
    list = i.split(' ')
    if list[0] == "iteration":
        continue
    listPenalty.append(float(list[2]))
    listSoc.append(float(list[1]))
    listSolar.append(float(list[3]))
plt.plot(listSoc)
plt.plot(listPenalty)
plt.plot([x/5 for x in listSolar])
plt.show()
f1.close()