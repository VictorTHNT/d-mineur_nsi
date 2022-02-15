from random import randint
from tkinter import Grid
from turtle import Turtle


def generate_grid():
    """Generation de la gille 
    type:
     0: vide
    -1: mine
    -2: drapeau
    """

    grille = {}
    for colonne in range(1, 11):
        for ligne in range(1, 11):
            grille[(colonne, ligne)] = ["0", "0", False]  # [type, nombre_de_mine_autour, decouverte]
    return grille



def generate_mines():
    """creation de la position de 20 mines aleatoires"""
    liste_position = [] # creation de la liste qui va contenir les coordonées aleatoire des bombes
    mine = 0
    while mine < 20: 
        x=randint(1, 10) #position aleatoire de x entre 1 et 10 
        y=randint(1, 10) #position aleatoire de y entre 1 et 10
        if (x,y) not in liste_position: #si ce x et y n'existe pas alors on introduit de x y dans la liste_position si x y n y est pas deja
            liste_position.append((x,y)) #introduction de x et y dans la liste_position
            mine+=1
    return liste_position 



def add_mines_to_grid(liste_position, grille):  
    for i in range(20): 
        if liste_position[i] in grille: 
            [x,y] = liste_position[i] # recupere les coordonées en position i  
            grille[(x,y)] = ["-1", "0", False] # positionnement des bombes dans le dico a partir de la liste de coordonées aleatoire
    return grille


def calculate_near_sum(coo, grille):
    near_sum = 0
    for x in range(-1, 2): # regarde autour en absisse (+1 -1)
        for y in range(-1, 2): # regarde autour en ordoonée (+1 -1)
            ''' debugage des coins '''
            if x != 0 or y != 0: 
                if x != 1 and y != 1 and coo[0] != 10 and coo[1] != 10 and grille[(int(coo[0]-x), coo[1]-y)][0] == "-1": #regarde si il y a une bombe en eliminant les bordures de coordonée 1 et 10
                    near_sum += 1 
    return near_sum  

    
def show_debug_grid(grille):
    print("""
====    grille secrète:  ====
""")
    print("      1  2  3  4  5  6  7  8  9  10")
    print("    ________________________________")
    for y in range(1, 11):
        if y == 10: # pour la derniere ligne
            print(f"{y} | ", end="")   # {y} coorespond a tous les coordonée en ordonné de 1 a 10 il les affiches donc
        else:                               # supprimer un espace à cause des 2 chiffres provoquant un décalage de ligne 
            print(f"{y}  | ", end="") 
        for x in range(1, 11):
            type_element = grille[(x, y)][0]
            if type_element.startswith("-") is False: 
                type_element = " " + type_element
            print(type_element, end=" ")
        print("|") # | pour fermer la grille 
    print("    --------------------------------")



def show_player_grid(grille):
    """Prints the player grid"""
    print("""
====    grille démineur:  ====
""")
    print("      1  2  3  4  5  6  7  8  9  10")
    print("    ________________________________")
    for y in range(1, 11):
        if y == 10: ## pour la derniere ligne
            print(f"{y} | ", end="")  # {y} coorespond a tous les coordonée en ordonné de 1 a 10 il les affiches donc
        else:                           # supprimer un espace à cause des 2 chiffres provoquant un décalage de ligne 
            print(f"{y}  | ", end="")
        for x in range(1, 11):
            if grille[(x, y)][2] is True: # lorsque l element est decouvert par le joueur ca l'affiche
                print(" " + str(calculate_near_sum((x, y), grille)), end=" ") #ca affiche le numero en suprimant les espaces (debug)
            elif grille[(x, y)][2] is None: # si il a tape d il place donc un drapeau car d pace la derniere valeur du dico en None
                print(" #", end=" ") 
            else:
                print(" .", end=" ") #affichage geneale de la grille
        print("|") # ferme le coté droit de la grille
    print("    --------------------------------")


# fonction principale

grille = generate_grid()
liste_position = generate_mines()
add_mines_to_grid(liste_position, grille)





while True:
    show_player_grid(grille)
    choix_joueur = str(input("Que voulez vous faire ?, découvrir une case: c ; planter un drapeau: d\n")) #demande au joueur de taper c ou d
    if choix_joueur == "c" or choix_joueur == "d": #si il tape c ou d ca continue si non il affiche un message d erreur crer par nos soins
        positionx_joueur = int(input("saisissez l'abscisse de la case: "))  #demande les coordonées en absisse 
        positiony_joueur = int(input("saisissez l'ordonnée de la case: ")) #demande les coordonées en ordonnée
        if 1 <= positionx_joueur <= 10 and 1 <= positiony_joueur <= 10:   # vérifier si l'entrée existe    
            if grille[(positionx_joueur, positiony_joueur)][2] is False:  # si la case n'a pas encore été découvert :
                if choix_joueur == "c": #si le joueur a tapé c:
                    if grille[(positionx_joueur, positiony_joueur)][0] == "-1":  # si cette case est une bombe 
                        print("BOOM !")
                        exit() #cela sort du programme
                    grille[(positionx_joueur, positiony_joueur)][2] = True  #dans tous les cas ca la marque comme découverte
                if choix_joueur == "d": #si le joueur a tapé d:
                    grille[(positionx_joueur, positiony_joueur)][2] = None # affiche un # qui sera suprimable ou possible de changer de place
                    grille[(positionx_joueur, positiony_joueur)][0] == "-2" # marquer le cas comme un drapeau
            else:
                print("Mauvaise touche !") # cela s'affiche si le joueur n'a tapé ni c ni d
        else:
            print("case invalide !") # cela s'affiche si le joueur entre des coordonées invalide (> 10 10)
    elif choix_joueur == "debug": #il faut ecrire debug pour que la grille des solutions s'affiche 
        show_debug_grid(grille) #cela affiche la grille de debug
