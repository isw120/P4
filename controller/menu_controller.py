from model.Tournoi import Tournoi
from model.Joueur import Joueur
from datetime import date

new_players = []

class MenuController:

    def createANewTournement(self):
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        print("Creating Tournement....")
        tournoi = Tournoi("tournoi01", "Paris", d1, 4, 3, 8, "bullet/blitz/coup rapide", "vide")
        print(tournoi)


    def addingNewPlayers(self):
        print("adding player :")
        name = input("Enter player name :")
        family_name = input("Enter player family name :")
        date_of_birth = input("Enter player date of birth :")
        sexe = input("Enter player sexe :")
        joureur = Joueur( family_name, name, date_of_birth, sexe,0)
        new_players.append(joureur)