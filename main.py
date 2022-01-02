import csv
from os import close
import numpy as np
import matplotlib.pyplot as plt
import folium, branca
import pandas

def dateFile(filename1):
    with open(filename1, 'r') as f1: 
        r1 = csv.reader(f1)
        l1 = list(r1)

    for i in range(1,len(l1)):
        s = l1[i][1][6:10]+'/'+l1[i][1][3:5]+'/'+l1[i][1][0:2]
        l1[i][1]=s
    return l1

def deleteDoublon1(liste):

    fin = len(liste)-1
    i = 0
    while i<fin:
        if liste[i][3]==liste[i+1][3] and liste[i][2]==liste[i+1][2]:
            liste[i][4]=str(int(liste[i][4])+int(liste[i+1][4]))
            liste.remove(liste[i+1])
            i-=1
            fin -= 1
        i+=1
    return liste

def deleteDoublon2(filename):
    with open(filename, 'r') as f:
        r1 = csv.reader(f,delimiter=',')
        l1 = list(r1)

    fin = len(l1)-1
    i = 0
    while i<fin:
        if l1[i][1]==l1[i+1][1] and l1[i][2]==l1[i+1][2] and l1[i][3]==l1[i+1][3] and l1[i][3]!="DOUBLE SENS" and l1[i][5][:4]==l1[i+1][5][:4] and l1[i][6][:3]==l1[i+1][6][:3]:
            l1.remove(l1[i+1])
            i-=1
            fin -= 1
        i+=1
    return l1
    

def fusion(liste1, liste2):
    for l in liste1:
        cmt = 0
        n = len(l[2])
        while cmt <n:
            if l[2][cmt]=="\"":
                l[2]=l[2][:cmt]+l[2][cmt+1:]
                cmt-=1
                n-=1
            cmt+=1

    for l in liste2:
        cmt = 0
        n = len(l[2])
        while cmt <n:
            if l[2][cmt]=="\"":
                l[2]=l[2][:cmt]+l[2][cmt+1:]
                cmt-=1
                n-=1
            cmt+=1

    i=1
    while i < len(liste1):
        for j in range(len(liste2)):
            if liste1[i][0]==liste2[j][0] and liste1[i][1]==liste2[j][1] and liste1[i][2]==liste2[j][2] :
                liste1[i][3]=liste2[j][3]
                liste1[i][4]=liste2[j][4]
        if liste1[i][4]=="":
            liste1.remove(liste1[i])
            i-=1
        i+=1

    f3 = open('radars-fusion.csv', 'w')
    for valeur in liste1:
        ligne = ";".join(valeur)+'\n'
        f3.write(ligne)

    return liste1

def get_names():
    colonnes=['Département','Date','Route','Direction','Flash','Latitude','Longitude','Vitesse']
    data = pandas.read_csv('radars-fusion.csv', names=colonnes,delimiter=';')
    routes=data.Route.tolist()
    return routes

def get_latitude():
    colonnes=['Département','Date','Route','Direction','Flash','Latitude','Longitude','Vitesse']
    data = pandas.read_csv('radars-fusion.csv', names=colonnes,delimiter=';')
    latitudes=data.Latitude.tolist()
    return latitudes

def get_longitude():
    colonnes=['Département','Date','Route','Direction','Flash','Latitude','Longitude','Vitesse']
    data = pandas.read_csv('radars-fusion.csv', names=colonnes,delimiter=';')
    longitudes=data.Longitude.tolist()
    return longitudes
    
def get_vitesse():
    colonnes=['Département','Date','Route','Direction','Flash','Latitude','Longitude','Vitesse']
    data = pandas.read_csv('radars-fusion.csv', names=colonnes,delimiter=';')
    vitesse=data.Vitesse.tolist()
    return vitesse
    
def get_flash():
    colonnes=['Département','Date','Route','Direction','Flash','Latitude','Longitude','Vitesse']
    data = pandas.read_csv('radars-fusion.csv', names=colonnes,delimiter=';')
    flash=data.Flash.tolist()
    return flash   

def tab_string_to_num(liste) :
    res = []
    for i in range(1,len(liste)):
        res.append(int(list[i]))
    return res

if __name__ == '__main__':
    bilanRadarsDate = dateFile("bilan-radars-fixes-2017.csv")
    bilanRadarsPropre = deleteDoublon1(bilanRadarsDate)
    radarsLocalisationPropre = deleteDoublon2("radars-localisation.csv")
    fusion = fusion(radarsLocalisationPropre,bilanRadarsPropre)
    coords = (46,2)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    map.save(outfile='map.html')
    routes=get_names()
    latitudes=get_latitude()
    longitudes=get_longitude()
    vitesses=get_vitesse()
    flashs = get_flash()
    latitudess = []
    longitudess= []
    vitessess= []
    flashss = []
    for i in range(1,len(latitudes)):
        latitudess.append(float(latitudes[i]))
        longitudess.append(float(longitudes[i]))
        flashss.append(float(flashs[i]))

    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(flashss), vmax=max(flashss))
    map.add_child(cm) # add this colormap on the display

    for lat, lng, size, color in zip(latitudess, longitudess, flashss, flashss):
        folium.CircleMarker(
        location=[lat, lng],
        radius=size/8000,
        color=cm(color),
        fill=True,
        fill_color=cm(color),
        fill_opacity=0.6
        ).add_to(map)
    map.save(outfile='map.html')

    flashs_num = []
    for i in range(1,len(flashs)):
        flashs_num.append(int(flashs[i]))
    b= [0,500,2000,10000,50000,max(flashs_num)]
    n, bins, patches = plt.hist(flashs_num, bins = b,histtype='stepfilled')
    plt.title('Nombre de déclenchements des radars fixes en France')
    plt.xlabel('nombre de déclenchements')
    plt.ylabel('nombre de radars')
    plt.show()