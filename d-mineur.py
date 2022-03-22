from random import randint
import colorama
from colorama import Fore, Back, Style


def generate_grid():
    """Generate the grid
    type:
     0: vide
    -1: mine
    """

    grid = {}
    for colonne in range(1, 11):
        for ligne in range(1, 11):
            grid[(colonne, ligne)] = ["0", False, False]  # [type, number_of_mines_surronding, discovered_bool]
    return grid


def generate_mines(number_mines):
    """creation des bombes aleatoirement choisie"""
    liste_position = []
    mine = 0
    while mine < number_mines:
        x=randint(1, 10)
        y=randint(1, 10)
        if (x,y) not in liste_position:
            liste_position.append((x,y))
            mine+=1
    return liste_position


def add_mines_to_grid(liste_position, grid, number_mines): 
    """ insérer des mines à des positions spécifiques stockées dans liste_position """
    for i in range(number_mines):
        if liste_position[0] in grid:
            [x,y] = liste_position[0]
            grid[(x,y)] = ["-1", "0", False]
            liste_position.remove(liste_position[0])
    return grid

def calculate_near_sum(coo, grille):
    near_sum = 0
    for x in range(-1, 2): # regarde autour en absisse (+1 -1)
        for y in range(-1, 2): # regarde autour en ordoonée (+1 -1)
            ''' debugage des coins '''
            if x != 0 or y != 0: 
                if x != 1 and y != 1 and coo[0] != 10 and coo[1] != 10 and grille[(int(coo[0]-x), coo[1]-y)][0] == "-1": #regarde si il y a une bombe en eliminant les bordures de coordonée 1 et 10
                    near_sum += 1 
    return near_sum  

def show_near_empty_cases(coo, grid): #victor 
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                try:
                    if grid[(int(coo[0]-x), int(coo[1]-y))][0] == "0":
                        grid[(int(coo[0]-x), int(coo[1]-y))][2] = True
                except:
                    pass



def show_debug_grid(grid):
    print("""
====    grille secrète:  ====
""")
    print("      1  2  3  4  5  6  7  8  9  10")
    print("    ________________________________")
    for y in range(1, 11):
        if y == 10: ## pour la dernière ligne
            print(f"{y} | ", end="")  # supprimer un espace à cause des 2 chiffres provoquant un décalage de ligne
        else:
            print(f"{y}  | ", end="") 
        for x in range(1, 11):
            type_element = grid[(x, y)][0]
            if type_element.startswith("-") is False:
                type_element = " " + type_element  # corrige le décalage de ligne '-'
            print(type_element, end=" ")
        print("|") # ferme le côté droit de la grille
    print("    --------------------------------")


def get_color_prefix(number): # lino
    if number == "1":
        return "\033[1;36;40m" # bleu
    if number == "2":
        return "\033[1;32;40m" # vert
    if number == "3":
        return "\033[1;31;40m" # rouge
    if number == "4":
        return "\033[1;37;40m" # blanc
    else:
        return ""

def show_player_grid(grid):
    """Prints the player grid"""
    print("""
====    grille démineur:  ====
""")
    print("      1  2  3  4  5  6  7  8  9  10")
    print("    ________________________________")
    for y in range(1, 11):
        if y == 10: ## pour imprimer 10 lignes
            print(f"{y} | ", end="")  
        else:                           ##supprimer un espace à cause des 2 chiffres provoquant un décalage de ligne
            print(f"{y}  | ", end="")
        for x in range(1, 11):
            if grid[(x, y)][1] is True: # si le drapeau est placé ici 
                print("\033[1;33;40m #\033[0m", end=" ")
            elif grid[(x, y)][2] is True: # lorsque l'élément est découvert par le joueur il l'affiche
                near_sum = str(calculate_near_sum((x,y), grid))
                print(" " + get_color_prefix(near_sum) + near_sum, end="\033[0m ") 
            else:
                print(" .", end=" ") 
        print("|") 
    print("    --------------------------------")


def check_if_coordinate_valid(positionx, positiony):  # cleante
    """ vérifier si les coordonnées (positionx et positiony) sont valides  """
    if 1 <= positionx <= 10 and 1 <= positiony <= 10:
        return True
    else:
        return False

def get_coordinates():
    """ demander les coordonnées à l'utilisateur """
    positionx = int(input("saisissez l'abscisse de la case: "))   
    positiony = int(input("saisissez l'ordonnée de la case: ")) 
    return positionx, positiony


