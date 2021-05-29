import sys
from controller import menu_controller

class Menu:

    controller = menu_controller.MenuController()

    def showMenu(self):
        print("Menu :")
        print("1) Ajouter un joueur")
        print("2) Afficher la list des joueurs")
        print("3) Créer un nouveau tournoi")
        print("4) Lancer un tournoi")
        print("5) Générer des rapports")
        print("6) exit")
        self.chooseOption()

    def chooseOption(self):
        while (True):
            option = input("Enter an option:")
            if (option == "1"):
                print("you choosed option 01")
                self.controller.addingNewPlayers()
                self.showMenu()
            if (option == "2"):
                print("you choosed option 02")
                self.controller.displayPlayersList()
                self.showMenu()
            if (option == "3"):
                print("you choosed option 03")
                self.controller.createANewTournement()
                self.showMenu()
            if (option == "4"):
                print("you choosed option 04")
                self.controller.startingTournemant()
                self.showMenu()
            if (option == "5"):
                print("you choosed option 05")
                self.controller.creatReports()
                self.showMenu()
            else:
                print("you choosed to exit")
                sys.exit()