from tkinter import *
from math import sqrt
from random import randint, uniform
from time import sleep


g1 = [(5, 3), (5, 6), (5, 0), (4, 3), (0, 3), (2, 4), (5, 5), (6, 2), (2, 2), (4, 4)]
g2 = [(9, 10), (10, 10), (11, 11), (11, 10), (8, 12), (13, 10), (10, 9), (8, 8), (12, 10), (9, 9)]
g3 = [(10, 1), (9, 3), (8, 4), (7, 2), (11, 1), (9, 2), (12, 3), (10, 1), (9, 4), (10, 3)]
g4 = [(4, 17), (5, 14), (4, 15), (5, 13), (4, 13), (7, 13), (6, 12), (6, 14), (4, 12), (4, 17)]

g = []
for g_i in [g1, g2, g3, g4]:
    for p in g_i :
        g.append(p)

def maxCord_liste(l):
    tmpY = 0
    tmpX = 0
    for i in l:
        if tmpY<i[1]:
            tmpY = i[1]
        if tmpX<i[0]:
            tmpX = i[0]
    return tmpX, tmpY

def minCord_liste(l):
    tmpY = 100000
    tmpX = 10000
    for i in l:
        if tmpY>i[1]:
            tmpY = i[1]
        if tmpX>i[0]:
            tmpX = i[0]
    return tmpX, tmpY

"""def init_centrides(k, g): #renvoir liste de centroide 
    l = list()
    maxX, maxY = maxCord_liste(g)
    minX, minY = minCord_liste(g)

    topDroite = ( minX-((maxX-minX)/4), maxY-((maxY-minY)/4) )
    topGauche = ( minX+((maxX-minX)/4), maxY-((maxY-minY)/4) )
    basDroite = ( minX-((maxX-minX)/4), maxY+((maxY-minY)/4) )
    basGauche = ( minX+((maxX-minX)/4), maxY+((maxY-minY)/4) )
    
    for i in range(k):
        l.append((uniform(basGauche[0], basDroite[0] ),uniform(basDroite[1],topDroite[1])))
    return l """

def init_centrides(k, g): #renvoir liste de centroide 
    l = list()    
    for i in range(k):
        l.append((randint(0,20),randint(0,20)))
    return l 

def distance(p1,p2):
    """
    >>> distance((5,5), (5,10))
    5.0
    
    >>> distance((0,10), (10,10))
    10.0
    """
    return sqrt(((p2[0]-p1[0])**(2))+((p2[1]-p1[1])**(2)))

def plus_proche_centroides(p, l): #point//liste de centroide
    """
    >>> plus_proche_centroides((0,0), [(1,0),(2,0),(3,0),(4,0)])
    0
    >>> plus_proche_centroides((0,0), [(2,0),(1,0),(3,0),(4,0)])
    1
    >>> plus_proche_centroides((0,0), [(3,0),(2,0),(1,0),(4,0)])
    2
    >>> plus_proche_centroides((0,0), [(4,0),(2,0),(3,0),(1,0)])
    3
    """    
    tmp = 300
    for i in l:
        if tmp>distance(p,i):
            tmp = distance(p,i)
            n = l.index(i)
    return n

def assignation(g, l): #Compare chaque point à chaque centroide
    """
    >>
    """
    c = []
    for i in range(len(l)):
        c.append([])

    for i in g:
        c[plus_proche_centroides(i, l)].append(i) # liste de liste
    return c