def interact_case(first_move, grid): #leo
    """ cliquez sur un cas spécifique """
    positionx, positiony = get_coordinates()
    coo_valid = check_if_coordinate_valid(positionx, positiony)
    coo = positionx, positiony
    if first_move is True: 
        show_near_empty_cases(coo, grid)
    if coo_valid and grid[(positionx, positiony)][2] is False:  # si la case n'est pas encore découvert 
        if grid[(positionx, positiony)][0] == "-1": # si c'est une mine  
            print("BOOM !")
            play_game() #leo
        else:
            grid[(positionx, positiony)][2] = True  # marquer le cas comme découvert 
    else:
        if coo_valid is False:
            print("\033[1;31;40m" + "Coordonees invalides !! Veuillez entrer des coordonees corrects" + "\033[0m")
        
        else:
            print("Case déja découverte Veuillez choisir une autre case !")


def interact_flag(grid): #victor
    """ ajoute ou supprime un drapeau à des coordonnées spécifiques"""
    positionx, positiony = get_coordinates()
    coo_valid = check_if_coordinate_valid(positionx, positiony)
    interaction_type = input("Voulez vous ajouter (a) ou supprimer (s) un drappeau ? (a/s): ") 
    if coo_valid and interaction_type == "a":
        grid[(positionx, positiony)][1] = True  # ajouter un drapeau au case au coordonnées de position x y
    elif coo_valid and interaction_type == "s":
        grid[(positionx, positiony)][1] = False  # ajouter un drapeau au case au coordonnées de position x y
    else:
        if coo_valid is False:
            print("Coordonees invalides !! Veuillez entrer des coordonees corrects")
        
        else:
            print("Case déja découver, Veuillez choisir une autre case !")

def get_highest_score():
    """ retourne le meilleur score de highest_score""" 
    score_file = open('highest_score.txt','r')
    score = score_file.read()  #exactement ce qu on a fait un classe avec les fichiers CSV
    score_file.close()
    if score != "":
        return int(score)
    else:
        return 0  # pas de meilleur score sauvegardé


def save_highest_score(score): 
    """ save le score le plus eleve dans highest_score"""
    score_file = open('highest_score.txt','w')
    score_file.write(str(score))
    score_file.close()

# la fonction principale
def play_game(pseudo = "Joueur"): #lino
    """  Fonction, la fonction principale de démarrage du jeu """
    grid = generate_grid()
    number_mines = int(input("combien de mine voulez vous avoir dans la grille ? "))
    liste_position = generate_mines(number_mines)
    add_mines_to_grid(liste_position, grid, number_mines)

    highest_score = get_highest_score()
    first_move = True
    case_valid = 0

    while True:
        show_player_grid(grid)
        if case_valid > highest_score: #affichage fin de partie meilleur score
            print(f"Nouveau record battu {pseudo} ! le score de {case_valid} est atteint")
            save_highest_score(case_valid) # SAuvegarde du meilleur score
        choix_joueur = str(input("Que voulez vous faire ?,\ndécouvrir une case: c ; planter un drapeau: d\n")) 
        if choix_joueur == "c": #si le joueur repond c
            interact_case(first_move, grid) # Validité de la case
            first_move = False # regarde si c est le premier mouv
            case_valid += 1 # rajoute un coup dans la fiche des scores
        elif choix_joueur == "d": #choix du joueur drapeau (retourne a la fonction intearct_flag)
            interact_flag(grid) 
        elif choix_joueur == "NSI":  
            show_debug_grid(grid) #grille des solutions
    

def Credit():
    print("""Créé par Victor Lino et Leo, en collaboration avec Mr Coudert""")

username = None
exit_now = False
colorama.init()
while exit_now is not True:
    menu_ask = input("Que voulez vous faire ? Ecrivez: \n\n• JOUER pour lancer le jeu \n\n• CREDIT pour afficher les crédits \n\n• NOM pour changer de nom \n\n• SORTIE pour sortir \n\n")
    if menu_ask == "NOM":
        username = input("Quel est votre pseudo ?")
    if menu_ask == "JOUER":
        if username is not None:
            play_game(username)
        else:
            play_game()
    if menu_ask == "CREDIT":
        Credit()
    if menu_ask == "SORTIE":
        exit_now = True
        exit()

    
