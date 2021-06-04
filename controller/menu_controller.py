from turtle import pd

from model.Tournoi import Tournoi
from model.Joueur import Joueur
from datetime import date
import datetime

new_players = [Joueur("Abrahamyan", "Tatev",datetime.datetime(1988, 1, 13).strftime("%d/%m/%Y"), "Female", 1),
               Joueur( "Markos", "Jan",datetime.datetime(1985, 7, 2).strftime("%d/%m/%Y"), "Male", 2),
               Joueur( "Badelka", "Olga",datetime.datetime(2002, 7, 8).strftime("%d/%m/%Y"),"Female", 3),
               Joueur( "Morphy", "Paul",datetime.datetime(1837, 6, 22).strftime("%d/%m/%Y"),"Male",4),
               Joueur( "Bellin", "Jana",datetime.datetime(1947, 12, 9).strftime("%d/%m/%Y"), "Female", 5),
               Joueur( "Nunn", "John",datetime.datetime(1955, 4, 25).strftime("%d/%m/%Y"),"Male", 6),
               Joueur( "Xiangzhi","Bu",datetime.datetime(1985, 12, 10).strftime("%d/%m/%Y"),"Male", 7),
               Joueur( "Sachdev", "Tania",datetime.datetime(1986, 8, 20).strftime("%d/%m/%Y"),"Female", 8)]

first_half = []

second_half = []

peer = []

players_score = []
class MenuController:

    def createANewTournement(self):
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        print("Creating Tournement....")
        tournoi = Tournoi("tournoi01", "Paris", d1, 4, 3, 8, "bullet/blitz/coup rapide", "vide")
        print(tournoi)

        self.dividePlayers()

    def addingNewPlayers(self):
        print("adding player :")
        name = input("Enter player name :")
        family_name = input("Enter player family name :")
        date_of_birth = input("Enter player date of birth :")
        sexe = input("Enter player sexe :")
        status = True
        while(status):
            classement = input("Enter a classement :")
            if classement.isalpha() or int(classement) < 0:
                print("classement must be a positive number")
            else:
                status = False

        joureur = Joueur( family_name, name, date_of_birth, sexe, classement)
        new_players.append(joureur)

    def displayPlayersList(self):
        if len(new_players) == 0:
            print("There are no players registred in the app")
        else:
            for element in new_players:
                print(element)



    def dividePlayers(self):

        index = len(new_players) // 2

        first_half = new_players[:index]

        second_half = new_players[index:]

        peer.extend(zip(first_half, second_half))

        for first, second in peer:
            score1 = input("Enter the score for the player : " + first.Nom_de_famille)
            score2 = input("Enter the score for the player : " + second.Nom_de_famille)
            players_score.append([first, score1])
            players_score.append([second, score2])


        print("players")
        for element in first_half:
            print(element)
        print("middle")
        for element in second_half:
            print(element)
        print("peer")
        for first, second in peer:
            print(first, second)

        print("score")
        for first, second in players_score:
            print(first, second)


