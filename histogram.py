import matplotlib.pyplot as plt
import re
import datetime
import argparse
# Добавляем аргумент для командной строки
parser = argparse.ArgumentParser(description='Path to log')
parser.add_argument("-s", "--string", type=str, required=True)

args = parser.parse_args()
#Берем текущее время для того чтоб вставить его в название отчета
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# берем данные из отчета и парсим
inf = open(args.string, mode="r", encoding="latin-1")

finded_first = False
data = ""
for line in inf:
    line = line[:-1]
    if re.search('\w+stimated power', line):
        finded_first = True
        print(line)
        continue
    elif line == '':
        continue
    elif finded_first == True:
        data = line;
        print(line)
        break
        
# в переменные добавляем данные
dig = re.findall(r"[\d']+", data)
dig_int = []

for c in dig:
    dig_int.append(int(c))
    
capacity = dig_int[0]
computed_drain = dig_int[1]
actual_drain = (dig_int[2] + dig_int[3])/2

# создаем гистограмму
s = [computed_drain, actual_drain]
x = range(len(s))
fig = plt.figure()
ax = plt.gca()
# настраиваем цветовую схему
if computed_drain - actual_drain >= (computed_drain*25)/100:
    ax.bar(x, s, align='center', color=['blue','green'])
elif 0 < computed_drain - actual_drain < (computed_drain*25)/100:
    ax.bar(x, s, align='center', color=['blue','yellow'])
elif computed_drain - actual_drain <= 0:
    ax.bar(x, s, align='center', color=['blue','red'])
    
ax.set_xticks(x)
ax.set_xticklabels(('computed drain', 'actual drain',), fontweight='bold')
fig.suptitle('Estimated power use', fontsize=20)
plt.ylabel('mAH', fontsize=14)
plt.text(-0.05, computed_drain+1, int(computed_drain),fontweight='bold')
plt.text(0.95, actual_drain+1, int(actual_drain), fontweight='bold')



plt.show()
plt.draw()
fig.savefig("x5_planner_battery_" + time + ".png", dpi=100)

# python3 path_to_histogram.py -s path_to_bugreport.txt