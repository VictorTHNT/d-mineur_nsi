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
            grille[(colonne, ligne)] = ["0", "0", False, False]  # [type, nombre_de_mine_autour, decouverte]
    return grille



def generate_mines():
    """creation de la position de 20 mines aleatoires"""
    liste_position = []
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
            [x,y] = liste_position[i]
            grille[(x,y)] = ["-1", "0", False]
    return grille


def calculate_near_sum(coo, grille):
    near_sum = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                try:
                    if grille[(int(coo[0]-x), coo[1]-y)][0] == "-1":
                        near_sum += 1
                except:
                    pass
    return near_sum

    
def show_debug_grid(grille):
    print("""
====    grille secrète:  ====
""")
    print("      1  2  3  4  5  6  7  8  9  10")
    print("    ________________________________")
    for y in range(1, 11):
        if y == 10: # pour la derniere ligne
            print(f"{y} | ", end="")  # supprimer un espace à cause des 2 chiffres provoquant un décalage de ligne 
        else:
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
            print(f"{y} | ", end="")  # supprimer un espace à cause des 2 chiffres provoquant un décalage de ligne 
        else:
            print(f"{y}  | ", end="")
        for x in range(1, 11):
            if grille[(x, y)][2] is True: # lorsque l element est decouvert par le joueur ca l'affiche
                print(" " + str(calculate_near_sum((x, y), grille)), end=" ")
            elif grille[(x, y)][2] is None: 
                print(" #", end=" ")
            else:
                print(" .", end=" ")
        print("|") # ferme le coté droit de la grille
    print("    --------------------------------")


# fonction principale

grille = generate_grid()
liste_position = generate_mines()
add_mines_to_grid(liste_position, grille)





while True:
    show_player_grid(grille)
    choix_joueur = str(input("Que voulez vous faire ?, découvrir une case: c ; planter un drapeau: d\n"))
    if choix_joueur == "c" or choix_joueur == "d":
        positionx_joueur = int(input("saisissez l'abscisse de la case: "))
        positiony_joueur = int(input("saisissez l'ordonnée de la case: "))
        if 1 <= positionx_joueur <= 10 and 1 <= positiony_joueur <= 10:   # vérifier si l'entrée existe    
            if grille[(positionx_joueur, positiony_joueur)][2] is False:  # si la case n'a pas encore été découvert :
                if choix_joueur == "c":
                    if grille[(positionx_joueur, positiony_joueur)][0] == "-1":  # si cette case est une bombe 
                        print("BOOM !")
                        exit()
                    grille[(positionx_joueur, positiony_joueur)][2] = True  #dans tous les cas ca la marque comme découverte
                if choix_joueur == "d":
                    grille[(positionx_joueur, positiony_joueur)][2] = None # affiche un # qui sera suprimable ou possible de changer de place
                    grille[(positionx_joueur, positiony_joueur)][0] == "-2" # marquer le cas comme un drapeau
            else:
                print("Mauvaise touche !")
        else:
            print("case invalide !")
    elif choix_joueur == "debug":
        show_debug_grid(grille)