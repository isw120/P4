import sys
from controller import menu_controller
from controller import DatabaseController

class Menu:

    controller = menu_controller.MenuController()
    controller2 = DatabaseController.DatabaseController()

    def showMenu(self):
        print("Menu :")
        print("1) Ajouter un joueur")
        print("2) Créer un nouveau tournoi")
        print("3) Lancer un tournoi")
        print("4) Reprendre un tournoi")
        print("5) Générer des rapports")
        print("6) exit")
        self.chooseOption()

    def chooseOption(self):
        while (True):
            option = input("Enter an option:")
            if (option == "1"):
                joueur = self.controller.addingNewPlayers()
                self.controller2.insertPlayers(joueur)
                self.showMenu()
            if (option == "2"):
                tournoi = self.controller.createANewTournement()
                self.controller2.insertTournement(tournoi)
                self.showMenu()
            if (option == "3"):
                self.controller.startingTournemant()
                self.showMenu()
            if (option == "4"):
                self.controller.continueTournement()
                self.showMenu()
            if (option == "5"):
                self.controller.creatReports()
                self.showMenu()
            if (option == "6"):
                print("you choosed to exit")
                sys.exit()
            else:
                print("wrong option")
                self.showMenu()