def barycentre(l): #baricentre d'une liste de point 
    summ_abs = 0
    summ_ord = 0
    yolo = len(l)
    for i in l:
        summ_abs += i[0]
        summ_ord += i[1]
    return (summ_abs//yolo, summ_ord//yolo)

def calibrage(g):
    b = list()
    for i in g:
        b.append(barycentre(i))
    return b

def k_means(g,k):
    new_centroide = []
    point_id = list()
    centroide_vide = True
    centroide = init_centrides(k, g)
    create_point(g)
    groupe_point_proche = assignation(g, centroide) # liste de liste
    while True:
        while centroide_vide:
            centroide_vide = False
            for i in range(k):
                if groupe_point_proche[i] == []:
                    centroide[i] = (randint(0,20),randint(0,20))
                    centroide_vide = True
                    groupe_point_proche = assignation(g, centroide) # liste de liste
        
        point_id = update_point(centroide, point_id)
        centroide = []
        for i in groupe_point_proche:
            centroide.append(barycentre(i))
        new_points = assignation(g, centroide)
        point_id = update_point(centroide, point_id)
        
        if groupe_point_proche == new_points:
            print(groupe_point_proche)
            print(new_points)
            break
        else:
            groupe_point_proche = new_points
            new_points = []
    return new_points

def lol(p, pp, partition_initiale):
    """
    >>> lol(1, 2, [[1,3,6],[2,8,9]])
    False

    >>> lol(1,2,[[1,2,3,6], [8,5,9,7]])
    True
    """
    for i in range(len(partition_initiale)):
        for j in range(len(partition_initiale[i])):
            if p in partition_initiale[i]:
                if pp in partition_initiale[i]:
                    return True
    else:
        return False
    


def score_partition(partition_initiale, partition_kmeans):
    """
    >>> score_partition([[(5, 3), (5, 6), (5, 0), (4, 3), (0, 3), (2, 4), (5, 5), (6, 2), (2, 2), (4, 4)],[(9, 10), (10, 10), (11, 11), (11, 10), (8, 12), (13, 10), (10, 9), (8, 8), (12, 10), (9, 9)],[(10, 1), (9, 3), (8, 4), (7, 2), (11, 1), (9, 2), (12, 3), (10, 1), (9, 4), (10, 3)],[(4, 17), (5, 14), (4, 15), (5, 13), (4, 13), (7, 13), (6, 12), (6, 14), (4, 12), (4, 17)]],[[(5, 3), (5, 6), (5, 0), (4, 3), (0, 3), (2, 4), (5, 5), (6, 2), (2, 2), (4, 4)],[(9, 10), (10, 10), (11, 11), (11, 10), (8, 12), (13, 10), (10, 9), (8, 8), (12, 10), (9, 9)],[(10, 1), (9, 3), (8, 4), (7, 2), (11, 1), (9, 2), (12, 3), (10, 1), (9, 4), (10, 3)],[(4, 17), (5, 14), (4, 15), (5, 13), (4, 13), (7, 13), (6, 12), (6, 14), (4, 12), (4, 17)]])
    6
    """
    list_a_test = list()
    score = 0
    for i in range(len(partition_kmeans)):
        list_a_test = []
        for a in range(len(partition_kmeans[i])):
            list_a_test.append(a)

        for j in range(len(partition_kmeans[i])):
            list_a_test.remove(j)
            for k in list_a_test:
                if lol(partition_kmeans[i][j], partition_kmeans[i][k], partition_initiale):
                    score+=1
    return score

def update_point(c, point_id):
    for i in point_id:
        canvas.delete(i)
    
    point_id = []
    for i in c:
        x = i[0]*30
        y = i[1]*30
        point_id.append(canvas.create_oval(x,y,x+10,y+10, fill="red"))
    
    Fenetre.update()
    sleep(0.25)
    return point_id

def create_point(g):
    n=0
    point_id = list()
    for i in g:
        x = i[0]*30
        y = i[1]*30
        canvas.create_oval(x,y,x+5,y+5)
    Fenetre.update()
    sleep(0.25)



Fenetre = Tk()
Fenetre.title("Fenetre de simulation")
Fenetre.geometry('800x800')
canvas = Canvas(Fenetre, width = 650, height = 650, background ='white')
canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)
print(score_partition([g1,g2,g3,g4], k_means(g,4)))
#Fenetre.mainloop()
