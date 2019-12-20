import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io


dict = {}

for (x,y,z) in data:
    if x not in dict.keys():
        dict[x] = {}
        dict[x][y] = z
    else:
        dict[x][y] = z


for key in dict.keys():
    
male = [dict[key]['Male'] for key in dict.keys()]
female = [dict[key]['Female'] for key in dict.keys()]
prefnot = [dict[key]['Prefer not to say'] for key in dict.keys()]


p1 = plt.bar(dict.keys(), male)
p2 = plt.bar(dict.keys(), female, bottom = male)
p3 = plt.bar(dict.keys(), prefnot, bottom = male)

plt.legend((p1[0], p2[0], p3[0]), ('Men', 'Women', 'Prefer not to say'))

df = pd.DataFrame({'Age': dict.keys(), 'Male': male, 'Female': female, 'Prefer not to say': prefnot})

df.plot(kind = 'bar', stacked = True)