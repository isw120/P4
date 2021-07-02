from model.Tournoi import Tournoi
from model.Joueur import Joueur
from model.Tour import Tour
from datetime import date, datetime
from controller import DatabaseController

new_players2 = []

new_players3 = []

new_players4 = []

new_players5 = []

first_half = []

second_half = []

first_half_2 = []

second_half_2 = []

first_half_3 = []

second_half_3 = []

peer = []

peer2 = []

peer3 = []

players_score = []

controller = DatabaseController.DatabaseController()

class MenuController:

    def createANewTournement(self):
        print("Creating a new Tournement")
        name = input("Enter tournement name :")
        place = input("Enter tournement place :")
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        time_controll = input("Enter tournement time controll (bullet, blitz, coup rapide) :")
        description = input("Enter tournement description :")
        tournoi = Tournoi(name, place, d1, 4, None, None, time_controll, description, None, None, None)

        return tournoi

    def addingNewPlayers(self):
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

        joureur = Joueur(family_name, name, date_of_birth, sexe, classement)

        return joureur


    def startingTournemant(self):

        tournement_name = input("Enter Tournement name :")

        number = 0
        while(number < 8):
            family_name = input("Enter player family name :")
            name = input("Enter player name :")
            serialized_player = controller.getByFamillyName(family_name, name)
            if serialized_player is not None:
                new_players2.append(serialized_player)
                number = number + 1
            else:
                print("this player was not found try again :")
                continue

        serialized_tournement = controller.getTournementByName(tournement_name)

        tournoi = Tournoi(serialized_tournement["Nom"],  serialized_tournement["Lieu"],  serialized_tournement["Date"],  serialized_tournement["Nombre_de_tours"],  serialized_tournement["Tournees"], new_players2,  serialized_tournement["Controle_du_temps"],  serialized_tournement["Description"],
                          serialized_tournement["status"], serialized_tournement["secondRoundPlayers"],
                          serialized_tournement["thirdRoundPlayers"])

        controller.updateTournementByName(tournoi)

        self.dividePlayers(tournoi)


    def continueTournement(self):

        tournement_name = input("Enter Tournement name :")

        serialized_tournement = controller.getTournementByName(tournement_name)

        tournoi = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"], serialized_tournement["Date"],
                          serialized_tournement["Nombre_de_tours"], serialized_tournement["Tournees"], serialized_tournement["Joueurs"],
                          serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                          serialized_tournement["status"], serialized_tournement["secondRoundPlayers"],
                          serialized_tournement["thirdRoundPlayers"])

        if tournoi.status == "first round":
            self.secondRound(tournoi)
        elif tournoi.status == "second round":
            self.thirdRound(tournoi)


    def dividePlayers(self, tournoi):
        print("Round 1 :")
        serialized_players = tournoi.Joueurs

        for player in serialized_players:
            joureur = Joueur(player["Nom_de_famille"], player["Prenom"], player["Date_de_naissance"], player["Sexe"], player["Classement"])
            new_players3.append(joureur)

        index = len(new_players3) // 2

        first_half = new_players3[:index]

        second_half = new_players3[index:]

        peer.extend(zip(first_half, second_half))

        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        tour = Tour("tour 1", date_and_time, None, None)

        matches = []

        for first, second in peer:

            score1 = input("Enter the score for the player : " + first.Nom_de_famille + " : ")
            score2 = input("Enter the score for the player : " + second.Nom_de_famille + " : ")

            if score1 == "1":
                ##new_players3.remove(first)
                new_players4.append(first)
            elif score2 == "1":
                new_players4.append(second)
                ##new_players3.remove(second)
            elif score1 == "0.5" and score2 == "0.5":
                new_players4.append(first)

            test = input("changer le classement ??")

            if test == "oui":
                first.Classement = input("enter new classment for " + first.Nom_de_famille + " " + first.Prenom + " : ")
                second.Classement = input("enter new classment for " + second.Nom_de_famille + " " + second.Prenom + " : ")

            first_ser = {
                'Nom_de_famille': first.Nom_de_famille,
                'Prenom': first.Prenom,
                'Date_de_naissance': first.Date_de_naissance,
                'Sexe': first.Sexe,
                'Classement': first.Classement
            }

            second_ser = {
                'Nom_de_famille': second.Nom_de_famille,
                'Prenom': second.Prenom,
                'Date_de_naissance': second.Date_de_naissance,
                'Sexe': second.Sexe,
                'Classement': second.Classement
            }

            list_a = [first_ser, second_ser]
            list_b = [score1, score2]

            matches.append(list(zip(list_a, list_b)))

        end_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tour.endDateAndHour = end_date_and_time
        tour.matches = matches

        tour1_ser = {
            'name': tour.name,
            'beginDateAndHour': tour.beginDateAndHour,
            'endDateAndHour': tour.endDateAndHour,
            'matches': tour.matches
        }

        round_list = []

        round_list.append(tour1_ser)

        tournoi.Tournees = round_list

        tournoi.status = "first round"

        secondRoundPlayers = []

        for player in new_players4:
            serialized_player = {
                'Nom_de_famille': player.Nom_de_famille,
                'Prenom': player.Prenom,
                'Date_de_naissance': player.Date_de_naissance,
                'Sexe': player.Sexe,
                'Classement': player.Classement
            }

            secondRoundPlayers.append(serialized_player)

        tournoi.secondRoundPlayers = secondRoundPlayers

        controller.updateTournementByName(tournoi)

        self.secondRound(tournoi)


    def secondRound(self, tournoi):

        print("Round 2 :")

        if len(new_players4) == 0:
            for player in tournoi.secondRoundPlayers:
                joureur = Joueur(player["Nom_de_famille"], player["Prenom"], player["Date_de_naissance"],
                                 player["Sexe"], player["Classement"])
                new_players4.append(joureur)

        index = len(new_players4) // 2

        first_half_2 = new_players4[:index]

        second_half_2 = new_players4[index:]

        peer2.extend(zip(first_half_2, second_half_2))

        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        tour2 = Tour("tour 2", date_and_time, None, None)

        matches2 = []

        for first, second in peer2:

            score1 = input("Enter the score for the player : " + first.Nom_de_famille)
            score2 = input("Enter the score for the player : " + second.Nom_de_famille)

            if score1 == "1":
                ##new_players3.remove(first)
                new_players5.append(first)
            elif score2 == "1":
                new_players5.append(second)
                ##new_players3.remove(second)
            elif score1 == "0.5" and score2 == "0.5":
                new_players4.append(first)

            test = input("changer le classement ??")

            if test == "oui":
                first.Classement = input("enter new classment for " + first.Nom_de_famille + " " + first.Prenom + " : ")
                second.Classement = input("enter new classment for " + second.Nom_de_famille + " " + second.Prenom + " : ")

            first_ser = {
                'Nom_de_famille': first.Nom_de_famille,
                'Prenom': first.Prenom,
                'Date_de_naissance': first.Date_de_naissance,
                'Sexe': first.Sexe,
                'Classement': first.Classement
            }

            second_ser = {
                'Nom_de_famille': second.Nom_de_famille,
                'Prenom': second.Prenom,
                'Date_de_naissance': second.Date_de_naissance,
                'Sexe': second.Sexe,
                'Classement': second.Classement
            }

            list_a = [first_ser, second_ser]
            list_b = [score1, score2]

            matches2.append(list(zip(list_a, list_b)))

        end_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tour2.endDateAndHour = end_date_and_time
        tour2.matches = matches2

        tour2_ser = {
            'name': tour2.name,
            'beginDateAndHour': tour2.beginDateAndHour,
            'endDateAndHour': tour2.endDateAndHour,
            'matches': tour2.matches
        }

        round_list = []

        for a in tournoi.Tournees:
            round_one = {
                'name': a["name"],
                'beginDateAndHour': a["beginDateAndHour"],
                'endDateAndHour': a["endDateAndHour"],
                'matches': a["matches"]
            }
            round_list.append(round_one)

        round_list.append(tour2_ser)

        tournoi.Tournees = round_list

        tournoi.status = "second round"

        thirdRoundPlayers = []

        for player in new_players5:
            serialized_player = {
                'Nom_de_famille': player.Nom_de_famille,
                'Prenom': player.Prenom,
                'Date_de_naissance': player.Date_de_naissance,
                'Sexe': player.Sexe,
                'Classement': player.Classement
            }

            thirdRoundPlayers.append(serialized_player)

        tournoi.thirdRoundPlayers = thirdRoundPlayers

        controller.updateTournementByName(tournoi)

        self.thirdRound(tournoi)


    def thirdRound(self, tournoi):

        print("Round 3 :")

        if len(new_players5) == 0:
            for player in tournoi.thirdRoundPlayers:
                joureur = Joueur(player["Nom_de_famille"], player["Prenom"], player["Date_de_naissance"],
                                 player["Sexe"], player["Classement"])
                new_players5.append(joureur)

        index = len(new_players5) // 2

        first_half_3 = new_players5[:index]

        second_half_3 = new_players5[index:]

        peer3.extend(zip(first_half_3, second_half_3))

        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        tour3 = Tour("tour 3", date_and_time, None, None)

        matches3 = []

        for first, second in peer3:
            score1 = input("Enter the score for the player : " + first.Nom_de_famille)
            score2 = input("Enter the score for the player : " + second.Nom_de_famille)

            if score1 == "0.5" and score2 == "0.5":
                new_players4.append(first)

            test = input("changer le classement ??")

            if test == "oui":
                first.Classement = input("enter new classment for " + first.Nom_de_famille + " " + first.Prenom + " : ")
                second.Classement = input("enter new classment for " + second.Nom_de_famille + " " + second.Prenom + " : ")

            first_ser = {
                'Nom_de_famille': first.Nom_de_famille,
                'Prenom': first.Prenom,
                'Date_de_naissance': first.Date_de_naissance,
                'Sexe': first.Sexe,
                'Classement': first.Classement
            }

            second_ser = {
                'Nom_de_famille': second.Nom_de_famille,
                'Prenom': second.Prenom,
                'Date_de_naissance': second.Date_de_naissance,
                'Sexe': second.Sexe,
                'Classement': second.Classement
            }

            list_a = [first_ser, second_ser]
            list_b = [score1, score2]

            matches3.append(list(zip(list_a, list_b)))

        end_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tour3.endDateAndHour = end_date_and_time
        tour3.matches = matches3

        tour3_ser = {
            'name': tour3.name,
            'beginDateAndHour': tour3.beginDateAndHour,
            'endDateAndHour': tour3.endDateAndHour,
            'matches': tour3.matches
        }

        round_list = []

        for a in tournoi.Tournees:
            round_one = {
                'name': a["name"],
                'beginDateAndHour': a["beginDateAndHour"],
                'endDateAndHour': a["endDateAndHour"],
                'matches': a["matches"]
            }
            round_list.append(round_one)

        round_list.append(tour3_ser)

        tournoi.Tournees = round_list

        allPlayers = []

        serialized_players = tournoi.Joueurs

        for player in serialized_players:
            joureur = Joueur(player["Nom_de_famille"], player["Prenom"], player["Date_de_naissance"], player["Sexe"],
                             player["Classement"])
            classment = input("enter new classment for " + joureur.Nom_de_famille + " " + joureur.Prenom + " : ")
            joueur = {
                'Nom_de_famille': joureur.Nom_de_famille,
                'Prenom': joureur.Prenom,
                'Date_de_naissance': joureur.Date_de_naissance,
                'Sexe': joureur.Sexe,
                'Classement': classment
            }
            allPlayers.append(joueur)

        tournoi.Joueurs = allPlayers

        controller.updateTournementByName(tournoi)



    def creatReports(self):

        print("1) list all actors by alphabet order")
        print("2) list all actors by classment")
        print("3) list all players of a tournement by alphabet order")
        print("4) list all players of a tournement by classment")
        print("5) list all tournements")
        print("6) list all rounds of a tournement")
        print("7) list all matches of a tournement")
        option = input("choose an option :")

        if (option == "1"):
            all = controller.getAllPlayers()
            orderedList = sorted(all, key=lambda j: j['Nom_de_famille'])
            print(orderedList)
        if (option == "2"):
            all = controller.getAllPlayers()
            orderedList = sorted(all, key=lambda j: j['Classement'])
            print(orderedList)
        if (option == "3"):
            name = input("enter tournement name : ")
            serialized_tournement = controller.getTournementByName(name)
            tournement = Tournoi(serialized_tournement["Nom"],  serialized_tournement["Lieu"],  serialized_tournement["Date"],  serialized_tournement["Nombre_de_tours"],  serialized_tournement["Tournees"], serialized_tournement["Joueurs"],  serialized_tournement["Controle_du_temps"],  serialized_tournement["Description"], serialized_tournement["status"], serialized_tournement["secondRoundPlayers"], serialized_tournement["thirdRoundPlayers"])
            players = tournement.Joueurs
            orderedList = sorted(players, key=lambda j: j['Nom_de_famille'])
            print(orderedList)
        if (option == "4"):
            name = input("enter tournement name : ")
            serialized_tournement = controller.getTournementByName(name)
            tournement = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"],
                                 serialized_tournement["Date"], serialized_tournement["Nombre_de_tours"],
                                 serialized_tournement["Tournees"], serialized_tournement["Joueurs"],
                                 serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                                 serialized_tournement["status"], serialized_tournement["secondRoundPlayers"], serialized_tournement["thirdRoundPlayers"])
            players = tournement.Joueurs
            orderedList = sorted(players, key=lambda j: j['Classement'])
            print(orderedList)
        if (option == "5"):
            all = controller.getAllTournements()
            print(all)
        if (option == "6"):
            name = input("enter tournement name : ")
            serialized_tournement = controller.getTournementByName(name)
            tournement = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"],
                                 serialized_tournement["Date"], serialized_tournement["Nombre_de_tours"],
                                 serialized_tournement["Tournees"], serialized_tournement["Joueurs"],
                                 serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                                 serialized_tournement["status"], serialized_tournement["secondRoundPlayers"], serialized_tournement["thirdRoundPlayers"])
            allRounds = tournement.Tournees
            print(allRounds)
        if (option == "7"):
            name = input("enter tournement name : ")
            serialized_tournement = controller.getTournementByName(name)
            tournement = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"],
                                 serialized_tournement["Date"], serialized_tournement["Nombre_de_tours"],
                                 serialized_tournement["Tournees"], serialized_tournement["Joueurs"],
                                 serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                                 serialized_tournement["status"], serialized_tournement["secondRoundPlayers"], serialized_tournement["thirdRoundPlayers"])
            serialized_rounds = tournement.Tournees

            for element in serialized_rounds:
                print(element["matches"])




