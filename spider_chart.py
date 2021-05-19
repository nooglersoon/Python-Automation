# Program: Spider Chart Auto
# Created by: Fauzi Achmad B D
# Radar chart function by matplotlib

# Libraries yang digunakan
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

#fungsi membuat chart
def createRadar(player, data):
    Attributes = ["Defending","Dribbling","Pace","Passing","Physical","Shooting"]
    
    data += data [:1]
    
    angles = [n / 6 * 2 * pi for n in range(6)]
    angles += angles [:1]
    
    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1],Attributes)
    ax.plot(angles,data)
    ax.fill(angles, data, 'blue', alpha=0.1)

    ax.set_title(player)
    plt.show()

#Data yang digunakan

data = {'Nama': ['Aji','Fauzi','Achmad','BD'], 'Var 1':[30, 30, 30, 30], 'var 2':[40, 40, 40, 40],'Var 3':[10, 10, 10, 10], 'var 4':[60, 20, 10, 50],'Var 5':[10, 20, 10, 40], 'var 6':[40, 20, 10, 40] }

# warga = pd.read_csv(namafile) --> to dataframe
warga = pd.DataFrame.from_dict(data)
    
for x in warga.index.values.tolist():
    name = warga.loc[x,'Nama']
    value=warga.iloc[x,1:].tolist()
    createRadar(name,value)
    filename=str(name)+'.png'
    plt.show()
    plt.draw()
    plt.savefig(filename)
    plt.close()
