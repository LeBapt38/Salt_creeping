"""
Created on Thu Sept  26 17:29:22 2024

@author: Baptiste Guilleminot

"""

import numpy as np
import random as rd
import matplotlib.pyplot as plt
from math import *

beta = 1/(1.3e-23 * 310)
A = (pi / 2) * beta * 2.3e-10 * 6.4e-19
print(A)

class case :
    def __init__(self, type = -1, proba = 0) :
        self.type = type
        self.nbVoisins = 0
        self.proba = proba
        self.typeVoisin = 0

    def voisinsProba(self, nbIons, nbCases) :
        self.proba = self.nbVoisins * nbIons / nbCases

class grille :
    def __init__(self, taille, eau, A, boostAir, dx) :
        """
        Input :
            un tableau donnant la taille de la grille
            tuple des coordonnées du solide
            type de base pour les autres cases
        """
        self.sizeInterface = 5
        self.dim = 2
        self.A = A
        self.boostAir = boostAir
        self.nbCristaux = 0
        self.sizeX = taille[0]
        self.sizeY = taille[1]
        self.dx = dx
        self.caseATraiter = []
        self.grille = np.array([[case() for i in range(self.sizeY)] for j in range(self.sizeX)])
        for i in eau :
            self.grille[i].type = 0

    def nbVoisins(self, typeVoisins) :
        a = []
        compteurAir = 0
        for i in typeVoisins :
            for b in a :
                if i>0 and b > 0 and b != i :
                    return -1
            if i == -2 or i > 0 :
                a.append(i)
            elif i == -1 :
                compteurAir += self.boostAir
        if len(a) > 0 :
            # les divisions permettent de prendre en compte les différentes situations
            return exp((self.A/self.dx) * (len(a)//4 + len(a)//5 + 1 + compteurAir))
        else :
            return 0

    def Voisins(self) :
        """
        Donne le nombre de voisin à chaque case
        """
        for i in range(self.sizeX) :
            for j in range(self.sizeY) :
                # evite que les nouveaux cristaux se place que dans les angles des anciens
                test = False
                if self.grille[i,j].type == -1 :
                    if i > 0 :
                        if self.grille[i-1, j].type == 0 :
                            test = True
                    if j > 0 :
                        if self.grille[i, j-1].type == 0 :
                            test = True
                    if i < self.sizeX-1 :
                        if self.grille[i+1, j].type == 0 :
                            test = True
                    if j < self.sizeY-1 :
                        if self.grille[i, j+1].type == 0 :
                            test = True
                if self.grille[i,j].type == 0 or test :
                    # Si on est dans l'eau on fait le point de ce qu'il y a autour
                    typeVoisins = []
                    if i > 0 :
                        typeVoisins.append(self.grille[i-1,j].type)
                        if j > 0 :
                            typeVoisins.append(self.grille[i-1,j-1].type)
                        if j < self.sizeY-1 :
                            typeVoisins.append(self.grille[i-1,j+1].type)
                    if j > 0 :
                        typeVoisins.append(self.grille[i, j-1].type)
                    if i < self.sizeX-1 :
                        typeVoisins.append(self.grille[i+1,j].type)
                        if j > 0 :
                            typeVoisins.append(self.grille[i+1,j-1].type)
                        if j < self.sizeY-1 :
                            typeVoisins.append(self.grille[i+1,j+1].type)
                    if j < self.sizeY-1 :
                        typeVoisins.append(self.grille[i,j+1].type)
                    a = self.nbVoisins(typeVoisins)
                    if a > 0 :
                        self.grille[i,j].nbVoisins = a
                        self.grille[i,j].typeVoisin = max(typeVoisins)
                        self.caseATraiter.append((i,j))

                    elif a == 0 :
                        #Si la case n'est entouré que d'eau on voit si ca peut etre le debut d'un cristal
                        if i > 1 and j > 1 and i < self.sizeX-2 and j < self.sizeY-2 :
                            a = True
                            for k in range(5) :
                                #Regarde les cases un cran plus loin
                                if a and (self.grille[i-2+k, j-2].type > 0 or self.grille[i-2+k, j+2].type > 0 or self.grille[i-2, j-2+k].type > 0 or self.grille[i+2, j-2+k].type > 0):
                                    a = False
                            if self.grille[i+1, j+1].type > 0 or self.grille[i-1, j+1].type > 0 or self.grille[i+1, j-1].type > 0 or self.grille[i-1, j-1].type > 0 :
                                #print(a)
                                a = True
                            if not a :
                                self.grille[i,j].nbVoisins = -1
                                self.caseATraiter.append((i,j))


    def proba(self, nbIons) :
        """
        Calcul la probabilité que chaque case puisse avoir un nouvel ion
        """
        nbCasePossible = 0
        # Estime le nombre de case avec leur multiplicité
        for tup in self.caseATraiter :
            if self.grille[tup].nbVoisins == -1 :
                nbCasePossible += 1
            else :
                nbCasePossible += self.grille[tup].nbVoisins
        probaParCase = nbIons / nbCasePossible

        for tup in self.caseATraiter :
            if self.grille[tup].nbVoisins == -1 :
                self.grille[tup].proba = probaParCase
            else :
                self.grille[tup].proba = self.grille[tup].nbVoisins * probaParCase


    def nvIons(self) :
        for tup in self.caseATraiter :
            a = rd.random()
            if self.grille[tup].proba > a :
                if self.grille[tup].typeVoisin > 0 :
                    self.grille[tup].type = self.grille[tup].typeVoisin
                else :
                    self.nbCristaux += 1
                    self.grille[tup].type = self.nbCristaux
                (i,j) = tup
                (a,b) = self.grille.shape
                nbAirEau = 0
                # S'assure qu'il y a de l'eau tout autour de la nouvelle case
                if j+1 < b :
                    if self.grille[i,j+1].type == -1 :
                        self.grille[i,j+1].type = 0
                        nbAirEau += 1
                if i+1 < a and j+1 < b :
                    if self.grille[i+1,j+1].type == -1 :
                        self.grille[i+1,j+1].type = 0
                        nbAirEau += 1
                if i > 0 and j+1 < b :
                    if self.grille[i-1,j+1].type == -1 :
                        self.grille[i-1,j+1].type = 0
                        nbAirEau += 1
                if i+1 < a :
                    if self.grille[i+1,j].type == -1 :
                        self.grille[i+1,j].type = 0
                        nbAirEau += 1
                if i > 0 :
                    if self.grille[i-1,j].type == -1 :
                        self.grille[i-1,j].type = 0
                        nbAirEau += 1
                if j > 0 :
                    if self.grille[i,j-1].type == -1 :
                        self.grille[i,j-1].type = 0
                        nbAirEau += 1
                if i < a-1 and j > 0 :
                    if self.grille[i+1,j-1].type == -1 :
                        self.grille[i+1,j-1].type = 0
                        nbAirEau += 1
                if i>0 and j>0 :
                    if self.grille[i-1,j-1].type == -1 :
                        self.grille[i-1,j-1].type = 0
                        nbAirEau += 1
                if nbAirEau > 0 :
                    self.sizeInterface += nbAirEau - 1
            self.grille[tup].nbVoisins = 0
            self.grille[tup].proba = 0
            self.grille[tup].typeVoisin = 0
        self.caseATraiter = []



    def timeStep(self, nbStep, nbIons) :
        for i in range(nbStep) :
            self.Voisins()
            self.proba(nbIons)
            self.nvIons()

    def affichage(self) :
        grilleAffichage = np.array([[0 for i in range(self.sizeY)] for j in range(self.sizeX)])
        for i in range(self.sizeX) :
            for j in range(self.sizeY) :
                if self.grille[i,j].type == -2 :
                    grilleAffichage[i,j] = -2
                elif self.grille[i,j].type == -1 :
                    grilleAffichage[i,j] = -1
                elif self.grille[i,j].type == 0:
                    grilleAffichage[i,j] = 0
                else :
                    grilleAffichage[i,j] = 1

        plt.imshow(grilleAffichage, cmap='viridis')  # 'cmap' est la palette de couleurs
        plt.title('Cristalisation')  # Ajouter un titre
        plt.show()
















