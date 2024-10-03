"""
Created on Thu Sept  26 17:29:22 2024

@author: Baptiste Guilleminot

"""

import numpy as np
import random as rd
import matplotlib.pyplot as plt


class case :
    def __init__(self, type = 0, proba = 0) :
        self.type = type
        self.nbVoisins = 0
        self.proba = proba
        self.typeVoisin = 0

    def voisinsProba(self, nbIons, nbCases) :
        self.proba = self.nbVoisins * nbIons / nbCases

class grille :
    def __init__(self, taille, solide, probaGenese) :
        """
        Input :
            un tableau donnant la taille de la grille
            tuple des coordonnées du solide
            type de base pour les autres cases
        """
        self.dim = 2
        self.probaGenese = probaGenese
        self.nbCristaux = 0
        self.sizeX = taille[0]
        self.sizeY = taille[1]
        self.caseATraiter = []
        self.grille = np.array([[case() for i in range(self.sizeY)] for j in range(self.sizeX)])
        for i in solide :
            self.grille[i].type = -2

    def nbVoisins(self, typeVoisins) :
        a = []
        for i in typeVoisins :
            for b in a :
                if b>0 and b != i :
                    return -1
            if i > 0 or i == -2 :
                a.append(i)
        return len(a)

    def Voisins(self) :
        """
        Donne le nombre de voisin à chaque case
        """
        for i in range(self.sizeX) :
            for j in range(self.sizeY) :
                if self.grille[i,j].type == 0 :
                    typeVoisins = []
                    if i > 0 :
                        typeVoisins.append(self.grille[i-1,j].type)
                    if j > 0 :
                        typeVoisins.append(self.grille[i, j-1].type)
                    if i < self.sizeX-1 :
                        typeVoisins.append(self.grille[i+1,j].type)
                    if j < self.sizeY-1 :
                        typeVoisins.append(self.grille[i,j+1].type)
                    self.grille[i,j].nbVoisins = self.nbVoisins(typeVoisins)
                    self.grille[i,j].typeVoisin = max(typeVoisins)
                    self.caseATraiter.append((i,j))

                    if self.grille[i,j].nbVoisins == 0 :
                        #Si la case n'est entouré que d'eau on voit si ca peut etre le debut d'un cristal
                        if i > 1 and j > 1 and i < self.sizeX-2 and j < self.sizeY-2 :
                            a = True
                            for k in range(5) :
                                #Regarde les cases un cran plus loin
                                if a and (self.grille[i-2+k, j-2].type > 0 or self.grille[i-2+k, j+2].type > 0 or self.grille[i-2, j-2+k].type > 0 or self.grille[i+2, j-2+k].type > 0 ):
                                    a = False
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
                nbCasePossible += self.probaGenese
            else :
                nbCasePossible += self.grille[tup].nbVoisins
        probaParCase = nbIons / nbCasePossible

        for tup in self.caseATraiter :
            if self.grille[tup].nbVoisins == -1 :
                self.grille[tup].proba = self.probaGenese * probaParCase
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
                self.grille[tup].nbVoisins = 0
                self.grille[tup].proba = 0
                self.grille[tup].typeVoisin = 0

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
















