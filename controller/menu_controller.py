from model.Tournoi import Tournoi
from model.Joueur import Joueur
from model.Tour import Tour
from datetime import date, datetime
from controller import DatabaseController


class MenuController:
    db_controller = DatabaseController.DatabaseController()

    def createANewTournement(self):
        print("Creating a new tournement")
        name = input("Enter tournement name : ")
        place = input("Enter tournement place : ")
        today = date.today()
        formated_day = today.strftime("%d/%m/%Y")
        time_controll = input("Enter tournement time controll (bullet, blitz, coup rapide) : ")
        description = input("Enter tournement description : ")
        tournoi = Tournoi(name, place, formated_day, 4, None, None, time_controll, description, None, None, None)

        self.db_controller.insertTournement(tournoi)

    def addingANewPlayer(self):
        print("Creating a new player")
        name = input("Enter player name : ")
        family_name = input("Enter player family name : ")
        date_of_birth = input("Enter player date of birth : ")
        sexe = input("Enter player sexe : ")
        while True:
            classement = input("Enter a classement : ")
            if classement.isalpha() or int(classement) < 0:
                print("classement must be a positive number")
            else:
                break

        joueur = Joueur(family_name, name, date_of_birth, sexe, classement)

        self.db_controller.insertPlayer(joueur)

    def startingTournemant(self):

        serialized_tournement = None

        while True:
            tournement_name = input("Enter tournement name :")
            serialized_tournement = self.db_controller.getTournementByName(tournement_name)
            if serialized_tournement is not None:
                break
            else:
                print("This tournement was not found try again")
                continue

        number = 0
        players_list = []
        while number < 8:
            family_name = input("Enter player family name : ")
            name = input("Enter player name : ")
            serialized_player = self.db_controller.getAPlayer(family_name, name)
            if serialized_player is not None:
                players_list.append(serialized_player)
                number = number + 1
            else:
                print("This player was not found try again")
                continue

        tournoi = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"], serialized_tournement["Date"],
                          serialized_tournement["Nombre_de_tours"], serialized_tournement["Tournees"], players_list,
                          serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                          serialized_tournement["status"], serialized_tournement["secondRoundPlayers"],
                          serialized_tournement["thirdRoundPlayers"])

        self.db_controller.updateTournementByName(tournoi)

        self.dividePlayers(tournoi)

    def continueTournement(self):

        serialized_tournement = None

        while True:
            tournement_name = input("Enter tournement name : ")
            serialized_tournement = self.db_controller.getTournementByName(tournement_name)
            if serialized_tournement is not None:
                break
            else:
                print("This tournement was not found try again")
                continue

        tournoi = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"], serialized_tournement["Date"],
                          serialized_tournement["Nombre_de_tours"], serialized_tournement["Tournees"],
                          serialized_tournement["Joueurs"],
                          serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                          serialized_tournement["status"], serialized_tournement["secondRoundPlayers"],
                          serialized_tournement["thirdRoundPlayers"])

        if tournoi.status == "first round":
            self.secondRound(tournoi)
        elif tournoi.status == "second round":
            self.thirdRound(tournoi)
        else:
            print("This tournement is finished")

    def dividePlayers(self, tournoi):

        print("Round 1 :")

        serialized_players = tournoi.Joueurs

        first_round_players = []
        first_round_peers = []
        next_round_players = []

        for player in serialized_players:
            joueur = Joueur(player["Nom_de_famille"], player["Prenom"], player["Date_de_naissance"], player["Sexe"],
                            player["Classement"])
            first_round_players.append(joueur)

        index = len(first_round_players) // 2

        first_half = first_round_players[:index]

        second_half = first_round_players[index:]

        first_round_peers.extend(zip(first_half, second_half))

        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        tour = Tour("tour 1", date_and_time, None, None)

        first_round_matches = []

        for first, second in first_round_peers:

            score1 = input("Enter the score for the player : " + first.Nom_de_famille + " : ")
            score2 = input("Enter the score for the player : " + second.Nom_de_famille + " : ")

            if score1 == "1":
                next_round_players.append(first)
            elif score2 == "1":
                next_round_players.append(second)
            elif score1 == "0.5" and score2 == "0.5":
                next_round_players.append(first)

            serialized_first_player = {
                'Nom_de_famille': first.Nom_de_famille,
                'Prenom': first.Prenom,
                'Date_de_naissance': first.Date_de_naissance,
                'Sexe': first.Sexe,
                'Classement': first.Classement
            }

            serialized_second_player = {
                'Nom_de_famille': second.Nom_de_famille,
                'Prenom': second.Prenom,
                'Date_de_naissance': second.Date_de_naissance,
                'Sexe': second.Sexe,
                'Classement': second.Classement
            }

            players = [serialized_first_player, serialized_second_player]
            scores = [score1, score2]

            first_round_matches.append(list(zip(players, scores)))

        end_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tour.endDateAndHour = end_date_and_time
        tour.matches = first_round_matches

        serialized_round = {
            'name': tour.name,
            'beginDateAndHour': tour.beginDateAndHour,
            'endDateAndHour': tour.endDateAndHour,
            'matches': tour.matches
        }

        round_list = [serialized_round]

        tournoi.Tournees = round_list

        tournoi.status = "first round"

        second_round_players = []

        for player in next_round_players:
            serialized_player = {
                'Nom_de_famille': player.Nom_de_famille,
                'Prenom': player.Prenom,
                'Date_de_naissance': player.Date_de_naissance,
                'Sexe': player.Sexe,
                'Classement': player.Classement
            }

            second_round_players.append(serialized_player)

        tournoi.secondRoundPlayers = second_round_players

        self.db_controller.updateTournementByName(tournoi)

        self.secondRound(tournoi)

    def secondRound(self, tournoi):

        print("Round 2 :")

        second_round_players = []
        second_round_peers = []
        next_round_players = []

        for player in tournoi.secondRoundPlayers:
            joueur = Joueur(player["Nom_de_famille"], player["Prenom"], player["Date_de_naissance"],
                            player["Sexe"], player["Classement"])
            second_round_players.append(joueur)

        index = len(second_round_players) // 2

        first_half = second_round_players[:index]

        second_half = second_round_players[index:]

        second_round_peers.extend(zip(first_half, second_half))

        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        tour = Tour("tour 2", date_and_time, None, None)

        second_round_matches = []

        for first, second in second_round_peers:

            score1 = input("Enter the score for the player : " + first.Nom_de_famille + " : ")
            score2 = input("Enter the score for the player : " + second.Nom_de_famille + " : ")

            if score1 == "1":
                next_round_players.append(first)
            elif score2 == "1":
                next_round_players.append(second)
            elif score1 == "0.5" and score2 == "0.5":
                next_round_players.append(first)

            serialized_first_player = {
                'Nom_de_famille': first.Nom_de_famille,
                'Prenom': first.Prenom,
                'Date_de_naissance': first.Date_de_naissance,
                'Sexe': first.Sexe,
                'Classement': first.Classement
            }

            serialized_second_player = {
                'Nom_de_famille': second.Nom_de_famille,
                'Prenom': second.Prenom,
                'Date_de_naissance': second.Date_de_naissance,
                'Sexe': second.Sexe,
                'Classement': second.Classement
            }

            players = [serialized_first_player, serialized_second_player]
            scores = [score1, score2]

            second_round_matches.append(list(zip(players, scores)))

        end_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tour.endDateAndHour = end_date_and_time
        tour.matches = second_round_matches

        serialized_round = {
            'name': tour.name,
            'beginDateAndHour': tour.beginDateAndHour,
            'endDateAndHour': tour.endDateAndHour,
            'matches': tour.matches
        }

        round_list = []

        for r in tournoi.Tournees:
            round = {
                'name': r["name"],
                'beginDateAndHour': r["beginDateAndHour"],
                'endDateAndHour': r["endDateAndHour"],
                'matches': r["matches"]
            }
            round_list.append(round)

        round_list.append(serialized_round)

        tournoi.Tournees = round_list

        tournoi.status = "second round"

        third_round_players = []

        for player in next_round_players:
            serialized_player = {
                'Nom_de_famille': player.Nom_de_famille,
                'Prenom': player.Prenom,
                'Date_de_naissance': player.Date_de_naissance,
                'Sexe': player.Sexe,
                'Classement': player.Classement
            }

            third_round_players.append(serialized_player)

        tournoi.thirdRoundPlayers = third_round_players

        self.db_controller.updateTournementByName(tournoi)

        self.thirdRound(tournoi)

    def thirdRound(self, tournoi):

        print("Round 3 :")

        third_round_players = []
        third_round_peers = []

        for player in tournoi.thirdRoundPlayers:
            joueur = Joueur(player["Nom_de_famille"], player["Prenom"], player["Date_de_naissance"],
                            player["Sexe"], player["Classement"])
            third_round_players.append(joueur)

        index = len(third_round_players) // 2

        first_half = third_round_players[:index]

        second_half = third_round_players[index:]

        third_round_peers.extend(zip(first_half, second_half))

        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        tour = Tour("tour 3", date_and_time, None, None)

        third_round_matches = []

        for first, second in third_round_peers:
            score1 = input("Enter the score for the player : " + first.Nom_de_famille + " : ")
            score2 = input("Enter the score for the player : " + second.Nom_de_famille + " : ")

            serialized_first_player = {
                'Nom_de_famille': first.Nom_de_famille,
                'Prenom': first.Prenom,
                'Date_de_naissance': first.Date_de_naissance,
                'Sexe': first.Sexe,
                'Classement': first.Classement
            }

            serialized_second_player = {
                'Nom_de_famille': second.Nom_de_famille,
                'Prenom': second.Prenom,
                'Date_de_naissance': second.Date_de_naissance,
                'Sexe': second.Sexe,
                'Classement': second.Classement
            }

            players = [serialized_first_player, serialized_second_player]
            scores = [score1, score2]

            third_round_matches.append(list(zip(players, scores)))

        end_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tour.endDateAndHour = end_date_and_time
        tour.matches = third_round_matches

        serialized_round = {
            'name': tour.name,
            'beginDateAndHour': tour.beginDateAndHour,
            'endDateAndHour': tour.endDateAndHour,
            'matches': tour.matches
        }

        round_list = []

        for r in tournoi.Tournees:
            round = {
                'name': r["name"],
                'beginDateAndHour': r["beginDateAndHour"],
                'endDateAndHour': r["endDateAndHour"],
                'matches': r["matches"]
            }
            round_list.append(round)

        round_list.append(serialized_round)

        tournoi.Tournees = round_list

        tournoi.status = "finished"

        new_players_classment = []

        serialized_players = tournoi.Joueurs

        for player in serialized_players:
            joueur = Joueur(player["Nom_de_famille"], player["Prenom"], player["Date_de_naissance"], player["Sexe"],
                            player["Classement"])
            classment = input(
                "enter the new classment for the player : " + joueur.Nom_de_famille + " " + joueur.Prenom + " : ")
            serialized_player = {
                'Nom_de_famille': joueur.Nom_de_famille,
                'Prenom': joueur.Prenom,
                'Date_de_naissance': joueur.Date_de_naissance,
                'Sexe': joueur.Sexe,
                'Classement': classment
            }
            new_players_classment.append(serialized_player)

        tournoi.Joueurs = new_players_classment

        self.db_controller.updateTournementByName(tournoi)

    def creatReports(self):
        while True:
            print("1) list all actors by alphabet order")
            print("2) list all actors by classment")
            print("3) list all players of a tournement by alphabet order")
            print("4) list all players of a tournement by classment")
            print("5) list all tournements")
            print("6) list all rounds of a tournement")
            print("7) list all matches of a tournement")
            print("8) Exit reports menu")
            option = input("choose an option :")

            if option == "1":
                all_players_list = self.db_controller.getAllPlayers()
                ordered_list = sorted(all_players_list, key=lambda j: j['Nom_de_famille'])
                for player in ordered_list:
                    print("Nom_de_famille : " + player["Nom_de_famille"])
                    print("Prenom : " + player["Prenom"])
                    print("Date_de_naissance : " + player["Date_de_naissance"])
                    print("Sexe : " + player["Sexe"])
                    print("Classement : " + player["Classement"] + "\n")
            if option == "2":
                all_players_list = self.db_controller.getAllPlayers()
                ordered_list = sorted(all_players_list, key=lambda j: j['Classement'])
                for player in ordered_list:
                    print("Nom_de_famille : " + player["Nom_de_famille"])
                    print("Prenom : " + player["Prenom"])
                    print("Date_de_naissance : " + player["Date_de_naissance"])
                    print("Sexe : " + player["Sexe"])
                    print("Classement : " + player["Classement"] + "\n")
            if option == "3":
                while True:
                    tournement_name = input("Enter tournement name : ")
                    serialized_tournement = self.db_controller.getTournementByName(tournement_name)
                    if serialized_tournement is not None:
                        break
                    else:
                        print("This tournement was not found try again")
                        continue

                tournement = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"],
                                     serialized_tournement["Date"], serialized_tournement["Nombre_de_tours"],
                                     serialized_tournement["Tournees"], serialized_tournement["Joueurs"],
                                     serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                                     serialized_tournement["status"], serialized_tournement["secondRoundPlayers"],
                                     serialized_tournement["thirdRoundPlayers"])
                tournement_players = tournement.Joueurs
                ordered_list = sorted(tournement_players, key=lambda j: j['Nom_de_famille'])
                for player in ordered_list:
                    print("Nom_de_famille : " + player["Nom_de_famille"])
                    print("Prenom : " + player["Prenom"])
                    print("Date_de_naissance : " + player["Date_de_naissance"])
                    print("Sexe : " + player["Sexe"])
                    print("Classement : " + player["Classement"] + "\n")
            if option == "4":

                while True:
                    tournement_name = input("Enter tournement name : ")
                    serialized_tournement = self.db_controller.getTournementByName(tournement_name)
                    if serialized_tournement is not None:
                        break
                    else:
                        print("This tournement was not found try again")
                        continue

                tournement = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"],
                                     serialized_tournement["Date"], serialized_tournement["Nombre_de_tours"],
                                     serialized_tournement["Tournees"], serialized_tournement["Joueurs"],
                                     serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                                     serialized_tournement["status"], serialized_tournement["secondRoundPlayers"],
                                     serialized_tournement["thirdRoundPlayers"])
                tournement_players = tournement.Joueurs
                ordered_list = sorted(tournement_players, key=lambda j: j['Classement'])
                for player in ordered_list:
                    print("Nom_de_famille : " + player["Nom_de_famille"])
                    print("Prenom : " + player["Prenom"])
                    print("Date_de_naissance : " + player["Date_de_naissance"])
                    print("Sexe : " + player["Sexe"])
                    print("Classement : " + player["Classement"] + "\n")
            if option == "5":
                all_tournements = self.db_controller.getAllTournements()
                for tournement in all_tournements:
                    print("Nom : " + tournement["Nom"])
                    print("Lieu : " + tournement["Lieu"])
                    print("Date : " + tournement["Date"])
                    print("Nombre_de_tours : " + str(tournement["Nombre_de_tours"]))
                    print("Tournees : \n")
                    for tour in tournement["Tournees"]:
                        print("name : " + tour["name"])
                        print("beginDateAndHour : " + tour["beginDateAndHour"])
                        print("endDateAndHour : " + tour["endDateAndHour"])
                        print("matches : \n")
                        for match in tour["matches"]:
                            print("Nom_de_famille : " + match[0][0]["Nom_de_famille"])
                            print("Prenom : " + match[0][0]["Prenom"])
                            print("Date_de_naissance : " + match[0][0]["Date_de_naissance"])
                            print("Sexe : " + match[0][0]["Sexe"])
                            print("Classement : " + match[0][0]["Classement"])
                            print("score : " + str(match[0][1]) + "\n")
                            print("contre : \n")
                            print("Nom_de_famille : " + match[1][0]["Nom_de_famille"])
                            print("Prenom : " + match[1][0]["Prenom"])
                            print("Date_de_naissance : " + match[1][0]["Date_de_naissance"])
                            print("Sexe : " + match[1][0]["Sexe"])
                            print("Classement : " + match[1][0]["Classement"])
                            print("score : " + str(match[1][1]) + "\n")
                    print("Joueurs : \n")
                    for player in tournement["Joueurs"]:
                        print("Nom_de_famille : " + player["Nom_de_famille"])
                        print("Prenom : " + player["Prenom"])
                        print("Date_de_naissance : " + player["Date_de_naissance"])
                        print("Sexe : " + player["Sexe"])
                        print("Classement : " + player["Classement"] + "\n")
                    print("Controle_du_temps : " + tournement["Controle_du_temps"])
                    print("Description : " + tournement["Description"])
                    print("status : " + tournement["status"])
                    print("secondRoundPlayers : \n")
                    for player in tournement["secondRoundPlayers"]:
                        print("Nom_de_famille : " + player["Nom_de_famille"])
                        print("Prenom : " + player["Prenom"])
                        print("Date_de_naissance : " + player["Date_de_naissance"])
                        print("Sexe : " + player["Sexe"])
                        print("Classement : " + player["Classement"] + "\n")
                    print("thirdRoundPlayers : \n")
                    for player in tournement["thirdRoundPlayers"]:
                        print("Nom_de_famille : " + player["Nom_de_famille"])
                        print("Prenom : " + player["Prenom"])
                        print("Date_de_naissance : " + player["Date_de_naissance"])
                        print("Sexe : " + player["Sexe"])
                        print("Classement : " + player["Classement"] + "\n")
            if option == "6":
                while True:
                    tournement_name = input("Enter tournement name : ")
                    serialized_tournement = self.db_controller.getTournementByName(tournement_name)
                    if serialized_tournement is not None:
                        break
                    else:
                        print("This tournement was not found try again")
                        continue

                tournement = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"],
                                     serialized_tournement["Date"], serialized_tournement["Nombre_de_tours"],
                                     serialized_tournement["Tournees"], serialized_tournement["Joueurs"],
                                     serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                                     serialized_tournement["status"], serialized_tournement["secondRoundPlayers"],
                                     serialized_tournement["thirdRoundPlayers"])
                all_rounds = tournement.Tournees
                for tour in all_rounds:
                    print("name : " + tour["name"])
                    print("beginDateAndHour : " + tour["beginDateAndHour"])
                    print("endDateAndHour : " + tour["endDateAndHour"])
                    print("matches : \n")
                    for match in tour["matches"]:
                        print("Nom_de_famille : " + match[0][0]["Nom_de_famille"])
                        print("Prenom : " + match[0][0]["Prenom"])
                        print("Date_de_naissance : " + match[0][0]["Date_de_naissance"])
                        print("Sexe : " + match[0][0]["Sexe"])
                        print("Classement : " + match[0][0]["Classement"])
                        print("score : " + str(match[0][1]) + "\n")
                        print("contre : \n")
                        print("Nom_de_famille : " + match[1][0]["Nom_de_famille"])
                        print("Prenom : " + match[1][0]["Prenom"])
                        print("Date_de_naissance : " + match[1][0]["Date_de_naissance"])
                        print("Sexe : " + match[1][0]["Sexe"])
                        print("Classement : " + match[1][0]["Classement"])
                        print("score : " + str(match[1][1]) + "\n")
            if option == "7":
                while True:
                    tournement_name = input("Enter tournement name : ")
                    serialized_tournement = self.db_controller.getTournementByName(tournement_name)
                    if serialized_tournement is not None:
                        break
                    else:
                        print("This tournement was not found try again")
                        continue

                tournement = Tournoi(serialized_tournement["Nom"], serialized_tournement["Lieu"],
                                     serialized_tournement["Date"], serialized_tournement["Nombre_de_tours"],
                                     serialized_tournement["Tournees"], serialized_tournement["Joueurs"],
                                     serialized_tournement["Controle_du_temps"], serialized_tournement["Description"],
                                     serialized_tournement["status"], serialized_tournement["secondRoundPlayers"],
                                     serialized_tournement["thirdRoundPlayers"])
                serialized_rounds = tournement.Tournees

                for tour in serialized_rounds:
                    for match in tour["matches"]:
                        print("Nom_de_famille : " + match[0][0]["Nom_de_famille"])
                        print("Prenom : " + match[0][0]["Prenom"])
                        print("Date_de_naissance : " + match[0][0]["Date_de_naissance"])
                        print("Sexe : " + match[0][0]["Sexe"])
                        print("Classement : " + match[0][0]["Classement"])
                        print("score : " + str(match[0][1]) + "\n")
                        print("contre : \n")
                        print("Nom_de_famille : " + match[1][0]["Nom_de_famille"])
                        print("Prenom : " + match[1][0]["Prenom"])
                        print("Date_de_naissance : " + match[1][0]["Date_de_naissance"])
                        print("Sexe : " + match[1][0]["Sexe"])
                        print("Classement : " + match[1][0]["Classement"])
                        print("score : " + str(match[1][1]) + "\n")
            if option == "8":
                break
